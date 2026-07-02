import os

# Tests never talk to a real Postgres instance — DATABASE_URL is a Render
# env var set in production (see ADR-002) and isn't meant to live in the repo.
# This placeholder just satisfies database.py's import-time os.environ[...]
# lookup for test modules that import `main`/`app` but don't touch the DB;
# test_user_route.py overrides get_db with a real SQLite session regardless.
os.environ.setdefault("DATABASE_URL", "postgresql://fake/fake")
