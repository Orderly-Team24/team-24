"""Order history HTTP endpoints (stub storage).

Routes:
- POST /history/orders        — record a dish into a user's history
- GET  /history/orders        — list a user's history
- GET  /history/orders/check  — whether a given dish is already in history

No auth yet — `user_id` is passed as a query/header parameter so we can
swap it for a real session later without changing the URL shape.
"""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel, Field

from order_history import (
    add_dislike,
    add_order,
    get_dislikes,
    get_history,
    has_ordered,
    make_dish_id,
    reset_for_tests,
)

router = APIRouter(prefix="/history", tags=["history"])


def _user_id(x_user_id: str | None) -> str:
    """Extract a non-empty user id from the X-User-Id header."""
    uid = (x_user_id or "").strip()
    if not uid:
        raise HTTPException(status_code=400, detail="Missing X-User-Id header")
    return uid


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


class DislikeResponse(BaseModel):
    status: str
    dish_id: int


class DislikesListResponse(BaseModel):
    user_id: str
    dislikes: list[int]


@router.post("/orders", response_model=OrderResponse)
def post_order(
    dish: DishIn,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """Record a dish as ordered by the given user.

    Idempotency is *not* assumed — re-clicking the button will add the dish
    again (matches real life: "I ordered it twice").
    """
    user_id = _user_id(x_user_id)

    # A dish without a name can't be uniquely identified, so we'd lose it
    # in history (every blank-name dish would collapse onto id=1).
    if not (dish.name or "").strip():
        raise HTTPException(status_code=422, detail="Dish name is required")

    dish_dict = dish.model_dump()
    if not dish_dict.get("id"):
        dish_dict["id"] = make_dish_id(dish_dict)

    saved = add_order(user_id, dish_dict)
    return OrderResponse(status="saved", dish=DishOut(**saved))


@router.get("/orders", response_model=HistoryResponse)
def list_orders(
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """Return the user's full history, most recent first."""
    user_id = _user_id(x_user_id)
    history = get_history(user_id)
    return HistoryResponse(
        user_id=user_id,
        count=len(history),
        history=[DishOut(**d) for d in history],
    )


@router.get("/orders/check", response_model=CheckResponse)
def check_order(
    dish_id: int = Query(..., ge=1),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """Cheap endpoint the frontend can call to decide whether to show
    'I'll order it again' (not yet ordered) vs 'In your history ✓'."""
    user_id = _user_id(x_user_id)
    return CheckResponse(
        user_id=user_id,
        dish_id=dish_id,
        already_ordered=has_ordered(user_id, dish_id),
    )


@router.post("/orders/{dish_id}/dislike", response_model=DislikeResponse)
def dislike_dish(
    dish_id: int,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """Mark a dish as disliked for this user (US-015).

    Idempotent-ish: disliking twice just keeps it disliked (it's a set).
    Doesn't require the dish to be in the user's order history — a user
    might dislike something recommended but never actually ordered.
    """
    user_id = _user_id(x_user_id)
    add_dislike(user_id, dish_id)
    return DislikeResponse(status="disliked", dish_id=dish_id)


@router.get("/dislikes", response_model=DislikesListResponse)
def list_dislikes(
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    user_id = _user_id(x_user_id)
    return DislikesListResponse(user_id=user_id, dislikes=sorted(get_dislikes(user_id)))


# --- dev / test helpers -------------------------------------------------


@router.post("/_reset", include_in_schema=False)
def _reset_endpoint(
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """Wipe the in-memory store. No-op in production once a real DB lands."""
    reset_for_tests()
    return {"status": "reset"}