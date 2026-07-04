from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from order_history import get_dislikes, make_dish_id
from recommendation_session import (
    get_session,
    get_remaining,
    mark_shown
)

router = APIRouter(prefix="/display", tags=["display"])


class AnotherOptionRequest(BaseModel):
    session_id: str

@router.post("/another-option")
def another_option(
    data: AnotherOptionRequest,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    session = get_session(data.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # US-015: skip dishes the user has disliked, same as /display/recommendations.
    user_id = (x_user_id or "").strip()
    disliked_ids = get_dislikes(user_id) if user_id else set()

    remaining = get_remaining(data.session_id, disliked_ids)

    if not remaining:
        return {
            "message": "No further recommendations available"
        }

    dish = remaining[0]

    mark_shown(
        data.session_id,
        dish["name"]
    )

    return {
    "recommendations": [
        {
            # Was hardcoded to 1 — broke dislike-by-id for cards shown via
            # "Another option" (frontend would always send dish_id=1).
            "id": make_dish_id(dish),
            "name": dish["name"],
            "price": dish["price"],
            "description": dish.get("description", ""),
            "ingredients": dish.get("ingredients", []),
            "reason": dish.get("reason", ""),
        }
    ]
}
