# Quality Requirement Tests

Each quality requirement test (QRT) is automated and runs in CI.
Tests are stored in normal repository test locations and linked below.

---

## QRT-01 — AI Backend Failure Returns HTTP 503

**Linked QR:** [QR-01 – Fault Tolerance](quality-requirements.md#qr-01--fault-tolerance-reliability)

**Type:** Automated integration test

**Location:** [`src/backend/tests/test_ai_service.py`](../src/backend/tests/test_ai_service.py)

**What it tests:**
Mocks the OpenAI client to raise a connection error, then calls `POST /display/recommendations`.
Asserts that:
- The HTTP response status is **HTTP 503** (not 200, not 500)
- The response body contains a human-readable `detail` field (e.g. `"AI service unavailable"`)
- No stub recommendation is returned (returning unvalidated dishes is unsafe for users with allergens)

**CI:** Runs as part of `pytest src/backend/tests/` in the CI pipeline.

---

## QRT-02 — Recommendation Endpoint Responds Within 500 ms

**Linked QR:** [QR-02 – Response Time](quality-requirements.md#qr-02--response-time-performance-efficiency)

**Type:** Automated performance test (pytest + `time` module)

**Location:** [`src/backend/tests/test_response_time.py`](../src/backend/tests/test_response_time.py)

**What it tests:**
Sends a POST request to `/display/recommendations` with stub backend active.
Records wall-clock time before and after the call.
Asserts that elapsed time is less than 500 ms.

**CI:** Runs as part of `pytest src/backend/tests/` in the CI pipeline.
Uses `AI_BACKEND=stub` to avoid network I/O.

---

## QRT-03 — Invalid Inputs Are Rejected With Correct HTTP Status

**Linked QR:** [QR-03 – Input Validation](quality-requirements.md#qr-03--input-validation-security)

**Type:** Automated integration tests (pytest + HTTPX TestClient)

**Locations:**
- [`src/backend/tests/test_history_router.py`](../src/backend/tests/test_history_router.py) — blank dish name → HTTP 422, missing `X-User-Id` header → HTTP 400
- [`src/backend/tests/test_budget_filter.py`](../src/backend/tests/test_budget_filter.py) — negative budget filtered correctly

**What it tests:**
- POST `/history/orders` with `name: ""` → must return HTTP 422
- POST `/history/orders` without `X-User-Id` header → must return HTTP 400
- Budget filter with `max_budget=-5` → must return empty list (no crash)

**CI:** Runs as part of `pytest src/backend/tests/` in the CI pipeline.
