"""QRT-02 — Recommendation Endpoint Responds Within 500 ms (QR-02: Time Behaviour).

Verifies that /display/recommendations responds within 500 ms under
single-user stub load (no concurrent requests, no network I/O).
"""

from __future__ import annotations

import os
import time
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)

THRESHOLD_MS = 500
THRESHOLD_S = THRESHOLD_MS / 1000


def _elapsed_ms(start: float) -> float:
    return (time.perf_counter() - start) * 1000


# --- response time under stub backend --------------------------------------


def test_response_time_within_threshold():
    """p1 (single call): must complete within 500 ms with AI_BACKEND=stub."""
    with patch.dict(os.environ, {"AI_BACKEND": "stub"}):
        start = time.perf_counter()
        resp = client.post("/display/recommendations", json={"message": "test"})
        elapsed = _elapsed_ms(start)

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert elapsed < THRESHOLD_MS, (
        f"Response took {elapsed:.1f} ms, threshold is {THRESHOLD_MS} ms"
    )


def test_response_time_repeated_calls():
    """5 consecutive calls must each complete within 500 ms."""
    with patch.dict(os.environ, {"AI_BACKEND": "stub"}):
        for i in range(5):
            start = time.perf_counter()
            resp = client.post("/display/recommendations", json={"message": f"call-{i}"})
            elapsed = _elapsed_ms(start)
            assert resp.status_code == 200
            assert elapsed < THRESHOLD_MS, (
                f"Call {i} took {elapsed:.1f} ms, threshold is {THRESHOLD_MS} ms"
            )


def test_response_time_with_budget_filter():
    """Budget-filter path must also respond within 500 ms."""
    with patch.dict(os.environ, {"AI_BACKEND": "stub"}):
        start = time.perf_counter()
        resp = client.post(
            "/display/recommendations",
            json={"message": "test", "preferences": {"max_budget": 20}},
        )
        elapsed = _elapsed_ms(start)

    assert resp.status_code == 200
    assert elapsed < THRESHOLD_MS, (
        f"Budget-filter response took {elapsed:.1f} ms, threshold is {THRESHOLD_MS} ms"
    )


def test_response_time_p95_estimate():
    """Rough p95 estimate: 20 calls, at most 1 may exceed threshold."""
    n = 20
    over_threshold = 0
    with patch.dict(os.environ, {"AI_BACKEND": "stub"}):
        for i in range(n):
            start = time.perf_counter()
            resp = client.post("/display/recommendations", json={"message": f"msg-{i}"})
            elapsed = _elapsed_ms(start)
            assert resp.status_code == 200
            if elapsed >= THRESHOLD_MS:
                over_threshold += 1

    assert over_threshold <= 1, (
        f"{over_threshold}/{n} calls exceeded {THRESHOLD_MS} ms (p95 threshold allows ≤1)"
    )
