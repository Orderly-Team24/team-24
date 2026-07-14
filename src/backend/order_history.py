"""Order history and dislikes, persisted via SQLAlchemy.

Backed by the `order_history` and `dislikes` tables (see `src/db/models.py`,
migrated in ADR-002). Same pattern as `auth.py`/`users.py`: callers pass in a
`Session` (via the `get_db` FastAPI dependency); there's no module-level
state, so the database is the single source of truth and survives restarts.

Per-dish shape (matches what the frontend already renders):

    {
        "id":          int,   # stable id derived from dish name
        "name":        str,
        "price":       float,
        "description": str,
        "ingredients": list[str],
        "reason":      str,
    }
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

from sqlalchemy.orm import Session

from models import Dislikes, OrderHistory

log = logging.getLogger("order_history")


def make_dish_id(dish: dict[str, Any]) -> int:
    """Deterministic 32-bit id derived from the dish name.

    The frontend renders a single recommended dish per request, so the name
    is stable across re-renders and we can use it as a natural key. When
    real menus land, this becomes a DB-side dish id.
    """
    name = (dish.get("name") or "").strip().lower()
    h = 0
    for ch in name:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    # Reserve 0 as "no id".
    return h or 1


def _sanitize_price(price_raw: Any) -> float:
    """Reject NaN/inf: they survive float() but break json.dumps downstream."""
    try:
        price = float(price_raw)
    except (TypeError, ValueError):
        return 0.0
    if price != price or price in (float("inf"), float("-inf")):  # NaN check
        return 0.0
    return price


def _serialize(row: OrderHistory) -> dict[str, Any]:
    """Return a JSON-safe dict with the canonical schema for one history row."""
    return {
        "id":          int(row.dish_id),
        "name":        row.dish_name or "",
        "price":       row.price or 0.0,
        "description": row.description or "",
        "ingredients": row.ingredients or [],
        "reason":      row.reason or "",
    }


def add_order(db: Session, user_id: int, dish: dict[str, Any]) -> dict[str, Any]:
    """Append a dish to the user's history.

    Same dish (by id) is allowed to appear multiple times — that's how
    "I ordered it 3 times" looks in real data.
    """
    if not user_id:
        raise ValueError("user_id is required")
    row = OrderHistory(
        user_id=user_id,
        dish_id=int(dish["id"]),
        dish_name=str(dish.get("name", "")),
        price=_sanitize_price(dish.get("price", 0)),
        description=str(dish.get("description", "")),
        ingredients=list(dish.get("ingredients", []) or []),
        reason=str(dish.get("reason", "")),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    log.info("Added dish id=%s name=%r for user=%s", row.dish_id, row.dish_name, user_id)
    return _serialize(row)


def get_history(db: Session, user_id: int) -> list[dict[str, Any]]:
    """Return the user's history, most recent first."""
    rows = (
        db.query(OrderHistory)
        .filter(OrderHistory.user_id == user_id)
        .order_by(OrderHistory.ordered_at.desc(), OrderHistory.id.desc())
        .all()
    )
    return [_serialize(r) for r in rows]


def has_ordered(db: Session, user_id: int, dish_id: int) -> bool:
    """True if ``dish_id`` is already in the user's history."""
    return (
        db.query(OrderHistory)
        .filter(OrderHistory.user_id == user_id, OrderHistory.dish_id == dish_id)
        .first()
        is not None
    )


def clear_history(db: Session, user_id: int) -> None:
    """Wipe a single user's history. Mostly useful for tests."""
    db.query(OrderHistory).filter(OrderHistory.user_id == user_id).delete()
    db.commit()


def add_dislike(db: Session, user_id: int, dish_id: int) -> None:
    """Mark a dish as disliked for the user. Idempotent — checked before insert."""
    if not user_id:
        raise ValueError("user_id is required")
    exists = (
        db.query(Dislikes)
        .filter(Dislikes.user_id == user_id, Dislikes.dish_id == dish_id)
        .first()
    )
    if exists is None:
        db.add(Dislikes(user_id=user_id, dish_id=dish_id))
        db.commit()
    log.info("Disliked dish id=%s for user=%s", dish_id, user_id)


def get_dislikes(db: Session, user_id: int) -> list[int]:
    """Return the user's disliked dish ids."""
    rows = db.query(Dislikes.dish_id).filter(Dislikes.user_id == user_id).all()
    return [r[0] for r in rows]


def reset_for_tests(db: Session) -> None:
    """Wipe both tables. For tests only."""
    db.query(OrderHistory).delete()
    db.query(Dislikes).delete()
    db.commit()
