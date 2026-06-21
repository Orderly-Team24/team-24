import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image
import pytesseract

app = FastAPI()

# Maximum allowed image size: 8 MB
MAX_IMAGE_SIZE = 8 * 1024 * 1024

# Supported image content types for OCR
SUPPORTED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


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

    # Run OCR
    try:
        extracted_text = pytesseract.image_to_string(image)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OCR engine failed: {exc}",
        )

    return {
        "status": "accepted",
        "filename": photo.filename,
        "extracted_text": extracted_text,
    }