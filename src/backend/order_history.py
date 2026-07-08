"""Order history (stub).

Stores dishes a user has marked with "I'll order it again". No real DB yet
— we keep everything in process memory. When a real DB lands, only the
``_store`` helpers here need to change; the HTTP contract stays the same.

Per-dish shape (matches what the frontend already renders):

    {
        "id":          int,   # stable id derived from dish name
        "name":        str,
        "price":       float,
        "description": str,
        "ingredients": list[str],
        "reason":      str,
    }

Per-user history is a list of those dicts, ordered most-recent first.
"""

from __future__ import annotations

import logging
import threading
from typing import Any

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


# --- in-memory store ----------------------------------------------------
#
# user_id -> list[dish] (most recent first)
#
# Guarded by a lock so concurrent FastAPI workers can't lose writes.

_lock = threading.RLock()
_store: dict[str, list[dict[str, Any]]] = {}
_dislikes: dict[str, set[int]] = {}

# --- dislike store (in-memory) ------------------------------------------
#
# user_id -> set[dish_id]
#
_dislike_store: dict[str, set[int]] = {}


def _serialize(dish: dict[str, Any]) -> dict[str, Any]:
    """Return a JSON-safe copy of the dish with the canonical schema."""
    price_raw = dish.get("price", 0)
    # Reject NaN/inf: they survive float() but break json.dumps downstream.
    try:
        price = float(price_raw)
    except (TypeError, ValueError):
        price = 0.0
    if price != price or price in (float("inf"), float("-inf")):  # NaN check
        price = 0.0
    return {
        "id":          int(dish["id"]),
        "name":        str(dish.get("name", "")),
        "price":       price,
        "description": str(dish.get("description", "")),
        "ingredients": list(dish.get("ingredients", []) or []),
        "reason":      str(dish.get("reason", "")),
    }


def add_order(user_id: str, dish: dict[str, Any]) -> dict[str, Any]:
    """Append a dish to the user's history.

    Same dish (by id) is allowed to appear multiple times — that's how
    "I ordered it 3 times" looks in real data.
    """
    if not user_id:
        raise ValueError("user_id is required")
    serialized = _serialize(dish)
    with _lock:
        history = _store.setdefault(user_id, [])
        history.insert(0, serialized)  # most recent first
    log.info("Added dish id=%s name=%r for user=%s", serialized["id"], serialized["name"], user_id)
    return serialized


def get_history(user_id: str) -> list[dict[str, Any]]:
    """Return the user's history, most recent first."""
    with _lock:
        return list(_store.get(user_id, []))


def has_ordered(user_id: str, dish_id: int) -> bool:
    """True if ``dish_id`` is already in the user's history."""
    with _lock:
        return any(d["id"] == dish_id for d in _store.get(user_id, []))


def clear_history(user_id: str) -> None:
    """Wipe a single user's history. Mostly useful for tests."""
    with _lock:
        _store.pop(user_id, None)


def add_dislike(user_id: str, dish_id: int) -> None:
    """Mark a dish as disliked for the user. Idempotent — a set dedups."""
    if not user_id:
        raise ValueError("user_id is required")
    with _lock:
        _dislikes.setdefault(user_id, set()).add(dish_id)
    log.info("Disliked dish id=%s for user=%s", dish_id, user_id)


def get_dislikes(user_id: str) -> list[int]:
    """Return the user's disliked dish ids."""
    with _lock:
        return list(_dislikes.get(user_id, set()))


def reset_for_tests() -> None:
    """Wipe the whole in-memory store. For tests only."""
    with _lock:
        _store.clear()
        _dislikes.clear()
