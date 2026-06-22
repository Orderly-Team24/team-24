from fastapi import APIRouter
from pydantic import BaseModel, Field

from ai_service import FALLBACK_POOL, get_recommendation_struct, pick_from_pool
from budget_filter import filter_by_budget

router = APIRouter(prefix="/display", tags=["display"])


class Preferences(BaseModel):
    """User preferences for the recommender.

    All fields are optional — an empty `Preferences` means "no constraints",
    which keeps backward compatibility with the original `message`-only API.
    """

    cuisine: str | None = None
    exclude_ingredients: list[str] | None = None
    favorite_ingredients: list[str] | None = None
    max_budget: float | None = Field(default=None, ge=0)


class RecommendationRequest(BaseModel):
    message: str = ""
    preferences: Preferences | None = None


@router.post("/recommendations")
def display_recommendations(data: RecommendationRequest):
    """
    Return a single recommendation formatted for the frontend card UI.

    Frontend expects:
        { recommendations: [{ id, name, price, description, ingredients, reason }] }

    When `preferences.max_budget` is set, only dishes with
    `price <= max_budget` are considered. If none fit, returns 200 with
    `recommendations: []`.
    """
    prefs = data.preferences

    # Budget filter: pull from the stub pool exposed by `ai_service`.
    # (When US-004-4 lands, this becomes `parser.parse_menu(...)` output.)
    candidates = FALLBACK_POOL
    if prefs is not None and prefs.max_budget is not None:
        candidates = filter_by_budget(FALLBACK_POOL, prefs.max_budget)
        if not candidates:
            return {"recommendations": []}

    # Pick deterministically from the (possibly filtered) pool. If a budget
    # filter was applied we must use the filtered pool; otherwise fall
    # through to the AI backend (which may itself fall back to the stub).
    if prefs is not None and prefs.max_budget is not None:
        pick = pick_from_pool(candidates, data.message)
    else:
        pick = get_recommendation_struct(data.message)

    return {
        "recommendations": [
            {
                "id": 1,
                "name": pick["name"],
                "price": pick["price"],
                "description": pick["description"],
                "ingredients": pick["ingredients"],
                "reason": pick["reason"],
            }
        ]
    }