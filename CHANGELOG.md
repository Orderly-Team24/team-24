## [Unreleased]

### Added
- Order history and dislikes (US-015): dislike storage + endpoints, filtering future recommendations by disliked dishes, and a frontend History page with a "Dislike" button per order.
- AI recommender now recognizes meal type (breakfast/lunch/dinner/brunch/supper) named in the free-text mood/craving field and prefers a matching dish when the menu has one.
- AI recommender never recommends a beverage (water, soda, coffee, juice, etc.) on its own as "the dish" — a drink is not a meal.
- LLM-backed supplement for parsing plain-language exclusions ("keep it away from shellfish") that the regex-based extractor misses, for deployments using a real LLM backend.
- "Another option" no-repeat guarantee: a dish already shown in the current session is never shown again until every candidate has been shown once.
- 3 new user acceptance test scenarios (UAT-08, UAT-09, UAT-10) covering order history/dislike, AI exclusion safety, and meal-type/beverage handling.
- `CONTRIBUTING.md`, `AGENTS.md`, and `docs/customer-handover.md` — Assignment 6 maintained assets.
- OCR: column-aware layout reconstruction, currency-symbol handling, and menu section detection, improving parsing of menus that don't fit the single-column layout the parser previously assumed.

### Changed
- Excluded ingredients (allergies, dislikes, and plain-language exclusions like "I don't want steak") are now a hard, code-enforced guarantee on every AI backend, including `openai`/`lmstudio` — previously this only worked reliably in stub mode and could silently fall back to recommending an excluded dish when every candidate matched.
- Removed the `cuisine` preference entirely. It was accepted end-to-end (UI → API → LLM prompt) but never actually persisted or collected from any real user input — every caller always sent `null`.

### Fixed
- Order history and disliked dishes are now persisted in PostgreSQL (the existing `order_history`/`dislikes` tables from ADR-002) instead of an in-memory store — they survive service restarts/redeploys like accounts and preferences already did. Removed the `/history/_reset` dev endpoint along with it: it was a test convenience that became a real live-data-wiping risk once the store held real persisted data.
- OCR layout reconstruction now detects an arbitrary number of columns (3+) and uneven splits via gap-based left-edge clustering, instead of only splitting at the image midline into at most two halves.
- README: fresh-clone backend setup crashed with `RuntimeError: DATABASE_URL is not set` — the Postgres migration (ADR-002) has required it since 0.3.0, but the README never mentioned it. Added the env var (SQLite connection string for local dev) and the missing `alembic upgrade head` step; verified end-to-end on a clean clone.
- README: linked the Week 5 report, which existed but wasn't linked from anywhere.
- CI: fixed lychee (link-checker) failures on open PRs — a release link left dangling by the `0.3.0` → `v0.3.0` tag rename, and a GitHub Pages link that 404s on PR branches since Pages only ever builds from `main` (excluded from the check for now).
- Menu OCR parser mixed up a dish's name with its description on multi-line scans (real menus put the name on its own line, description + price on the next), which read as "the second menu photo didn't work" in customer UAT.
- Registration gave no loading feedback, letting a slow connection cause a double submit and a false "email already in use" error.
- Allergen/excluded-ingredient filtering silently fell back to an unfiltered candidate pool when every dish matched the exclusion, instead of returning no recommendation — the one scenario where the safety guarantee mattered most.
- The "Another option" button dropped the user's mood/craving text on every click after the first, replacing it with a bare placeholder string — so a stated exclusion ("I don't want steak") stopped applying after the first re-roll.
- LLM-backed negation extraction could hallucinate an exclusion for a purely positive message (e.g. "I want fish" being read as excluding fish); it now only runs when the message actually contains a negation word.
- An expired or invalid access token locked users out of both `/login` and `/register` (each page redirected the other way) instead of clearing the stale token and letting them log in again; the Profile page also now redirects to login on a 401 instead of showing a stuck error.
- Order history/dislikes appeared empty (or, worse, pooled across different users) because the frontend saved orders under a hardcoded/mismatched user identity instead of the logged-in user's real id. Root-caused to `/auth/login` not returning `user_id` at all, and to the post-registration auto-login flow independently having the same gap; fixed both, plus added the first backend test coverage for `/auth/register` and `/auth/login`.
- The History page rendered a blank screen — `App.js` never registered a route for `/history`, even though the page and its nav link both existed.

### Notes for next-sprint owner
- JWT signing secret is hardcoded in `src/backend/jwt_handler.py` rather than sourced from an environment variable — externalize before relying on this for anything beyond a course project.
- Two Render services (`team-24`, `team-24-1`) and two frontend hosts have drifted in the past (different `API_URL` values hardcoded per page) — worth auditing before the next release.
- OCR multi-column layout reconstruction clusters non-price word left-edges across horizontal gutters (any number of columns, including uneven widths) instead of assuming a single midline split; handwritten specials boards are still out of scope.
- OCR menu parsing is tuned for one common layout (name on its own line, description + price after); non-Latin currency symbols aren't handled reliably yet.

---

## [0.3.0] - 2026-07-05 "MVP v2"

### Added
- PostgreSQL database (SQLAlchemy models + Alembic migrations) backing users, preferences, refresh tokens, and order history tables.
- User registration (`POST /auth/register`) and login (`POST /auth/login`), issuing JWT access/refresh tokens.
- Profile page: view and edit saved preferences (`GET`/`PATCH /users/me/preferences`), Bearer-token authenticated.
- Delete account (`DELETE /users/me`), Bearer-token authenticated, cascades to preferences and refresh tokens.
- "End session" button and "specify today's meal intent" alongside budget on the upload step.
- Architecture documentation (`docs/architecture/`: component, sequence, and deployment diagrams, plus 3 ADRs) and `docs/development-process.md`.

### Changed
- Registration now actually calls the backend and logs the user in immediately, instead of only caching form input in the browser and never creating an account.
- Returning (logged-in) users skip the preferences questionnaire and go straight to the upload step; their saved preferences are pulled from the backend automatically.
- `PATCH /users/me/preferences` now supports partial updates — a body with only one field no longer wipes the other two.

### Fixed
- AI recommendations silently ignored the uploaded/OCR'd menu when using the `openai`/`lmstudio` backends — the menu never reached the LLM prompt (only the `stub` backend used it). Recommendations are now always based on the actual uploaded menu.
- `bcrypt==4.0.1` crashed passlib's backend self-test on any password hash/verify call, breaking registration and login entirely; pinned to `bcrypt==3.2.2`.
- The recommender's Dockerfile was missing `user_route.py`, `auth.py`, `users.py`, and `jwt_handler.py`, and couldn't reach `src/db/` from its build context — both broke Render deploys. Rebuilt around a repo-root build context that can see both `src/backend/` and `src/db/`.
- Removed a fully duplicated OCR endpoint/module from the recommender service — the dedicated `upload-menu-backend` service is the one the frontend actually calls; the copy in the recommender was dead code with its own `tesseract-ocr` apt dependency bloating that image.
- Two parallel PRs implemented the same `/users/me/preferences` endpoints in different files, registering duplicate routes on the same path; consolidated into one implementation.

## [0.2.0] - 2026-06-28 "Sprint 2"

### Added
- Preferences questionnaire with allergen and diet fields.
- Menu upload and manual menu parsing (dish name + price structuring).
- Budget filtering and recommendation logic based on user preferences.
- "Another option" flow without re-uploading the menu.
- Order history stub ("I'll order it" button).
- Frontend migration to React with a 3-page flow.
- Docker deployment and CI pipeline with tests and link checking.
- Local Tesseract OCR (pytesseract + system `tesseract-ocr` binary in Docker) replacing the HTTP-forward stub from 0.1.0.
- CORS middleware on the upload-menu backend.

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