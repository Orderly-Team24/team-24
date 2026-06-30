import pytest
from unittest.mock import MagicMock, patch
import os

os.environ.setdefault("DATABASE_URL", "postgresql://fake/fake")

from fastapi.testclient import TestClient
from main import app
from database import get_db

def override_get_db():
    yield MagicMock()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_without_user_id_returns_401():
    resp = client.delete("/users/me")
    assert resp.status_code==401

def test_delete_nonexistent_user_return_404():
    resp = client.delete("/users/me", headers={"X-User-Id": "999"})
    assert resp.status_code==404

def test_delete_existing_user_return_200():
    # TODO: заменить мок на реального пользователя когда будет JWT
    resp = client.delete("/users/me", headers={"X-User-Id", "1"})
    assert resp.status_code==200
    assert resp.json() == {"status": "deleted"}

    