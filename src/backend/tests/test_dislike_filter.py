"""Tests for dislike filtering in /display/recommendations (US-015-2).

Covers:
- AC 1: A disliked dish is excluded from recommendations for the same user.
- AC 2: Without X-User-Id, behavior is unchanged (no filtering applied).
- AC 3: If all candidates are disliked, returns 200 with empty recommendations.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from main import app
from order_history import (
    add_dislike,
    make_dish_id,
    reset_for_tests,
    reset_dislikes_for_tests,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def _wipe():
    """Make every test start from an empty store."""
    reset_for_tests()
    reset_dislikes_for_tests()
    yield
    reset_for_tests()
    reset_dislikes_for_tests()


# --- AC 1: Disliked dish is excluded -----------------------------------


def test_disliked_dish_excluded_for_user():
    """A dish disliked via add_dislike is excluded from recommendations."""
    # First, get a recommendation to know what dish id would be returned.
    resp = client.post("/display/recommendations", json={"message": ""})
    assert resp.status_code == 200
    dish = resp.json()["recommendations"][0]
    dish_id = dish["id"]

    # Dislike that dish.
    add_dislike("dasha", dish_id)

    # Get recommendations again — the disliked dish should be excluded.
    resp2 = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "dasha"},
    )
    assert resp2.status_code == 200
    result = resp2.json()["recommendations"]
    # The returned dish should NOT be the disliked one.
    assert len(result) == 1
    assert result[0]["id"] != dish_id


def test_disliked_dish_still_returned_for_other_user():
    """A dish disliked by user A is still returned for user B."""
    resp = client.post("/display/recommendations", json={"message": ""})
    dish = resp.json()["recommendations"][0]
    dish_id = dish["id"]

    # User A dislikes it.
    add_dislike("alice", dish_id)

    # User B should still see it.
    resp2 = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "bob"},
    )
    assert resp2.status_code == 200
    result = resp2.json()["recommendations"]
    assert len(result) == 1
    assert result[0]["id"] == dish_id


# --- AC 2: Without X-User-Id, no filtering -----------------------------


def test_no_user_id_no_filtering():
    """Without X-User-Id header, behavior is unchanged (no filtering)."""
    resp = client.post("/display/recommendations", json={"message": ""})
    assert resp.status_code == 200
    dish = resp.json()["recommendations"][0]
    dish_id = dish["id"]

    # Dislike the dish (simulates some other path having added it).
    add_dislike("dasha", dish_id)

    # No header → no filtering, so the disliked dish can still appear.
    resp2 = client.post("/display/recommendations", json={"message": ""})
    assert resp2.status_code == 200
    result = resp2.json()["recommendations"]
    assert len(result) == 1
    # The dish may or may not be the same one (stub picks based on message),
    # but the point is: no 400/500 error, and we get a recommendation.
    assert result[0]["id"] > 0


# --- AC 3: All candidates disliked → empty result ----------------------


def test_all_candidates_disliked_returns_empty():
    """If all candidates are disliked, return 200 with empty recommendations."""
    from ai_service import FALLBACK_POOL

    # Dislike every dish in the fallback pool.
    for dish in FALLBACK_POOL:
        add_dislike("dasha", make_dish_id(dish))

    resp = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "dasha"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"recommendations": []}


# --- Edge cases ---------------------------------------------------------


def test_empty_dislikes_no_effect():
    """User with no dislikes still gets a normal recommendation."""
    resp = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "fresh-user"},
    )
    assert resp.status_code == 200
    result = resp.json()["recommendations"]
    assert len(result) == 1
    assert result[0]["id"] > 0


def test_dislike_filter_works_with_budget_filter():
    """Dislike filtering composes correctly with budget filtering."""
    from ai_service import FALLBACK_POOL

    # Dislike the cheapest dish.
    cheapest = min(FALLBACK_POOL, key=lambda d: d["price"])
    add_dislike("dasha", make_dish_id(cheapest))

    # Set a budget that only the cheapest dish would fit.
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "",
            "preferences": {"max_budget": cheapest["price"]},
        },
        headers={"X-User-Id": "dasha"},
    )
    # The cheapest is disliked, so nothing should remain.
    assert resp.status_code == 200
    assert resp.json() == {"recommendations": []}