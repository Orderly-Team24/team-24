from fastapi import APIRouter
from pydantic import BaseModel, Field

from ai_service import FALLBACK_POOL, get_recommendation_struct, pick_from_pool
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
    menu: list[dict] = []  # Из вашей ветки (для загруженного меню)
    preferences: Preferences | None = None  # Из ветки main (для фильтрации и предпочтений)


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

    
    prefs_dict = prefs.dict() if prefs else None
    pick = get_recommendation_struct(data.message, candidates, prefs_dict)

    if not pick:
        return {"recommendations": []}

    
    dish = {
        "name":        str(pick.get("name", "Chef's special")),
        "price":       pick.get("price"),
        "description": str(pick.get("description", "")),
        "ingredients": list(pick.get("ingredients", []) or []),
        "reason":      str(pick.get("reason", "Recommended by AI")),
    }

    
    return {
        "session_id": session_id,  # Берется из глобального контекста файла
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