from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from recommendation_session import (
    get_session,
    get_remaining,
    mark_shown
)

router = APIRouter(prefix="/display", tags=["display"])


class AnotherOptionRequest(BaseModel):
    session_id: str

@router.post("/another-option")
def another_option(data: AnotherOptionRequest):
    session = get_session(data.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    remaining = get_remaining(data.session_id)

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
            "id": 1,
            "name": dish["name"],
            "price": dish["price"],
            "description": dish.get("description", ""),
            "ingredients": dish.get("ingredients", []),
            "reason": dish.get("reason", ""),
        }
    ]
}
