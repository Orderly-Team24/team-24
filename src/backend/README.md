# backend

Recommender service for the **Orderly** menu app. Exposes a single
recommendation endpoint backed by a swappable AI module.

## Endpoints

| Method | Path                       | Purpose                                                              |
|--------|----------------------------|----------------------------------------------------------------------|
| GET    | `/`                        | Healthcheck (used by Render).                                        |
| POST   | `/recommend`               | Legacy. Returns `{recommendation: "free-form text"}`.                 |
| POST   | `/display/recommendations` | Frontend-facing. Returns structured card data.                       |
| POST   | `/history/orders`          | Save a dish into a user's order history (in-memory stub).            |
| GET    | `/history/orders`          | Read a user's order history, most-recent first.                      |
| GET    | `/history/orders/check`    | Whether a given dish is already in a user's history.                 |

Interactive docs at `/docs`.

### Order history (stub)

The `/history/orders*` endpoints back the **"I'll order it again"** button
on the recommendation card. No real database yet — everything lives in a
thread-safe in-memory `dict`, so data is lost on restart. When a real DB
lands, only `order_history.py` needs to change; the HTTP shape stays.

Each dish gets a stable id derived from its name (32-bit hash). The
frontend passes the dish from `/display/recommendations` straight to
`POST /history/orders` with the `X-User-Id` header.

```bash
# Save a dish
curl -X POST http://127.0.0.1:8003/history/orders \
  -H 'Content-Type: application/json' \
  -H 'X-User-Id: dasha' \
  -d '{"name":"Margherita pizza","price":13,"description":"...","ingredients":["flour","tomato"],"reason":"classic"}'

# Read history
curl http://127.0.0.1:8003/history/orders -H 'X-User-Id: dasha'

# Check whether a dish is already in history (used by the button label)
curl 'http://127.0.0.1:8003/history/orders/check?dish_id=42' -H 'X-User-Id: dasha'
```

## AI backends

Picked at startup via `AI_BACKEND`:

| Value      | What it does                                            | Requires                          |
|------------|---------------------------------------------------------|-----------------------------------|
| `stub`     | Deterministic fake responses (default).                 | nothing — works anywhere          |
| `openai`   | Calls OpenAI Chat Completions API.                      | `OPENAI_API_KEY`                  |
| `lmstudio` | Calls LM Studio's OpenAI-compatible endpoint.           | `LMSTUDIO_BASE_URL` (local-only)  |

If a backend raises (no key, server down, malformed JSON), the service
silently falls back to the stub so the demo never breaks. Render logs will
show the warning.

### Examples

```bash
# Default — stub, no setup.
AI_BACKEND=stub uvicorn main:app --reload --port 8003

# Real OpenAI.
AI_BACKEND=openai OPENAI_API_KEY=sk-... \
  uvicorn main:app --reload --port 8003

# LM Studio running on your laptop.
AI_BACKEND=lmstudio LMSTUDIO_BASE_URL=http://localhost:1234/v1 \
  LMSTUDIO_MODEL="qwen/qwen3.5-9b" \
  uvicorn main:app --reload --port 8003
```

## Environment variables

| Variable             | Default                          | Purpose                                              |
|----------------------|----------------------------------|------------------------------------------------------|
| `AI_BACKEND`         | `stub`                           | `stub`, `openai`, or `lmstudio`.                     |
| `OPENAI_API_KEY`     | _(unset)_                        | Required if `AI_BACKEND=openai`.                     |
| `OPENAI_BASE_URL`    | OpenAI API                       | Override for Azure / proxies.                        |
| `OPENAI_MODEL`       | `gpt-4o-mini`                    | Any chat-completions model.                          |
| `LMSTUDIO_BASE_URL`  | `http://localhost:1234/v1`       | LM Studio endpoint.                                  |
| `LMSTUDIO_API_KEY`   | `lm-studio`                      | LM Studio ignores it but the client requires a value.|
| `LMSTUDIO_MODEL`     | `qwen/qwen3.5-9b`                | Whatever is currently loaded in LM Studio.           |
| `ALLOWED_ORIGINS`    | `*`                              | Comma-separated CORS origins.                        |
| `PORT`               | `8000`                           | Listening port (set automatically by Render).        |

## Run locally

```bash
cd src/backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Stub backend (no setup, demo works out of the box).
uvicorn main:app --reload --port 8003

# Or with the real OpenAI backend:
AI_BACKEND=openai OPENAI_API_KEY=sk-... uvicorn main:app --reload --port 8003
```

Test:

```bash
curl http://127.0.0.1:8003/                                                # healthcheck
curl -X POST http://127.0.0.1:8003/display/recommendations \
  -H 'Content-Type: application/json' \
  -d '{"message": "something vegetarian and cheap"}'
# {"recommendations":[{"id":1,"name":"Mushroom risotto",...}]}
```

## Deploy to Render

1. **New → Web Service** on Render, pick the repo.
2. Configure:
   - **Root directory:** leave empty (repository root) — this service's
     code imports `src/db/database.py`/`models.py` via a `../db` path, and
     Docker can only reach that if the build context includes both
     `src/backend/` and `src/db/`. Setting Root Directory to `src/backend`
     will fail with `requirements.txt: not found` at build time.
   - **Dockerfile Path:** `src/backend/Dockerfile` (relative to repo root)
   - **Runtime:** Docker
   - **Instance type:** Free
   - **Environment variables:**
     - `AI_BACKEND` → `stub` (default) or `openai`
     - `OPENAI_API_KEY` → your key (only if `AI_BACKEND=openai`)
     - `ALLOWED_ORIGINS` → `https://<your-site>.netlify.app`
     - `DATABASE_URL`, `JWT_SECRET_KEY` — see `src/db`'s and `auth.py`'s docs
3. **Create Web Service**. Once live you'll get a URL like
   `https://orderly-recommender.onrender.com`.
4. This service no longer handles menu-photo upload/OCR at all — that's
   `src/upload-menu-backend`, deployed separately. Point
   `src/new-frontend`'s upload flow at that service's URL.

## What's NOT in this service anymore

- OCR (menu photo upload) — this used to be duplicated here (`ocr_reader.py`,
  a `POST /upload-menu` endpoint, `tesseract-ocr` installed in the image)
  even though the frontend only ever called the dedicated
  `src/upload-menu-backend` service for it (see ADR-001). Removed the dead
  copy; `parser.py` stays since `tests/test_parser.py` still covers it and
  it has no OCR dependencies of its own.
- The previous version also called LM Studio directly, which crashed on
  Linux and required the model to run on the same host:
  - `ai_service.py` no longer touches LM Studio by default. Set
    `AI_BACKEND=lmstudio` to bring it back locally.
  - `retriever.py` (LangChain + Chroma) is unused by the live endpoints but
    kept in the repo for the offline scripts in `test_*.py`.

If you want to put RAG back into the live service, the seam is
`ai_service._lmstudio_backend` — extend it to call the retriever before
hitting the model.