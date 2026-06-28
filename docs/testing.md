# Testing Strategy

## Overview

Orderly uses pytest for all automated testing across both backend services.
Tests are co-located with the service source code and run in CI on every push to `main` and on every pull request.

---

## Test Locations

| Service | Test directory |
|---------|---------------|
| Recommender backend | [`src/backend/tests/`](../src/backend/tests/) |
| Upload / OCR backend | [`src/upload-menu-backend/tests/`](../src/upload-menu-backend/tests/) |

---

## Critical Modules

The following modules contain core product logic and must each maintain at least **30% automated line coverage**.

| Module | Role | Test file |
|--------|------|-----------|
| `src/backend/budget_filter.py` | Filters dishes by max budget — safety-critical post-filter | [`tests/test_budget_filter.py`](../src/backend/tests/test_budget_filter.py) |
| `src/backend/order_history.py` | In-memory order history store — thread safety required | [`tests/test_history_router.py`](../src/backend/tests/test_history_router.py) |
| `src/backend/parser.py` | Parses OCR raw text into structured menu items | [`test_parser.py`](../src/backend/test_parser.py) |
| `src/upload-menu-backend/main.py` | File upload + Tesseract OCR endpoint | [`tests/test_upload.py`](../src/upload-menu-backend/tests/test_upload.py) |

---

## Unit Tests

Unit tests verify individual functions and modules in isolation.

- [`src/backend/tests/test_budget_filter.py`](../src/backend/tests/test_budget_filter.py) — pure function tests for budget filtering logic
- [`src/backend/test_parser.py`](../src/backend/test_parser.py) — regex-based menu parsing (price extraction, flagging unparseable items)
- [`src/backend/tests/test_history_router.py`](../src/backend/tests/test_history_router.py) — order history store: happy path, idempotency, blank-name rejection, missing header

## Integration Tests

Integration tests verify interactions between components using FastAPI's `TestClient`.

- [`src/backend/tests/test_budget_filter.py`](../src/backend/tests/test_budget_filter.py) — HTTP endpoint tests for `/display/recommendations` with budget param
- [`src/backend/tests/test_history_router.py`](../src/backend/tests/test_history_router.py) — full HTTP CRUD cycle for `/history/orders*`
- [`src/upload-menu-backend/tests/test_upload.py`](../src/upload-menu-backend/tests/test_upload.py) — file upload endpoint: format validation, size limits, OCR mock

## Quality Requirement Tests

See [`docs/quality-requirement-tests.md`](quality-requirement-tests.md) for automated QRTs linked to each quality requirement.

---

## Additional QA Check — Bandit (Security Static Analysis)

**Tool:** [Bandit](https://bandit.readthedocs.io/) — static security analysis for Python

**QA objective:** Detect common security vulnerabilities in Python source code (e.g. hardcoded credentials, unsafe use of `eval`, insecure subprocess calls, SQL injection patterns).

**Why this risk matters:**
Orderly's backends handle user-supplied file uploads, AI-generated text, and HTTP headers used as user IDs.
Without static security analysis, subtle vulnerabilities (e.g. path traversal in file upload, shell injection in OCR calls) could go undetected until exploitation.

**Where it runs:** CI pipeline — `bandit -r src/backend src/upload-menu-backend -ll` (medium and high severity only, to avoid noise from low-severity informational findings).

**Limitations:**
- Bandit does not replace a full security audit or penetration test.
- False positives are possible; findings are reviewed before blocking the build.
- Frontend (vanilla JS) is not covered — a separate JS security scan (e.g. `npm audit`) is deferred to a later sprint.

---

## Running Tests Locally

```bash
# Recommender backend
cd src/backend
pip install -r requirements.txt
pytest tests/ -v --tb=short

# Upload backend
cd src/upload-menu-backend
pip install -r requirements.txt
pytest tests/ -v --tb=short

# Coverage report (recommender backend)
cd src/backend
pytest tests/ --cov=. --cov-report=term-missing

# Security scan
pip install bandit
bandit -r src/backend src/upload-menu-backend -ll
```

---

## Coverage Expectations

- **Critical modules** (listed above): ≥ 30% line coverage each
- **Global repository coverage** may be lower — the frontend is vanilla JS with no automated test runner configured yet; coverage applies to Python backend modules only
- Coverage is measured and reported in CI on every push to `main`
