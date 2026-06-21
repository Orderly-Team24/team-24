# Minimal Dockerfile for the upload-menu-backend service.
# Build context must be the repository root (Render defaults to .), so we
# COPY files using their full repo-relative paths.
FROM python:3.12-slim

# Install Tesseract OCR engine + English language pack. Tesseract is the
# system binary that pytesseract wraps; without it, image_to_string fails.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first so this layer is cached when only source changes.
COPY src/upload-menu-backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Source.
COPY src/upload-menu-backend/main.py ./

# Tesseract data is owned by root; allow appuser to read it.
# (Tesseract writes nothing at runtime, so no extra write perms needed.)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Render expects $PORT; default to 8000 for local docker runs.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]