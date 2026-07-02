import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base, User

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


def test_without_user_id_returns_401():
    resp = client.delete("/users/me")
    assert resp.status_code == 401


def test_delete_nonexistent_user_return_404():
    resp = client.delete("/users/me", headers={"X-User-Id": "999"})
    assert resp.status_code == 404


def test_delete_existing_user_return_200():
    _create_user(user_id=1)

    resp = client.delete("/users/me", headers={"X-User-Id": "1"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "deleted"}

    db = TestingSessionLocal()
    assert db.query(User).filter(User.id == 1).first() is None
    db.close()
