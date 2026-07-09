from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from recommendation_session import create_session, mark_shown

from ai_service import (
    AIServiceUnavailableError,
    FALLBACK_POOL,
    extract_negated_terms,
    filter_fallback_pool_by_preferences,
    filter_out_beverages,
    get_recommendation_struct,
    pick_from_pool,
)
from budget_filter import filter_by_budget
from order_history import get_dislikes, make_dish_id

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
def display_recommendations(
    data: RecommendationRequest,
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """
    Return a single recommendation formatted for the frontend card UI.

    Frontend expects:
        { recommendations: [{ id, name, price, description, ingredients, reason }] }

    When `preferences.max_budget` is set, only dishes with
    `price <= max_budget` are considered. If none fit, returns 200 with
    `recommendations: []`.

    When `X-User-Id` header is provided, dishes the user has disliked
    (via US-015-1) are excluded from recommendations.
    """
    prefs = data.preferences

    # Fold explicit negations in the free-text mood/craving message (e.g.
    # "I don't want steak") into exclude_ingredients, so they get the same
    # hard-filter + post-hoc guarantee as allergies instead of relying on
    # the LLM to infer them from prose alone.
    negated_terms = extract_negated_terms(data.message)
    if negated_terms:
        existing_excludes = list(prefs.exclude_ingredients or []) if prefs else []
        existing_lower = {item.lower() for item in existing_excludes}
        merged_excludes = existing_excludes + [
            term for term in negated_terms if term.lower() not in existing_lower
        ]
        prefs = (prefs or Preferences()).model_copy(update={"exclude_ingredients": merged_excludes})

    candidates = data.menu if data.menu else FALLBACK_POOL

    
    if prefs is not None and prefs.max_budget is not None:
        candidates = filter_by_budget(candidates, prefs.max_budget)
        if not candidates:
            
            return {"recommendations": []}

    if prefs is not None:
        candidates = filter_fallback_pool_by_preferences(candidates, prefs)
        if not candidates:
            # Every candidate dish contains an excluded (e.g. allergen)
            # ingredient — no safe recommendation exists.
            return {"recommendations": []}

    # A drink on its own is never a valid "meal" recommendation, regardless
    # of meal type or other preferences.
    candidates = filter_out_beverages(candidates)
    if not candidates:
        return {"recommendations": []}

    # --- Filter out disliked dishes (US-015-2) ---------------------------
    if x_user_id:
        disliked_ids = set(get_dislikes(x_user_id))
        if disliked_ids:
            candidates = [
                dish
                for dish in candidates
                if make_dish_id(dish) not in disliked_ids
            ]
            if not candidates:
                return {"recommendations": []}

    prefs_dict = prefs.model_dump() if prefs else None

    try:
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