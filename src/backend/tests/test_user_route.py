from fastapi.testclient import TestClient

from main import app
from models import User
from jwt_handler import create_access_token
from .conftest import TestingSessionLocal

client = TestClient(app)


def _create_user(user_id=1, email="test@example.com", username="testuser"):
    db = TestingSessionLocal()
    db.add(User(id=user_id, email=email, username=username, hashed_password="hashed"))
    db.commit()
    db.close()


def _auth_header(user_id=1):
    return {"Authorization": f"Bearer {create_access_token(user_id)}"}


def test_delete_without_token_returns_401():
    resp = client.delete("/users/me")
    assert resp.status_code == 401


def test_delete_with_garbage_token_returns_401():
    resp = client.delete("/users/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401


def test_delete_for_nonexistent_user_returns_401():
    # A structurally valid token for a user that isn't in the DB (e.g. already
    # deleted) — can't be told apart from a forged token, so 401 either way.
    resp = client.delete("/users/me", headers=_auth_header(user_id=999))
    assert resp.status_code == 401


def test_delete_existing_user_return_200():
    _create_user(user_id=1)

    resp = client.delete("/users/me", headers=_auth_header(user_id=1))
    assert resp.status_code == 200
    assert resp.json() == {"status": "deleted"}

    db = TestingSessionLocal()
    assert db.query(User).filter(User.id == 1).first() is None
    db.close()
