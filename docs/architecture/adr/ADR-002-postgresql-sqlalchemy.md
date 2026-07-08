# ADR-002: Use PostgreSQL with SQLAlchemy and Alembic

**Date:** 2026-06-29  
**Status:** Accepted

## Context

Prior to Sprint 3, all user data (order history) was stored in process memory (`dict` in `order_history.py`). This meant all data was lost on every service restart. User registration, preferences, order history, and token storage all require persistent, structured storage. The team needed to choose a persistence solution compatible with the existing FastAPI stack and deployable on Render's free tier.

## Decision

Use PostgreSQL as the relational database, SQLAlchemy 2.0 as the ORM, and Alembic for schema migrations.

- PostgreSQL instance provisioned on Render (free tier, same region as the Recommender service)
- SQLAlchemy models defined in `src/db/models.py` (five tables: `users`, `preferences`, `refresh_tokens`, `order_history`, `dislikes`)
- Database session management in `src/db/database.py` using `get_db()` FastAPI dependency
- Alembic migration in `src/db/alembic/versions/` creates all tables on `alembic upgrade head`
- `DATABASE_URL` stored as a Render environment variable, never committed to the repository

## Consequences

**Positive:**
- Data persists across service restarts and redeployments.
- SQLAlchemy provides type-safe model definitions and protects against SQL injection.
- Alembic migration history makes schema changes reviewable, reversible, and auditable.
- `CASCADE` delete rules on foreign keys ensure that deleting a user removes all their associated data automatically.
- PostgreSQL on Render's internal network is not publicly accessible, reducing the attack surface.

**Negative:**
- `DATABASE_URL` must be manually set in Render's environment after any database reset or recreation.
- Alembic migrations must be run manually from `src/db/` after schema changes — this is not yet automated in CI.
- The `src/db/` module is not co-located with `src/backend/`, requiring `sys.path` manipulation in modules that import from it.
- Render's free-tier PostgreSQL has storage and connection limits that may require upgrading if the user base grows.

## Quality requirements addressed

- **QR-001 – Functional Correctness:** persistent storage ensures user data is not silently lost between sessions.
- **QR-003 – Maintainability:** migration history and ORM models make the schema easy to evolve and review.
- **QR-004 – Security:** credentials are stored as environment variables; the database is on an internal network.
