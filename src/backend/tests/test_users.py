from fastapi.testclient import TestClient

from main import app
from models import Preferences, User
from jwt_handler import create_access_token
from .conftest import TestingSessionLocal

client = TestClient(app)


def _create_user(user_id=1, email="test@example.com", username="testuser"):
    db = TestingSessionLocal()
    db.add(User(id=user_id, email=email, username=username, hashed_password="hashed"))
    db.commit()
    db.close()


def _create_preferences(user_id=1, allergies=None, likes=None, dislikes=None):
    db = TestingSessionLocal()
    db.add(Preferences(
        user_id=user_id,
        allergies=allergies or [],
        likes=likes or [],
        dislikes=dislikes or [],
    ))
    db.commit()
    db.close()


def _auth_header(user_id=1):
    return {"Authorization": f"Bearer {create_access_token(user_id)}"}


def test_get_preferences_without_token_returns_401():
    resp = client.get("/users/me/preferences")
    assert resp.status_code == 401


def test_get_preferences_returns_saved_data():
    _create_user(user_id=1)
    _create_preferences(user_id=1, allergies=["nuts"], likes=["tomato"], dislikes=["onion"])

    resp = client.get("/users/me/preferences", headers=_auth_header(user_id=1))
    assert resp.status_code == 200
    assert resp.json() == {"allergies": ["nuts"], "likes": ["tomato"], "dislikes": ["onion"]}


def test_get_preferences_is_scoped_to_the_requesting_user():
    _create_user(user_id=1, email="a@example.com", username="a")
    _create_user(user_id=2, email="b@example.com", username="b")
    _create_preferences(user_id=1, allergies=["nuts"])
    _create_preferences(user_id=2, allergies=["shellfish"])

    resp = client.get("/users/me/preferences", headers=_auth_header(user_id=2))
    assert resp.json()["allergies"] == ["shellfish"]


def test_patch_preferences_without_token_returns_401():
    resp = client.patch("/users/me/preferences", json={"likes": ["tomato"]})
    assert resp.status_code == 401


def test_patch_preferences_updates_saved_data():
    _create_user(user_id=1)
    _create_preferences(user_id=1, allergies=["nuts"])

    resp = client.patch(
        "/users/me/preferences",
        headers=_auth_header(user_id=1),
        json={"allergies": ["gluten"], "likes": ["pasta"], "dislikes": ["mushroom"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"allergies": ["gluten"], "likes": ["pasta"], "dislikes": ["mushroom"]}

    resp = client.get("/users/me/preferences", headers=_auth_header(user_id=1))
    assert resp.json() == {"allergies": ["gluten"], "likes": ["pasta"], "dislikes": ["mushroom"]}


def test_patch_preferences_partial_body_only_updates_named_fields():
    _create_user(user_id=1)
    _create_preferences(user_id=1, allergies=["nuts"], likes=["tomato"], dislikes=["onion"])

    resp = client.patch(
        "/users/me/preferences",
        headers=_auth_header(user_id=1),
        json={"likes": ["pasta"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"allergies": ["nuts"], "likes": ["pasta"], "dislikes": ["onion"]}
