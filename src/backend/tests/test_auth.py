"""Tests for /auth/register and /auth/login.

Covers the root cause of issue #311 ("Order history is always empty"):
the frontend stores `data.user_id` from the login response into
localStorage and uses it as the X-User-Id for every subsequent request
(orders, dislikes, history). If /auth/login doesn't return `user_id`,
every user ends up sharing the same ("undefined") identity client-side.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def _register(email="test@example.com", username="testuser", password="hunter2"):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password,
            "preferences": {"allergies": [], "likes": [], "dislikes": []},
        },
    )


def test_login_response_includes_user_id_matching_registration():
    register_resp = _register()
    assert register_resp.status_code == 201
    registered_user_id = register_resp.json()["user_id"]

    login_resp = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "hunter2"},
    )
    assert login_resp.status_code == 200
    body = login_resp.json()

    assert "user_id" in body, (
        "login response is missing user_id — the frontend "
        "(LoginPage.jsx) stores this in localStorage and uses it as "
        "X-User-Id for orders/history/dislikes; without it every user "
        "shares the same identity client-side (issue #311)"
    )
    assert body["user_id"] == registered_user_id


def test_login_response_user_id_is_distinct_per_user():
    _register(email="a@example.com", username="userA", password="pw-a")
    _register(email="b@example.com", username="userB", password="pw-b")

    login_a = client.post("/auth/login", json={"email": "a@example.com", "password": "pw-a"})
    login_b = client.post("/auth/login", json={"email": "b@example.com", "password": "pw-b"})

    assert login_a.json()["user_id"] != login_b.json()["user_id"]
