# ADR-003: Use OpenAI API for dish recommendations

**Date:** 2026-06-15  
**Status:** Accepted

## Context

The core product feature is recommending a dish from a restaurant menu based on user preferences, allergies, and budget. The team evaluated three approaches:
1. A rule-based filter that picks the highest-scoring dish by matching keywords
2. A locally hosted LLM (LM Studio) for development, OpenAI for production
3. OpenAI API directly, with a stub fallback for development and testing

A rule-based approach cannot generate natural-language reasons for recommendations, which is a key part of the user experience. A locally hosted LLM would require GPU infrastructure not available on Render's free tier.

## Decision

Use the OpenAI API (`gpt-4o-mini` or equivalent) as the production AI backend. Implement a configurable backend via the `AI_BACKEND` environment variable:
- `AI_BACKEND=stub` (default) — returns a dish from an in-memory pool; used in local development and CI tests without requiring an API key
- `AI_BACKEND=openai` — calls the OpenAI API; used in production on Render

The `OPENAI_API_KEY` and `OPENAI_BASE_URL` are stored as Render environment variables and never committed to the repository.

## Consequences

**Positive:**
- Natural-language recommendation reasons improve the user experience significantly.
- The stub backend makes CI and local development possible without an API key or network access.
- `AI_BACKEND` can be switched without code changes, making it easy to test different providers.
- OpenAI API is reliable and well-documented, reducing integration risk.

**Negative:**
- The recommendation endpoint has an external network dependency on OpenAI. If OpenAI is slow or unavailable, the endpoint returns 503.
- API usage incurs cost. For a course project on a free tier, this is managed by using a low-cost model and limiting request frequency.
- Response latency from OpenAI (typically 1–3 seconds) is the dominant latency factor in the recommendation flow.
- The stub backend returns fixed responses that may not fully represent production AI behavior in tests.

## Quality requirements addressed

- **QR-001 – Functional Correctness:** AI-generated recommendations are contextually appropriate and preference-aware.
- **QR-002 – Fault Tolerance:** the stub fallback and 503 error handling ensure the service degrades gracefully when OpenAI is unavailable.
- **QR-005 – Response Time:** the known latency of OpenAI calls is documented so the team can set appropriate user-facing expectations (loading states, timeouts).
