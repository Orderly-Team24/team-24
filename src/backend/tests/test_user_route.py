import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base, Preferences, User
from jwt_handler import create_access_token

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def _fresh_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


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


def test_get_preferences_without_token_returns_401():
    resp = client.get("/users/me/preferences")
    assert resp.status_code == 401


def test_get_preferences_returns_404_when_missing():
    _create_user(user_id=1)
    resp = client.get("/users/me/preferences", headers=_auth_header(user_id=1))
    assert resp.status_code == 404


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
