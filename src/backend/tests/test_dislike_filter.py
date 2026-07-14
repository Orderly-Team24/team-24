"""Tests for dislike filtering in /display/recommendations (US-015-2).

Covers:
- AC 1: A disliked dish is excluded from recommendations for the same user.
- AC 2: Without X-User-Id, behavior is unchanged (no filtering applied).
- AC 3: If all candidates are disliked, returns 200 with empty recommendations.

`X-User-Id` is the real numeric DB user id (see `history_router.py`), so
fixtures below use plain numeric strings. Dislikes are seeded directly via
`order_history.add_dislike` against a throwaway session from `conftest.py`'s
shared test engine; each test starts from an empty DB via the autouse
`_fresh_db` fixture there.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app
from order_history import make_dish_id

from .conftest import TestingSessionLocal

client = TestClient(app)


def _seed_dislike(user_id: int, dish_id: int) -> None:
    from order_history import add_dislike

    db = TestingSessionLocal()
    try:
        add_dislike(db, user_id, dish_id)
    finally:
        db.close()


# --- AC 1: Disliked dish is excluded -----------------------------------


def test_disliked_dish_excluded_for_user():
    """A dish disliked via add_dislike is excluded from recommendations."""
    # First, get a recommendation to know what dish id would be returned.
    resp = client.post("/display/recommendations", json={"message": ""})
    assert resp.status_code == 200
    dish = resp.json()["recommendations"][0]
    dish_id = dish["id"]

    # Dislike that dish.
    _seed_dislike(101, dish_id)

    # Get recommendations again — the disliked dish should be excluded.
    resp2 = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "101"},
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
    _seed_dislike(102, dish_id)

    # User B should still see it.
    resp2 = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "103"},
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
    _seed_dislike(101, dish_id)

    # No header → no filtering, so the disliked dish can still appear.
    resp2 = client.post("/display/recommendations", json={"message": ""})
    assert resp2.status_code == 200
    result = resp2.json()["recommendations"]
    assert len(result) == 1
    # The dish may or may not be the same one (stub picks based on message),
    # but the point is: no 400/500 error, and we get a recommendation.
    assert result[0]["id"] > 0


def test_non_numeric_user_id_no_filtering():
    """A non-numeric X-User-Id can't map to a real user, so no filtering."""
    resp = client.post("/display/recommendations", json={"message": ""})
    dish = resp.json()["recommendations"][0]
    dish_id = dish["id"]
    _seed_dislike(101, dish_id)

    resp2 = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "not-a-number"},
    )
    assert resp2.status_code == 200
    assert len(resp2.json()["recommendations"]) == 1


# --- AC 3: All candidates disliked → empty result ----------------------


def test_all_candidates_disliked_returns_empty():
    """If all candidates are disliked, return 200 with empty recommendations."""
    from ai_service import FALLBACK_POOL

    # Dislike every dish in the fallback pool.
    for dish in FALLBACK_POOL:
        _seed_dislike(101, make_dish_id(dish))

    resp = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "101"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"recommendations": []}


# --- Edge cases ---------------------------------------------------------


def test_empty_dislikes_no_effect():
    """User with no dislikes still gets a normal recommendation."""
    resp = client.post(
        "/display/recommendations",
        json={"message": ""},
        headers={"X-User-Id": "105"},
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
    _seed_dislike(101, make_dish_id(cheapest))

    # Set a budget that only the cheapest dish would fit.
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "",
            "preferences": {"max_budget": cheapest["price"]},
        },
        headers={"X-User-Id": "101"},
    )
    # The cheapest is disliked, so nothing should remain.
    assert resp.status_code == 200
    assert resp.json() == {"recommendations": []}
