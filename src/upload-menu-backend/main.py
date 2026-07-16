import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from parser import parse_menu
from ocr_layout import reconstruct_text
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from pytesseract import Output
import os

tesseract_path = os.environ.get("TESSERACT_PATH")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
import os

ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
# Maximum allowed image size: 8 MB
MAX_IMAGE_SIZE = 8 * 1024 * 1024

# Below this width, Tesseract reliably fails to read menu text — verified:
# a 349px-wide photo returned only a decorative title, 0 dish/price words;
# upscaling 3x recovered 59 real words. Scale small photos up before OCR
# instead of letting recognition silently fail.
MIN_OCR_WIDTH = 1200

# Supported image content types for OCR
SUPPORTED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

# Uniform block of text — reads multi-column menus and right-aligned prices
# much more reliably than Tesseract's default page mode on styled menu photos.
TESSERACT_CONFIG = "--psm 6"


def _upscale_if_small(image: Image.Image) -> Image.Image:
    """Scale up low-resolution photos before OCR.

    Tesseract's accuracy drops sharply once individual characters get too
    small in absolute pixels, which happens with small source photos even
    if the menu text is perfectly legible to a human. LANCZOS resampling
    keeps upscaled text edges reasonably crisp for OCR purposes.
    """
    if image.width >= MIN_OCR_WIDTH:
        return image
    scale = MIN_OCR_WIDTH / image.width
    new_size = (MIN_OCR_WIDTH, round(image.height * scale))
    return image.resize(new_size, Image.LANCZOS)


def _prepare_for_ocr(image: Image.Image) -> Image.Image:
    """Upscale small photos and boost contrast before OCR.

    Decorative menu images often use light-on-cream text with dotted price
    leaders; without preprocessing Tesseract frequently misses right-aligned
    prices entirely, leaving the recommender with almost no valid dishes.
    """
    scaled = _upscale_if_small(image)
    gray = ImageOps.grayscale(scaled.convert("RGB"))
    gray = ImageEnhance.Contrast(gray).enhance(2.0)
    return ImageEnhance.Sharpness(gray).enhance(1.5)


@app.post("/upload-menu")
async def upload_menu(photo: UploadFile = File(...)):
    """
    Upload a menu photo, run OCR on it locally, and return the extracted text.

    Args:
        photo: Menu image file (max 8 MB, JPEG/PNG/WEBP).

    Returns:
        Confirmation with the filename and the OCR'd text.

    Raises:
        413: File size exceeds 8 MB.
        415: Unsupported content type.
        422: Image cannot be decoded.
        500: OCR engine failed.
    """
    # Read the uploaded file into memory
    image_bytes = await photo.read()

    # Validate file size
    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 8 MB")

    # Validate content type
    content_type = (photo.content_type or "").lower()
    if content_type not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type: {content_type}. "
                   f"Use one of {sorted(SUPPORTED_CONTENT_TYPES)}.",
        )

    # Decode image
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.load()
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Could not decode image: {exc}",
        )

    # Run OCR. We use image_to_data (word-level bounding boxes) instead of
    # plain image_to_string, so reconstruct_text() can detect and correctly
    # handle 2-column menu layouts instead of interleaving both columns'
    # words into garbled single lines.
    try:
        ocr_image = _prepare_for_ocr(image)
        ocr_data = pytesseract.image_to_data(
            ocr_image,
            lang="rus+eng",
            output_type=Output.DICT,
            config=TESSERACT_CONFIG,
        )
        extracted_text = reconstruct_text(ocr_data, ocr_image.width)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OCR engine failed: {exc}",
        )
    structured_menu = parse_menu(extracted_text)

    return {
        "status": "accepted",
        "filename": photo.filename,
        "extracted_text": extracted_text,
        "menu": structured_menu,
    }
