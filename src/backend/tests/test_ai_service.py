"""QRT-01 — AI Backend Failure Returns HTTP 503 (QR-01: Fault Tolerance).

Verifies that when the configured AI backend raises an exception,
/display/recommendations returns HTTP 503 with a human-readable detail message,
and does NOT return a stub recommendation (which would ignore allergens).
"""

from __future__ import annotations

import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from ai_service import AIServiceUnavailableError
from main import app

client = TestClient(app)


# --- /display/recommendations returns 503 when AI backend fails -------------


def test_endpoint_returns_503_on_connection_error():
    """QR-01 acceptance threshold: HTTP 503 when AI backend raises ConnectionError."""
    with patch("ai_service._openai_compatible", side_effect=ConnectionError("refused")):
        with patch.dict(os.environ, {"AI_BACKEND": "openai", "OPENAI_API_KEY": "fake"}):
            resp = client.post("/display/recommendations", json={"message": "anything"})
    assert resp.status_code == 503


def test_endpoint_returns_503_on_timeout():
    """HTTP 503 when AI backend raises TimeoutError."""
    with patch("ai_service._openai_compatible", side_effect=TimeoutError("timeout")):
        with patch.dict(os.environ, {"AI_BACKEND": "openai", "OPENAI_API_KEY": "fake"}):
            resp = client.post("/display/recommendations", json={"message": "anything"})
    assert resp.status_code == 503


def test_endpoint_returns_503_on_runtime_error():
    """HTTP 503 when AI backend raises a generic RuntimeError."""
    with patch("ai_service._openai_compatible", side_effect=RuntimeError("crashed")):
        with patch.dict(os.environ, {"AI_BACKEND": "openai", "OPENAI_API_KEY": "fake"}):
            resp = client.post("/display/recommendations", json={"message": "test"})
    assert resp.status_code == 503


def test_endpoint_503_has_human_readable_detail():
    """Response body must contain a human-readable 'detail' field on 503."""
    with patch("ai_service._openai_compatible", side_effect=ConnectionError("no route")):
        with patch.dict(os.environ, {"AI_BACKEND": "openai", "OPENAI_API_KEY": "fake"}):
            resp = client.post("/display/recommendations", json={"message": "anything"})
    body = resp.json()
    assert "detail" in body
    assert len(body["detail"]) > 0


def test_endpoint_does_not_return_stub_on_backend_failure():
    """Must NOT return recommendations when AI backend fails.

    Returning a stub dish is unsafe: it ignores allergens and preferences.
    """
    with patch("ai_service._openai_compatible", side_effect=ConnectionError("no route")):
        with patch.dict(os.environ, {"AI_BACKEND": "openai", "OPENAI_API_KEY": "fake"}):
            resp = client.post("/display/recommendations", json={"message": "anything"})
    assert resp.status_code != 200


# --- AIServiceUnavailableError is raised (not swallowed) --------------------


def test_ai_service_unavailable_error_raised_on_connection_error():
    """get_recommendation_struct must raise AIServiceUnavailableError, not return stub."""
    from ai_service import get_recommendation_struct

    with patch("ai_service._openai_compatible", side_effect=ConnectionError("refused")):
        with patch.dict(os.environ, {"AI_BACKEND": "openai", "OPENAI_API_KEY": "fake"}):
            with pytest.raises(AIServiceUnavailableError):
                get_recommendation_struct("test")


def test_ai_service_unavailable_error_raised_on_timeout():
    """TimeoutError from the backend must propagate as AIServiceUnavailableError."""
    from ai_service import get_recommendation_struct

    with patch("ai_service._openai_compatible", side_effect=TimeoutError("timed out")):
        with patch.dict(os.environ, {"AI_BACKEND": "openai", "OPENAI_API_KEY": "fake"}):
            with pytest.raises(AIServiceUnavailableError):
                get_recommendation_struct("test")
