# upload-menu-backend

Photo upload service for the **Orderly** menu-recommender app. Accepts a menu
photo (≤ 8 MB), forwards it to the OCR service, and returns an acceptance
receipt. The OCR service is treated as an external dependency.

## Stack

- Python 3.12, FastAPI 0.137, Uvicorn 0.49, httpx 0.28
- Single endpoint: `POST /upload-menu` (field: `photo`)
- Healthcheck: `GET /`

## Run locally

```bash
cd src/upload-menu-backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run with the dev OCR stub on localhost:8002 (default).
uvicorn main:app --reload --port 8001

# Or point at a different OCR service:
OCR_SERVICE_URL="https://my-ocr.example.com/extract-text" \
  uvicorn main:app --reload --port 8001
```

Test the upload:

```bash
curl -F "photo=@./menu.jpg" http://127.0.0.1:8001/upload-menu
# {"status":"accepted","filename":"menu.jpg"}
```

Interactive docs at <http://127.0.0.1:8001/docs>.

## Run tests

```bash
pytest -v
# 12 passed in ~0.4s
```

The test suite mocks the OCR HTTP call via a `fake_ocr` fixture, so no real
OCR service needs to be running.

> **Important:** run from `src/upload-menu-backend/`. Running `pytest` from
> the repo root will also collect the script-style tests in `src/backend/`,
> which require `openai` and will fail to collect.

## Environment variables

| Variable          | Default                                | Purpose                                                              |
|-------------------|----------------------------------------|----------------------------------------------------------------------|
| `OCR_SERVICE_URL` | `http://localhost:8002/extract-text`   | Where the photo is forwarded to after the size check.                |
| `ALLOWED_ORIGINS` | `*`                                    | Comma-separated CORS origins. Set to your frontend URL in prod.      |
| `PORT`            | `8000`                                 | Listening port (set automatically by Render / Railway).              |

`OCR_SERVICE_URL` is the integration point with the OCR service that lives
on a different machine. Set it to the public URL of that service when
deploying.

## Deploy to Render (recommended for demo)

Render gives you a public HTTPS URL for a FastAPI service in ~5 minutes,
free tier.

1. **Push the branch** with these changes to GitHub.
2. Go to <https://render.com>, sign in with GitHub.
3. Click **New → Web Service**, pick the `Orderly-Team24/team-24` repo.
4. Configure:
   - **Root directory:** `src/upload-menu-backend`
   - **Runtime:** Docker (Render auto-detects the `Dockerfile`)
   - **Instance type:** Free
   - **Environment variables:**
     - `OCR_SERVICE_URL` → your OCR service URL (the team has it on a
       separate device; paste the public URL here)
     - `ALLOWED_ORIGINS` → your frontend URL, or `*` for the demo
5. Click **Create Web Service**. First deploy takes ~3 min.
6. Once live, Render shows you a URL like
   `https://orderly-upload-menu-backend.onrender.com`. Test:
   ```bash
   curl https://orderly-upload-menu-backend.onrender.com/
   # {"status":"ok","service":"upload-menu-backend"}
   ```
7. In `src/frontend/photo_from_gallery/script.js`, set:
   ```js
   const API_BASE_URL = "https://orderly-upload-menu-backend.onrender.com";
   ```
   Deploy the frontend (see "Deploy the frontend" below).

### Notes on Render free tier

- Spins down after 15 min of inactivity. First request after that takes
  ~30s. Fine for a demo, mention it to your instructor.
- 750 hours/month free.

## Deploy the frontend

The frontend (`src/frontend/photo_from_gallery/`) is static HTML/JS/CSS. Two
easy options:

### Option A: Render Static Site

1. **New → Static Site**, same repo.
2. **Root directory:** `src/frontend/photo_from_gallery`
3. **Build command:** *(leave empty)*
4. **Publish directory:** `.`
5. After deploy, Render gives you a URL like
   `https://orderly-photo-upload.onrender.com`.

### Option B: GitHub Pages

1. Push the frontend to a separate branch, e.g. `gh-pages`.
2. Settings → Pages → Source: `gh-pages` branch, `/` root.
3. Public URL: `https://<your-org>.github.io/team-24/photo_from_gallery/`.

If you choose GitHub Pages, set `API_BASE_URL` in `script.js` to your
Render backend URL before pushing.

## Architecture

```
Browser ──► /upload-menu ──► upload-menu-backend (this service) ──► OCR service
                              (this repo, Render)                  (other device)
```

- This service does **not** run OCR or any AI itself. It only validates
  the upload (size) and forwards it.
- The OCR service is a separate component on a different device owned by
  the team. `OCR_SERVICE_URL` points at it.
- For the demo, if the OCR service is offline, the upload still succeeds
  in reaching this service but returns 502 (OCR unreachable). The frontend
  shows the error message — that's correct behavior, not a bug.

## What's intentionally NOT in this service

- No tesseract / OCR code (lives on the OCR service device).
- No AI / LLM code (lives in `src/backend/`).
- No DB (no persistence needed for upload-and-forward).
- No auth (out of scope for MVP).