from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from recommendation_session import create_session, mark_shown

from ai_service import (
    AIServiceUnavailableError,
    FALLBACK_POOL,
    filter_fallback_pool_by_preferences,
    get_recommendation_struct,
    pick_from_pool,
)
from budget_filter import filter_by_budget
from order_history import make_dish_id

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
    menu: list[dict] = [] 
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

    
    candidates = data.menu if data.menu else FALLBACK_POOL

    
    if prefs is not None and prefs.max_budget is not None:
        candidates = filter_by_budget(candidates, prefs.max_budget)
        if not candidates:
            
            return {"recommendations": []}

    if prefs is not None:
        preferred_candidates = filter_fallback_pool_by_preferences(candidates, prefs)
        if preferred_candidates:
            candidates = preferred_candidates

    prefs_dict = prefs.model_dump() if prefs else None

    try:
        if prefs is not None and prefs.max_budget is not None:
            pick = pick_from_pool(candidates, data.message)
        else:
            pick = get_recommendation_struct(
                data.message,
                preferences=prefs_dict,
                menu=candidates,
            )
    except AIServiceUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again later.",
        ) from exc

    if not pick:
        return {"recommendations": []}

    dish = {
        "name": str(pick.get("name", "Chef's special")),
        "price": pick.get("price"),
        "description": str(pick.get("description", "")),
        "ingredients": list(pick.get("ingredients", []) or []),
        "reason": str(pick.get("reason", "Recommended by AI")),
    }

    return {
        "recommendations": [
            {
                "id":          make_dish_id(dish),
                "name":        dish["name"],
                "price":       dish["price"],
                "description": dish["description"],
                "ingredients": dish["ingredients"],
                "reason":      dish["reason"],
            }
        ]
    }