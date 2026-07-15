"""Order history HTTP endpoints (persisted storage, see order_history.py).

Routes:
- POST /history/orders               — record a dish into a user's history
- GET  /history/orders               — list a user's history
- GET  /history/orders/check         — whether a given dish is already in history
- POST /history/orders/{dish_id}/dislike — mark a dish as disliked
- GET  /history/dislikes             — list a user's disliked dish ids

No auth yet — `user_id` is passed as a header parameter so we can swap it
for a real session later without changing the URL shape. The header already
carries the real DB user id today (set at login/register — see AGENTS.md),
so it's parsed as an int before hitting the database.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from order_history import (
    add_dislike,
    add_order,
    get_dislikes,
    get_history,
    has_ordered,
    make_dish_id,
)

router = APIRouter(prefix="/history", tags=["history"])


def _user_id(x_user_id: str | None) -> tuple[str, int]:
    """Extract the X-User-Id header and parse it as the real numeric user id.

    Returns (raw string, parsed int) — the raw string is only used to echo
    back in responses.
    """
    uid = (x_user_id or "").strip()
    if not uid:
        raise HTTPException(status_code=400, detail="Missing X-User-Id header")
    try:
        return uid, int(uid)
    except ValueError:
        raise HTTPException(status_code=400, detail="X-User-Id must be a numeric user id") from None


class DishIn(BaseModel):
    """A dish coming in from the frontend (matches /display/recommendations)."""

    id: int | None = Field(default=None, description="Optional client id; backend will derive one if absent.")
    name: str
    price: float | None = None
    description: str | None = None
    ingredients: list[str] | None = None
    reason: str | None = None


class DishOut(BaseModel):
    """The dish shape we return — always has a real id."""

    id: int
    name: str
    price: float
    description: str
    ingredients: list[str]
    reason: str


class OrderResponse(BaseModel):
    status: str
    dish: DishOut


class HistoryResponse(BaseModel):
    user_id: str
    count: int
    history: list[DishOut]


class CheckResponse(BaseModel):
    user_id: str
    dish_id: int
    already_ordered: bool


@router.post("/orders", response_model=OrderResponse)
def post_order(
    dish: DishIn,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
):
    """Record a dish as ordered by the given user.

    Idempotency is *not* assumed — re-clicking the button will add the dish
    again (matches real life: "I ordered it twice").
    """
    _, user_id = _user_id(x_user_id)

    # A dish without a name can't be uniquely identified, so we'd lose it
    # in history (every blank-name dish would collapse onto id=1).
    if not (dish.name or "").strip():
        raise HTTPException(status_code=422, detail="Dish name is required")

    dish_dict = dish.model_dump()
    if not dish_dict.get("id"):
        dish_dict["id"] = make_dish_id(dish_dict)

    saved = add_order(db, user_id, dish_dict)
    return OrderResponse(status="saved", dish=DishOut(**saved))


@router.get("/orders", response_model=HistoryResponse)
def list_orders(
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
):
    """Return the user's full history, most recent first."""
    uid_str, user_id = _user_id(x_user_id)
    history = get_history(db, user_id)
    return HistoryResponse(
        user_id=uid_str,
        count=len(history),
        history=[DishOut(**d) for d in history],
    )


@router.get("/orders/check", response_model=CheckResponse)
def check_order(
    dish_id: int = Query(..., ge=1),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
):
    """Cheap endpoint the frontend can call to decide whether to show
    'I'll order it again' (not yet ordered) vs 'In your history ✓'."""
    uid_str, user_id = _user_id(x_user_id)
    return CheckResponse(
        user_id=uid_str,
        dish_id=dish_id,
        already_ordered=has_ordered(db, user_id, dish_id),
    )


class DislikeResponse(BaseModel):
    status: str
    dish_id: int


class DislikesResponse(BaseModel):
    user_id: str
    dislikes: list[int]


@router.post("/orders/{dish_id}/dislike", response_model=DislikeResponse)
def post_dislike(
    dish_id: int,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
):
    """Mark a dish as disliked so it's excluded from future recommendations."""
    _, user_id = _user_id(x_user_id)
    add_dislike(db, user_id, dish_id)
    return DislikeResponse(status="disliked", dish_id=dish_id)


@router.get("/dislikes", response_model=DislikesResponse)
def list_dislikes(
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
):
    """Return the user's disliked dish ids."""
    uid_str, user_id = _user_id(x_user_id)
    return DislikesResponse(user_id=uid_str, dislikes=get_dislikes(db, user_id))
