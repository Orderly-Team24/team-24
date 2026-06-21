import os

import httpx
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# OCR service endpoint (handled by US-011-2)
OCR_SERVICE_URL = os.getenv("OCR_SERVICE_URL", "http://localhost:8002/extract-text")

# Comma-separated list of allowed CORS origins. Override via env in deploy.
# Use "*" for demos; lock down to your frontend origin in production.
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Maximum allowed image size: 8 MB
MAX_IMAGE_SIZE = 8 * 1024 * 1024


@app.get("/")
def root() -> dict[str, str]:
    """Cheap healthcheck used by Render / uptime monitors."""
    return {"status": "ok", "service": "orderly-upload-menu"}


@app.post("/upload-menu")
async def upload_menu(photo: UploadFile = File(...)):
    """
    Upload a menu photo and forward it to the OCR service.
    The OCR service handles text extraction and further processing.
    
    Args:
        photo: Menu image file (max 8 MB).
    
    Returns:
        Confirmation that the photo was accepted.
    
    Raises:
        413: File size exceeds 8 MB.
        504: OCR service timed out.
        502: OCR service returned an error.
    """
    
    # Read the uploaded file into memory
    image_bytes = await photo.read()

    # Validate file size
    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 8 MB")
    
    # Forward the image to the OCR service
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OCR_SERVICE_URL,
                files={"photo": (photo.filename, image_bytes, photo.content_type)},
            )
            response.raise_for_status()
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="OCR service timeout")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"OCR service error: {e}")

    # Photo accepted — OCR service handles the rest
    return {
        "status": "accepted",
        "filename": photo.filename
    }
