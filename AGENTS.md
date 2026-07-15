# AGENTS.md

Instructions for AI coding agents (Claude Code, GitHub Copilot workspace agents, etc.) working in this repository. Human contributors should read [CONTRIBUTING.md](CONTRIBUTING.md) instead — this file exists because agents need a few things spelled out that a human picks up implicitly from context.

## Project shape

Three deployable services, one repo:

- `src/backend/` — Recommender API (FastAPI). Owns AI recommendation logic (`ai_service.py`), auth (`auth.py`), user preferences, order history/dislikes (`history_router.py`, `order_history.py`). Deployed to Render as `team-24`.
- `src/upload-menu-backend/` — OCR/menu upload API (FastAPI + Tesseract). Deployed to Render as `team-24-1`.
- `src/new-frontend/` — React SPA. Deployed to Vercel from `main`.
- `src/db/` — SQLAlchemy models + Alembic migrations, shared by the recommender service.

Full details: [README.md § Project structure](README.md#project-structure), [docs/architecture/](docs/architecture/README.md).

## Before making a change

1. Read [docs/development-process.md](docs/development-process.md) for branch naming, PR, and CI conventions — follow them exactly, don't invent a new pattern.
2. Check for other open PRs touching the same file before starting — `display_recommendations.py` and `App.js` in particular have repeatedly been the target of parallel, independently-merged PRs that conflict with each other. If you open a PR and it later shows a merge conflict against `main` because another PR landed first, resolve it by keeping **both** sides' additions (they're almost always independent, additive features stacked in the same function) rather than picking one side.
3. One fix/feature per branch/PR. Don't bundle unrelated changes.

## Running things locally

```bash
# Backend (recommender), stub AI backend — no API key needed
cd src/backend && AI_BACKEND=stub uvicorn main:app --reload --port 8003

# Backend (OCR upload)
cd src/upload-menu-backend && uvicorn main:app --reload --port 8002

# Frontend
cd src/new-frontend && npm start
```

Tests:
```bash
cd src/backend && pytest tests/ -v
cd src/upload-menu-backend && pytest tests/ -v
```

There is **no automated test suite for the frontend**. Any frontend change should be manually exercised (or at minimum have its logic traced through by hand) before being claimed as verified — don't report a frontend fix as done on the strength of a type-check alone.

## Things that have bitten agents (and humans) working in this repo before

- **`AI_BACKEND` defaults to `stub` locally and in CI, but production runs `AI_BACKEND=openai`.** A fix that only changes prompt wording or relies on the LLM "being told" not to do something is not a guarantee — real models (gpt-4o-mini) have been observed hallucinating against explicit system-prompt instructions in this codebase (see the negation-extraction guard in `ai_service.py`). Prefer hard filters over prompt-only instructions wherever the failure mode is unsafe (allergens, excluded ingredients) or user-visible (recommending something the user explicitly didn't want).
- **`order_history.py` now persists to PostgreSQL** (`order_history`/`dislikes` tables, see ADR-002) via a `db: Session` parameter — same `get_db` dependency pattern as `auth.py`/`users.py`. It used to be an in-memory `dict` that restarts wiped; that's fixed as of Sprint 5 (issue #338). There's no `/history/_reset` endpoint anymore — it was a dev/test convenience that became a real live-data-wiping foot-gun once the store was backed by a real database, so it was removed. Tests reset state via `order_history.reset_for_tests(db)` called directly, not over HTTP.
- **`localStorage.userId` has been the source of multiple real bugs** (order history appearing empty, orders/dislikes pooling under the wrong identity). If you touch anything in `RegisterPage.jsx`, `LoginPage.jsx`, `FoodRecommenderPage.jsx`, or `HistoryPage.jsx`, verify `userId` is actually being set/read consistently across all four — it's easy to fix one and miss another.
- **A missing `<Route>` in `App.js` produces a silent blank page**, not a build error — React Router logs "No routes matched location" to the console but renders nothing. If a page "doesn't show anything," check the browser console for that message before assuming it's a data/API problem.
- **The live backend and frontend are real, deployed services** (`https://team-24.onrender.com`, `https://team-24-1.onrender.com`, `https://team-24-navy.vercel.app`). Prefer testing against a local stub/dev server; if you do exercise the live backend directly (e.g. via `curl`) to confirm a fix, prefer read-only calls or calls against a disposable test account, and never call destructive/reset endpoints.

## Documentation upkeep

If your change affects setup, workflow, architecture, quality requirements, or known limitations, update the relevant file under `docs/`, `CONTRIBUTING.md`, this file, or `CHANGELOG.md` in the same PR — not as a follow-up. See [docs/customer-handover.md](docs/customer-handover.md) for what the customer has been told is current and accurate; don't let it silently drift out of date.
