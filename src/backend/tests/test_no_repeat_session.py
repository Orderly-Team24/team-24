"""Tests for the "Another option" no-repeat session (recommendation_session.py
wired into /display/recommendations).

Covers:
- A fresh call with no session_id creates one and returns it.
- Reusing that session_id never repeats a dish already shown, as long as
  unshown candidates remain.
- Once every candidate has been shown, the rotation resets instead of
  running out of options.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

MENU = [
    {"name": "Dish A", "price": 10, "ingredients": []},
    {"name": "Dish B", "price": 10, "ingredients": []},
    {"name": "Dish C", "price": 10, "ingredients": []},
]


def _recommend(session_id=None):
    body = {"message": "Recommend a dish", "menu": MENU}
    if session_id:
        body["session_id"] = session_id
    resp = client.post("/display/recommendations", json=body)
    assert resp.status_code == 200
    return resp.json()


def test_first_call_returns_a_session_id():
    data = _recommend()
    assert data["session_id"]
    assert data["recommendations"]


def test_session_never_repeats_a_shown_dish_until_pool_is_exhausted():
    first = _recommend()
    session_id = first["session_id"]
    shown_names = {first["recommendations"][0]["name"]}

    for _ in range(len(MENU) - 1):
        nxt = _recommend(session_id)
        name = nxt["recommendations"][0]["name"]
        assert name not in shown_names, "repeated a dish before the pool was exhausted"
        shown_names.add(name)

    assert shown_names == {dish["name"] for dish in MENU}


def test_session_rotation_resets_once_everything_has_been_shown():
    session_id = _recommend()["session_id"]
    for _ in range(len(MENU) - 1):
        session_id = _recommend(session_id)["session_id"]

    # Every dish in MENU has now been shown once — the next call must still
    # return a recommendation (from the reset rotation), not an empty list.
    again = _recommend(session_id)
    assert again["recommendations"]
    assert again["recommendations"][0]["name"] in {dish["name"] for dish in MENU}


def test_unknown_session_id_is_treated_as_a_fresh_session():
    data = _recommend(session_id="does-not-exist")
    assert data["recommendations"]
    assert data["session_id"] != "does-not-exist"
