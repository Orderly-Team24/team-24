"""Tests for US-001-1: budget filter.

Covers:
- AC 1: Preferences.max_budget field exists (Pydantic model accepts it).
- AC 2: backend filters candidates with price <= max_budget.
- AC 3: empty result returns 200 with recommendations: [] (no 500), warning logged.
- AC 4: max_budget=None or absent → no filtering.
"""

from __future__ import annotations

import logging

import pytest
from fastapi.testclient import TestClient

from budget_filter import filter_by_budget
from display_recommendations import Preferences, RecommendationRequest
from main import app

client = TestClient(app)


# --- pure-function tests (filter_by_budget) ----------------------------


def _dish(name: str, price):
    return {"name": name, "price": price, "description": "", "ingredients": [], "reason": ""}


def test_filter_none_budget_returns_all():
    dishes = [_dish("A", 5.0), _dish("B", 50.0), _dish("C", 100.0)]
    assert filter_by_budget(dishes, None) == dishes


def test_filter_zero_budget_returns_all():
    dishes = [_dish("A", 5.0)]
    assert filter_by_budget(dishes, 0) == dishes


def test_filter_negative_budget_returns_all():
    """A negative budget is nonsense; treat it like 'no filter'."""
    dishes = [_dish("A", 5.0)]
    assert filter_by_budget(dishes, -1) == dishes


def test_filter_drops_expensive():
    dishes = [_dish("A", 5.0), _dish("B", 50.0), _dish("C", 100.0)]
    out = filter_by_budget(dishes, 10.0)
    assert [d["name"] for d in out] == ["A"]


def test_filter_keeps_zero_priced():
    dishes = [_dish("Free", 0), _dish("A", 5.0)]
    out = filter_by_budget(dishes, 10.0)
    assert [d["name"] for d in out] == ["Free", "A"]


def test_filter_drops_dishes_without_price():
    """Dishes with price=None can't be evaluated, so they're excluded."""
    dishes = [_dish("Mystery", None), _dish("A", 5.0)]
    out = filter_by_budget(dishes, 10.0)
    assert [d["name"] for d in out] == ["A"]


def test_filter_empty_result_logs_warning(caplog):
    dishes = [_dish("A", 100.0)]
    with caplog.at_level(logging.WARNING, logger="budget_filter"):
        result = filter_by_budget(dishes, 10.0)
    assert result == []
    assert any("no dishes within budget" in r.message for r in caplog.records)


def test_filter_preserves_order():
    dishes = [_dish("C", 3.0), _dish("A", 1.0), _dish("B", 2.0)]
    out = filter_by_budget(dishes, 5.0)
    assert [d["name"] for d in out] == ["C", "A", "B"]


# --- Pydantic model tests (AC 1) ---------------------------------------


def test_preferences_has_max_budget_field():
    p = Preferences(max_budget=15.0)
    assert p.max_budget == 15.0


def test_preferences_max_budget_defaults_to_none():
    p = Preferences()
    assert p.max_budget is None


def test_preferences_max_budget_rejects_negative():
    """Field constraint `ge=0` should reject negative budgets at parse time."""
    with pytest.raises(Exception):
        Preferences(max_budget=-1)


def test_recommendation_request_accepts_preferences():
    r = RecommendationRequest(message="hi", preferences=Preferences(max_budget=10))
    assert r.preferences.max_budget == 10


def test_recommendation_request_backward_compat_no_preferences():
    """Legacy call with just `message` still works."""
    r = RecommendationRequest(message="hi")
    assert r.preferences is None
    assert r.message == "hi"


def test_preferences_has_dietary_preferences_field():
    p = Preferences(dietary_preferences="vegan, halal")
    assert p.dietary_preferences == "vegan, halal"


def test_preferences_dietary_preferences_defaults_to_none():
    p = Preferences()
    assert p.dietary_preferences is None


def test_recommendation_request_accepts_dietary_preferences():
    r = RecommendationRequest(
        message="hi",
        preferences=Preferences(dietary_preferences="gluten-free"),
    )
    assert r.preferences.dietary_preferences == "gluten-free"


def test_endpoint_accepts_dietary_preferences_without_filtering():
    """dietary_preferences is prompt-only — stub mode still returns a dish."""
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "anything",
            "preferences": {"dietary_preferences": "vegan"},
        },
    )
    assert resp.status_code == 200
    assert len(resp.json()["recommendations"]) == 1


# --- HTTP endpoint tests (AC 2, 3, 4) ----------------------------------


def test_endpoint_no_budget_returns_recommendation():
    resp = client.post("/display/recommendations", json={"message": "anything"})
    assert resp.status_code == 200
    body = resp.json()
    assert "recommendations" in body
    assert len(body["recommendations"]) == 1


def test_endpoint_budget_filters_expensive():
    """max_budget=10 should exclude every stub-pool dish (all > $10)."""
    resp = client.post(
        "/display/recommendations",
        json={"message": "x", "preferences": {"max_budget": 10}},
    )
    assert resp.status_code == 200
    # All stub dishes are > $10, so the result must be empty.
    assert resp.json() == {"recommendations": []}


def test_endpoint_budget_keeps_affordable():
    """max_budget=20 keeps all stub dishes (cheapest is $11, most expensive $18.50)."""
    resp = client.post(
        "/display/recommendations",
        json={"message": "x", "preferences": {"max_budget": 20}},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["recommendations"]) == 1
    assert body["recommendations"][0]["price"] <= 20


def test_endpoint_empty_budget_pool_returns_200_not_500(caplog):
    """AC 3: empty result is 200 with [], not 500."""
    with caplog.at_level(logging.WARNING):
        resp = client.post(
            "/display/recommendations",
            json={"message": "x", "preferences": {"max_budget": 1}},
        )
    assert resp.status_code == 200
    assert resp.json() == {"recommendations": []}
    # And we logged the warning somewhere (logger name may be 'budget_filter').
    warnings = [r for r in caplog.records if "no dishes within budget" in r.message]
    assert warnings, f"Expected a 'no dishes within budget' warning, got: {[r.message for r in caplog.records]}"


def test_endpoint_no_preferences_field_works():
    """Backward compat: request without `preferences` key still works."""
    resp = client.post("/display/recommendations", json={"message": ""})
    assert resp.status_code == 200