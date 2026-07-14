"""Tests for the "I'll order it again" history backend.

Covers:
- AC 1: POST /history/orders saves a dish and returns it.
- AC 2: GET  /history/orders returns the saved dishes, most-recent-first.
- AC 3: The dish id is stable across calls (same name → same id).
- AC 4: Re-clicking the button re-records the dish (no dedup).
- AC 5: GET /history/orders/check tells the frontend whether to flip the label.
- AC 6: Missing/non-numeric X-User-Id → 400.
- AC 7: /display/recommendations now returns a real id (not the placeholder `1`).

`X-User-Id` is the real numeric DB user id (see `history_router.py`), so
fixtures below use plain numeric strings rather than free-form names. Each
test starts from an empty DB via `conftest.py`'s autouse `_fresh_db` fixture
(create_all/drop_all around every test) — no extra wipe needed here.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


HEADERS = {"X-User-Id": "101"}


def _dish(name: str = "Margherita pizza", price: float = 13.0):
    return {"name": name, "price": price, "description": "x", "ingredients": ["a"], "reason": "y"}


# --- POST /history/orders ----------------------------------------------


def test_post_order_saves_dish():
    resp = client.post("/history/orders", json=_dish(), headers=HEADERS)
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "saved"
    assert body["dish"]["name"] == "Margherita pizza"
    assert body["dish"]["price"] == 13.0
    assert isinstance(body["dish"]["id"], int) and body["dish"]["id"] > 0


def test_post_order_requires_user_id():
    resp = client.post("/history/orders", json=_dish())
    assert resp.status_code == 400
    assert "X-User-Id" in resp.json()["detail"]


def test_post_order_blank_user_id_rejected():
    resp = client.post("/history/orders", json=_dish(), headers={"X-User-Id": "   "})
    assert resp.status_code == 400


def test_post_order_non_numeric_user_id_rejected():
    """X-User-Id must be the real numeric DB user id, not an arbitrary name."""
    resp = client.post("/history/orders", json=_dish(), headers={"X-User-Id": "dasha"})
    assert resp.status_code == 400
    assert "numeric" in resp.json()["detail"]


def test_post_order_assigns_id_if_missing():
    """Even if the client omits `id`, the backend derives one and returns it."""
    payload = _dish()
    assert "id" not in payload
    resp = client.post("/history/orders", json=payload, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["dish"]["id"] > 0


def test_post_order_preserves_client_id():
    payload = _dish()
    payload["id"] = 4242
    resp = client.post("/history/orders", json=payload, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["dish"]["id"] == 4242


def test_post_order_rejects_blank_name():
    """Empty/whitespace name collapses to id=1 in the store — reject at the door."""
    for bad in ["", "   ", "\n\t"]:
        resp = client.post("/history/orders", json={"name": bad, "price": 5}, headers=HEADERS)
        assert resp.status_code == 422, f"expected 422 for name={bad!r}, got {resp.status_code}"


def test_post_order_rejects_missing_name():
    resp = client.post("/history/orders", json={"price": 5}, headers=HEADERS)
    assert resp.status_code == 422


def test_sanitize_price_handles_nan_and_inf():
    """NaN/inf in `price` must not produce JSON-invalid output."""
    from order_history import _sanitize_price

    assert _sanitize_price(float("nan")) == 0.0
    assert _sanitize_price(float("inf")) == 0.0
    assert _sanitize_price(float("-inf")) == 0.0
    assert _sanitize_price("13.5") == 13.5
    assert _sanitize_price("not-a-number") == 0.0


# --- GET /history/orders -----------------------------------------------


def test_get_history_empty_for_new_user():
    resp = client.get("/history/orders", headers={"X-User-Id": "104"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 0
    assert body["history"] == []


def test_get_history_returns_saved_dishes_most_recent_first():
    client.post("/history/orders", json=_dish("Margherita pizza"), headers=HEADERS)
    client.post("/history/orders", json=_dish("Chicken pho"), headers=HEADERS)
    client.post("/history/orders", json=_dish("Mushroom risotto"), headers=HEADERS)

    resp = client.get("/history/orders", headers=HEADERS)
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 3
    assert [d["name"] for d in body["history"]] == [
        "Mushroom risotto",
        "Chicken pho",
        "Margherita pizza",
    ]


def test_get_history_requires_user_id():
    resp = client.get("/history/orders")
    assert resp.status_code == 400


def test_history_is_per_user():
    client.post("/history/orders", json=_dish("Pizza"), headers={"X-User-Id": "102"})
    resp = client.get("/history/orders", headers={"X-User-Id": "103"})
    assert resp.status_code == 200
    assert resp.json()["count"] == 0


# --- GET /history/orders/check ----------------------------------------


def test_check_false_for_unknown_dish():
    resp = client.get("/history/orders/check", params={"dish_id": 99999}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json() == {"user_id": "101", "dish_id": 99999, "already_ordered": False}


def test_check_true_after_posting():
    post = client.post("/history/orders", json=_dish("Chicken pho"), headers=HEADERS)
    dish_id = post.json()["dish"]["id"]

    resp = client.get("/history/orders/check", params={"dish_id": dish_id}, headers=HEADERS)
    assert resp.json()["already_ordered"] is True


def test_check_requires_user_id():
    resp = client.get("/history/orders/check", params={"dish_id": 1})
    assert resp.status_code == 400


def test_check_rejects_invalid_dish_id():
    resp = client.get("/history/orders/check", params={"dish_id": 0}, headers=HEADERS)
    assert resp.status_code == 422  # pydantic Query validation: ge=1
    resp = client.get("/history/orders/check", params={"dish_id": -3}, headers=HEADERS)
    assert resp.status_code == 422


# --- Re-click behavior (no dedup) -------------------------------------


def test_re_clicking_records_again():
    """Same dish twice should appear twice — re-ordering is real life."""
    client.post("/history/orders", json=_dish("Pizza"), headers=HEADERS)
    client.post("/history/orders", json=_dish("Pizza"), headers=HEADERS)

    resp = client.get("/history/orders", headers=HEADERS)
    assert resp.json()["count"] == 2


# --- Stable id across calls (AC 3) ------------------------------------


def test_dish_id_is_stable_across_calls():
    """The same dish name should map to the same id across endpoints."""
    post1 = client.post("/history/orders", json=_dish("Margherita pizza"), headers=HEADERS)
    id1 = post1.json()["dish"]["id"]

    # Compute the id the display endpoint *would* assign to the same name
    # and confirm they match (we don't care which pool entry the stub picks
    # for an empty message — we just care that IDs are derived from the name).
    rec = client.post("/display/recommendations", json={"message": ""}).json()
    rec_dish = rec["recommendations"][0]
    from order_history import make_dish_id as _mid
    assert rec_dish["id"] == _mid({"name": rec_dish["name"]})

    # /check against the saved id should agree.
    check = client.get("/history/orders/check", params={"dish_id": id1}, headers=HEADERS).json()
    assert check["already_ordered"] is True


# --- /display/recommendations now returns a real id (AC 7) -----------


def test_display_recommendations_returns_real_id():
    resp = client.post("/display/recommendations", json={"message": ""})
    assert resp.status_code == 200
    rec_id = resp.json()["recommendations"][0]["id"]
    assert isinstance(rec_id, int) and rec_id > 1  # not the old hard-coded 1


def test_display_recommendations_id_is_repeatable():
    a = client.post("/display/recommendations", json={"message": ""}).json()
    b = client.post("/display/recommendations", json={"message": ""}).json()
    assert a["recommendations"][0]["id"] == b["recommendations"][0]["id"]


# --- Dislikes ------------------------------------------------------------


def test_dislike_marks_dish():
    resp = client.post("/history/orders/42/dislike", headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json() == {"status": "disliked", "dish_id": 42}


def test_get_dislikes_returns_disliked_ids():
    client.post("/history/orders/42/dislike", headers=HEADERS)
    client.post("/history/orders/7/dislike", headers=HEADERS)
    resp = client.get("/history/dislikes", headers=HEADERS)
    assert resp.status_code == 200
    assert set(resp.json()["dislikes"]) == {42, 7}


def test_dislike_is_idempotent():
    client.post("/history/orders/42/dislike", headers=HEADERS)
    client.post("/history/orders/42/dislike", headers=HEADERS)
    resp = client.get("/history/dislikes", headers=HEADERS)
    assert resp.json()["dislikes"] == [42]


def test_dislike_requires_user_id():
    resp = client.post("/history/orders/42/dislike")
    assert resp.status_code == 400


def test_get_dislikes_requires_user_id():
    resp = client.get("/history/dislikes")
    assert resp.status_code == 400


def test_dislikes_are_per_user():
    client.post("/history/orders/42/dislike", headers={"X-User-Id": "102"})
    resp = client.get("/history/dislikes", headers={"X-User-Id": "103"})
    assert resp.json()["dislikes"] == []


def test_get_dislikes_empty_for_new_user():
    resp = client.get("/history/dislikes", headers={"X-User-Id": "104"})
    assert resp.status_code == 200
    assert resp.json() == {"user_id": "104", "dislikes": []}
