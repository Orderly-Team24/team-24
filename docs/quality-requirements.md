# Quality Requirements

Quality requirements are defined using ISO/IEC 25010 quality sub-characteristics and measurable scenario format.

Each requirement has a stable ID, a linked quality requirement test (QRT), and a rationale.

---

## QR-01 — Fault Tolerance (Reliability)

**ISO/IEC 25010 sub-characteristic:** Reliability – Fault tolerance

**Scenario:**
When the AI backend (OpenAI or LM Studio) is unavailable or returns an error,
the `/display/recommendations` endpoint must return HTTP 503 with a human-readable error message
within 3 seconds, without crashing or returning an unhandled 500.

**Rationale:**
The AI backend runs on an external service that can be rate-limited, timed out, or unreachable.
Returning a stub recommendation in this case is unsafe: the stub ignores user preferences and allergens,
and could recommend a dish that harms a user (e.g. a nut dish to someone with a nut allergy).
A clear 503 error is the correct behavior — it tells the client the service is temporarily unavailable
and prevents unsafe recommendations from being shown.

**Acceptance threshold:** 100% of requests must return HTTP 503 (not 500, not 200) when the AI backend is mocked as unavailable.

**Linked QRT:** [QRT-01](quality-requirement-tests.md#qrt-01)

**Related ADRs:** [ADR-003](architecture/adr/ADR-003-openai-integration.md) (the stub fallback and 503 handling this requirement describes is a direct consequence of depending on the OpenAI API) and [ADR-001](architecture/adr/ADR-001-split-backend-services.md) (splitting OCR into its own service means an OCR outage can't take the recommender down with it).

---

## QR-02 — Response Time (Performance Efficiency)

**ISO/IEC 25010 sub-characteristic:** Performance efficiency – Time behaviour

**Scenario:**
When a user submits a recommendation request with preferences and budget,
the `/display/recommendations` endpoint (using the stub backend) must return a response
within 500 ms under normal single-user load (no concurrent requests).

**Rationale:**
A slow recommendation response breaks the user experience and makes the product feel unreliable.
The stub backend is deterministic and has no I/O dependencies, so any latency above 500 ms
indicates an internal bottleneck in filtering or routing logic.

**Acceptance threshold:** p95 response time ≤ 500 ms in CI (stub backend, single-process Uvicorn).

**Linked QRT:** [QRT-02](quality-requirement-tests.md#qrt-02)

**Related ADR:** [ADR-003](architecture/adr/ADR-003-openai-integration.md) — the 1-3s OpenAI latency is the dominant cost in production; this requirement's 500ms budget is specifically scoped to the stub backend so CI can measure internal filtering/routing overhead in isolation from that external dependency.

---

## QR-03 — Input Validation (Security)

**ISO/IEC 25010 sub-characteristic:** Security – Input validation

**Scenario:**
When a client sends a request to `/display/recommendations` or `/history/orders`
with invalid input (blank dish name, negative budget, or missing required header),
the API must reject the request with HTTP 422 or HTTP 400
and must not persist or process the invalid data.

**Rationale:**
Invalid inputs can corrupt the persisted order history (e.g. all unnamed dishes colliding on the same ID)
or produce nonsensical recommendations (e.g. negative budget).
This was already observed during development: blank names caused ID collisions on `id=1`.

**Acceptance threshold:** 100% of invalid input cases must be rejected with the correct HTTP status code.

**Linked QRT:** [QRT-03](quality-requirement-tests.md#qrt-03)

**Related ADR:** [ADR-002](architecture/adr/ADR-002-postgresql-sqlalchemy.md) — this requirement covers request-level validation (Pydantic models rejecting malformed input with 422/400); ADR-002's move to SQLAlchemy adds a second layer underneath it, using parameterized queries instead of hand-built SQL so malformed/malicious input can't reach the database as raw strings.

---

> **Note:** the ADRs' own "Quality requirements addressed" sections reference `QR-001`–`QR-005`, an earlier numbering that doesn't match the `QR-01`–`QR-03` IDs defined in this file (some, like `QR-001` "Functional Correctness" and `QR-003` "Maintainability", don't correspond to any requirement documented here at all). The links above map by the actual scenario each QR describes, not by number. Reconciling the two numbering schemes — either by renumbering the ADRs or by documenting the missing requirements — is tracked as follow-up work, not done in this pass.
