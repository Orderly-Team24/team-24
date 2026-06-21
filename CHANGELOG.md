## [0.1.0] - 2026-06-21

First public deployment of all three Orderly services: recommender backend, upload-menu backend, and the static frontend, wired together end-to-end.

### Added
- Backend: `AI_BACKEND` switch in `ai_service.py` supporting `stub` (deterministic offline fallback), `openai`, and `lmstudio`; existing endpoint behavior preserved.
- Backend: POST `/display/recommendations` returning structured `{ recommendations: [{ id, name, price, description, ingredients, reason }, ...] }`.
- Upload-menu backend: POST `/upload-menu` (multipart `photo`, max 8 MB, CORS-enabled, JWT-optional), forwards to `OCR_SERVICE_URL`.
- Dockerfiles, `.dockerignore`, `requirements.txt`, and `README.md` for both `src/backend/` and `src/upload-menu-backend/`, repo-relative `COPY` paths so Render uses the repo root as build context.
- Frontend: shared `src/frontend/config.js` exposing `API_RECOMMENDER` and `API_UPLOAD` as the single source of truth for backend URLs.
- Frontend: `src/frontend/netlify.toml` for static-site deployment.
- Frontend: `/photo_from_gallery/` page with file picker, preview, size/format validation, and server response display.
- Frontend: absolute paths and Vercel rewrites so `/food-recommender/` and `/photo_from_gallery/` resolve correctly from any page.

### Changed
- Frontend `config.js` updated to point at the deployed Render backends (`https://team-24.onrender.com`, `https://team-24-1.onrender.com`) instead of localhost.
- Recommender and upload-menu backends: CORS defaults to `*` (configurable via `ALLOWED_ORIGINS` env).
- Recommender backend: optional `OPENAI_API_KEY`; defaults to `stub` mode when unset so the service runs offline-safe.

### Fixed
- Frontend: navigation links used relative paths and broke when entering pages directly; switched to absolute paths.
- Frontend: `/food-recommender/` returned 404 on Vercel when accessed via a deep link; added rewrites so the route resolves to `index.html`.

### Security
- Frontend: AI-generated text is HTML-escaped before being rendered as dish cards (defense in depth against XSS from model output).