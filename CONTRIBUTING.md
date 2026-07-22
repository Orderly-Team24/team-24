# Contributing to Orderly

This document is the practical entry point for anyone (team member, new contributor, or the customer's own team) who wants to make a change to Orderly. It summarizes the day-to-day workflow; see [docs/development-process.md](docs/development-process.md) for the full rationale and history.

## Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- `tesseract-ocr` installed locally if you're working on `src/upload-menu-backend/` (see [README.md](README.md) for OS-specific install commands)

## Setting up a local environment

Follow [README.md § Getting started](README.md#getting-started-local-development) to run both backend services and the frontend locally. In short:

```bash
python -m venv venv && source venv/bin/activate
pip install -r src/backend/requirements.txt
pip install -r src/upload-menu-backend/requirements.txt
export DATABASE_URL="sqlite:///$(pwd)/local.db"
export JWT_SECRET_KEY="local-dev-secret"
cd src/db && alembic upgrade head && cd ../..
```

## Making a change

1. **Pick an issue.** All work should trace back to a GitHub issue (a user story, task, or bug). If none exists for what you want to do, open one first.
2. **Branch from `main`**, named `<issue-number>-short-description` (e.g. `285-task-us-015-1-backend-dislike-storage-endpoints`). See [docs/development-process.md § Branch Naming](docs/development-process.md#branch-naming).
3. **Write the change and its tests together.** Both backend services (`src/backend/`, `src/upload-menu-backend/`) have `pytest` suites — run them before opening a PR:
```bash
   cd src/backend && pytest tests/ -v --cov=. --cov-report=term-missing
   cd src/upload-menu-backend && pytest tests/ -v --cov=. --cov-report=term-missing
```
   The frontend (`src/new-frontend/`) has no automated test suite yet — verify UI changes manually (`npm start`) against the golden path and at least one edge case.

   > **Known issue (root cause found, fix pending confirmation on production):** order history persistence had a live regression despite #338 being closed — traced to a broken Alembic migration chain, not the DB-backed rewrite itself. See [AGENTS.md](AGENTS.md) for the full root cause before touching `order_history.py`, migrations, `localStorage.userId`-related files, or History-related endpoints. The fix needs `alembic upgrade head` re-run against the live database to take effect there.
4. **Open a PR** using the template in `.github/pull_request_template.md`: reference the issue with `Closes #<number>`, describe what was done, and how to test it.
5. **Update `CHANGELOG.md`** under `[Unreleased]` for any user-visible change — that's how the team assembles each SemVer release.
6. **Get one review from someone other than the author.** The reviewer checks acceptance criteria, tests, CI status, and that no other open PR touches the same endpoint/route (a real recurring source of merge conflicts in this repo — see recent history of `src/backend/display_recommendations.py`).
7. **Update documentation** if the change touches architecture, quality requirements, dev process, or user-facing behavior covered in `docs/`.

## Code review expectations

See [docs/development-process.md § Pull Request Process](docs/development-process.md#pull-request-process) and [docs/definition-of-done.md](docs/definition-of-done.md) for the full checklist. The short version: acceptance criteria met, tests cover the changed logic, no secrets committed, CHANGELOG updated, CI green (checked manually — not yet enforced by branch protection).

## Where things live

| Area | Path |
|---|---|
| Recommender API (FastAPI) | `src/backend/` |
| OCR / menu upload API (FastAPI) | `src/upload-menu-backend/` |
| Frontend (React SPA) | `src/new-frontend/` |
| Database models & migrations | `src/db/` |
| Design/process docs | `docs/` |
| Weekly reports | `reports/` |

## Questions

If something in this file, [docs/development-process.md](docs/development-process.md), or [AGENTS.md](AGENTS.md) is out of date or unclear, open an issue or flag it in a PR — these are living documents and are expected to be kept current as the workflow evolves.
