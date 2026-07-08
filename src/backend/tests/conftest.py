import os

# Tests never talk to a real Postgres instance — DATABASE_URL is a Render
# env var set in production (see ADR-002) and isn't meant to live in the repo.
# This placeholder just satisfies database.py's import-time os.environ[...]
# lookup for test modules that import `main`/`app` but don't touch the DB.
os.environ.setdefault("DATABASE_URL", "postgresql://fake/fake")

# Same idea for JWT_SECRET_KEY: auth.py/jwt_handler.py sign/verify tokens,
# tests just need any fixed value.
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-not-for-production")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base

# One shared in-memory engine for the whole test session. `app` is a single
# module-level object imported by every test file — if each file set its own
# dependency_overrides[get_db] with its own engine, whichever file pytest
# collects last would silently win for every other file's tests too.
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _fresh_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
