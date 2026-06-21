## [Unreleased]

### Planned
- **OCR locally via Tesseract** — move `/upload-menu` from HTTP-forward stub to local Tesseract OCR (pytesseract + system `tesseract-ocr` binary in Docker). Returns `{status, filename, extracted_text}` and integrates with downstream parser. This was prototyped in branch `feat/connect-backends-deploy` (commits `80a1e9e`, `9aae267`) but rolled back before merge — to be re-done in the next sprint.
- **CORS middleware on upload-menu backend** — same `ALLOWED_ORIGINS` env pattern as recommender; needed for browser `fetch()` from the deployed frontend.
- **Absolute paths for static assets** — `style.css` / `script.js` on sub-pages resolved relative to the current URL; switched to absolute `/<page>/<asset>` so deep links work.

### Notes for next-sprint owner
- Tesseract must be installed **system-wide** (not via pip). On Render: `apt-get install tesseract-ocr tesseract-ocr-eng` in the Dockerfile. On dev machines: `brew install tesseract` (macOS) or download from UB-Mannheim (Windows, set `TESSERACT_PATH` env).
- The current `OCR_SERVICE_URL = "http://localhost:8002/extract-text"` default in `src/upload-menu-backend/main.py` is a **stub** and will return 502 for every upload — fine for development, broken for demos.
- A shared PostgreSQL database on Render is the agreed-upon storage layer for upcoming auth, dislikes, and likes user stories.

---

## [0.1.0] - 2026-06-21

First public deployment of all three Orderly services: recommender backend, upload-menu backend, and the static frontend, wired together end-to-end.

### Added
- Backend: `AI_BACKEND` switch in `ai_service.py` supporting `stub` (deterministic offline fallback), `openai`, and `lmstudio`; existing endpoint behavior preserved.
- Backend: POST `/display/recommendations` returning structured `{ recommendations: [{ id, name, price, description, ingredients, reason }, ...] }`.
- Upload-menu backend: POST `/upload-menu` (multipart `photo`, max 8 MB), forwards to `OCR_SERVICE_URL` (currently a stub — real OCR is a next-sprint task).
- Dockerfiles, `.dockerignore`, `requirements.txt`, and `README.md` for both `src/backend/` and `src/upload-menu-backend/`, repo-relative `COPY` paths so Render uses the repo root as build context.
- Frontend: shared `src/frontend/config.js` exposing `API_RECOMMENDER` and `API_UPLOAD` as the single source of truth for backend URLs.
- Frontend: `src/frontend/netlify.toml` for static-site deployment.
- Frontend: `/photo_from_gallery/` page with file picker, preview, size/format validation, and server response display.
- Frontend: absolute paths and Vercel rewrites so `/food-recommender/` and `/photo_from_gallery/` resolve correctly from any page.

### Changed
- Frontend `config.js` updated to point at the deployed Render backends (`https://team-24.onrender.com`, `https://team-24-1.onrender.com`) instead of localhost.
- Recommender backend: optional `OPENAI_API_KEY`; defaults to `stub` mode when unset so the service runs offline-safe.
- Upload-menu backend: `OCR_SERVICE_URL` is a placeholder (`http://localhost:8002/extract-text`) — uploads will 502 until the real OCR service or local Tesseract is wired up.

### Known limitations (carried into next sprint)
- No CORS middleware on the upload-menu backend — browser `fetch()` from the deployed frontend may be blocked until the CORS fix lands (see Unreleased).
- OCR is a forwarder only — no local image processing yet.
- No authentication, no persistent user data, no dislikes/likes storage yet.

### Fixed
- Frontend: navigation links used relative paths and broke when entering pages directly; switched to absolute paths.
- Frontend: `/food-recommender/` returned 404 on Vercel when accessed via a deep link; added rewrites so the route resolves to `index.html`.

### Security
- Frontend: AI-generated text is HTML-escaped before being rendered as dish cards (defense in depth against XSS from model output).