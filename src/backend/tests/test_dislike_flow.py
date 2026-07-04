"""Tests for US-015: disliking dishes and having them excluded from recs.

Covers:
- AC 1: POST /history/orders/{dish_id}/dislike returns 200 and marks disliked.
- AC 2: GET /history/dislikes returns the list of disliked dish ids.
- AC 3: A disliked dish is never returned by /display/recommendations.
- AC 4: Disliking the currently recommended dish excludes it from the next
        /display/another-option call.
- Backward compat: anonymous callers (no X-User-Id) are unaffected.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from main import app
from order_history import make_dish_id, reset_for_tests
from recommendation_session import create_session

client = TestClient(app)


@pytest.fixture(autouse=True)
def _wipe():
    reset_for_tests()
    yield
    reset_for_tests()


HEADERS = {"X-User-Id": "dasha"}

MENU = [
    {"name": "Chicken pho", "price": 12.5, "description": "soup", "ingredients": ["chicken"], "reason": "r"},
    {"name": "Margherita pizza", "price": 13.0, "description": "pizza", "ingredients": ["cheese"], "reason": "r"},
]


def _dish_id(name: str) -> int:
    return make_dish_id({"name": name})


# --- POST /history/orders/{dish_id}/dislike -----------------------------


def test_dislike_returns_200_and_marks_dish():
    dish_id = _dish_id("Chicken pho")
    resp = client.post(f"/history/orders/{dish_id}/dislike", headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json() == {"status": "disliked", "dish_id": dish_id}


def test_dislike_requires_user_id():
    resp = client.post("/history/orders/123/dislike")
    assert resp.status_code == 400


def test_dislike_twice_is_idempotent():
    dish_id = _dish_id("Chicken pho")
    client.post(f"/history/orders/{dish_id}/dislike", headers=HEADERS)
    resp = client.post(f"/history/orders/{dish_id}/dislike", headers=HEADERS)
    assert resp.status_code == 200
    dislikes = client.get("/history/dislikes", headers=HEADERS).json()["dislikes"]
    assert dislikes.count(dish_id) == 1


# --- GET /history/dislikes ------------------------------------------------


def test_get_dislikes_empty_for_new_user():
    resp = client.get("/history/dislikes", headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["dislikes"] == []


def test_get_dislikes_returns_disliked_ids():
    dish_id = _dish_id("Chicken pho")
    client.post(f"/history/orders/{dish_id}/dislike", headers=HEADERS)
    resp = client.get("/history/dislikes", headers=HEADERS)
    assert dish_id in resp.json()["dislikes"]


def test_dislikes_are_per_user():
    dish_id = _dish_id("Pizza")
    client.post(f"/history/orders/{dish_id}/dislike", headers={"X-User-Id": "alice"})
    resp = client.get("/history/dislikes", headers={"X-User-Id": "bob"})
    assert resp.json()["dislikes"] == []


def test_get_dislikes_requires_user_id():
    resp = client.get("/history/dislikes")
    assert resp.status_code == 400


# --- /display/recommendations excludes disliked dishes --------------------


def test_recommendations_excludes_disliked_dish():
    pho_id = _dish_id("Chicken pho")
    client.post(f"/history/orders/{pho_id}/dislike", headers=HEADERS)

    resp = client.post(
        "/display/recommendations",
        json={"message": "", "menu": MENU},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    rec = resp.json()["recommendations"][0]
    assert rec["id"] != pho_id
    assert rec["name"] != "Chicken pho"


def test_recommendations_empty_when_all_candidates_disliked():
    for dish in MENU:
        client.post(f"/history/orders/{make_dish_id(dish)}/dislike", headers=HEADERS)

    resp = client.post(
        "/display/recommendations",
        json={"message": "", "menu": MENU},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    assert resp.json() == {"recommendations": []}


def test_recommendations_without_user_id_ignores_dislikes():
    """Anonymous callers (no X-User-Id) get unfiltered results — no 400, no crash."""
    pho_id = _dish_id("Chicken pho")
    client.post(f"/history/orders/{pho_id}/dislike", headers=HEADERS)

    resp = client.post("/display/recommendations", json={"message": "", "menu": MENU})
    assert resp.status_code == 200
    assert len(resp.json()["recommendations"]) == 1


# --- /display/another-option excludes disliked dishes (AC 4) --------------


def test_another_option_excludes_disliked_dish():
    session_id = create_session(MENU)
    pho_id = _dish_id("Chicken pho")
    client.post(f"/history/orders/{pho_id}/dislike", headers=HEADERS)

    resp = client.post(
        "/display/another-option",
        json={"session_id": session_id},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    rec = resp.json()["recommendations"][0]
    assert rec["name"] != "Chicken pho"
    assert rec["id"] == make_dish_id({"name": rec["name"]})


def test_another_option_message_when_all_remaining_disliked():
    session_id = create_session(MENU)
    for dish in MENU:
        client.post(f"/history/orders/{make_dish_id(dish)}/dislike", headers=HEADERS)

    resp = client.post(
        "/display/another-option",
        json={"session_id": session_id},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_another_option_without_user_id_ignores_dislikes():
    session_id = create_session(MENU)
    pho_id = _dish_id("Chicken pho")
    client.post(f"/history/orders/{pho_id}/dislike", headers=HEADERS)

    resp = client.post("/display/another-option", json={"session_id": session_id})
    assert resp.status_code == 200
    assert "recommendations" in resp.json()
