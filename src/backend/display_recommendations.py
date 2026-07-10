from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from recommendation_session import (
    create_session,
    get_remaining,
    get_session,
    mark_shown,
    reset_shown,
)

from ai_service import (
    AIServiceUnavailableError,
    FALLBACK_POOL,
    extract_meal_type,
    extract_negated_terms,
    extract_negated_terms_via_llm,
    filter_by_meal_type,
    filter_fallback_pool_by_preferences,
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

    exclude_ingredients: list[str] | None = None
    favorite_ingredients: list[str] | None = None
    max_budget: float | None = Field(default=None, ge=0)


class RecommendationRequest(BaseModel):
    message: str = ""
    menu: list[dict] = []
    preferences: Preferences | None = None
    session_id: str | None = None

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

    `session_id` (returned in the response) tracks which dishes have
    already been shown in this "Another option" rotation, so repeat calls
    with the same `session_id` never show the same dish twice until every
    remaining candidate has been shown once, at which point the rotation
    starts over.
    """
    prefs = data.preferences

    # Fold explicit negations in the free-text mood/craving message (e.g.
    # "I don't want steak") into exclude_ingredients, so they get the same
    # hard-filter + post-hoc guarantee as allergies instead of relying on
    # the recommendation LLM to infer them from prose alone. The regex
    # extractor runs first (free, catches common phrasings); the LLM-backed
    # extractor is a best-effort supplement for phrasings it misses.
    negated_terms = extract_negated_terms(data.message)
    llm_negated_terms = extract_negated_terms_via_llm(data.message)
    if llm_negated_terms:
        existing_lower = {t.lower() for t in negated_terms}
        negated_terms = negated_terms + [
            t for t in llm_negated_terms if t.lower() not in existing_lower
        ]
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
              
    # Meal type (breakfast/lunch/dinner) named in the mood/craving message is
    # a soft preference, not a safety constraint — narrow to matching
    # dishes when we can, otherwise keep the current candidates.
    candidates = filter_by_meal_type(candidates, extract_meal_type(data.message))

    # --- Don't repeat a dish already shown in this "Another option"
    # rotation ------------------------------------------------------------
    if data.session_id and get_session(data.session_id):
        session_id = data.session_id
        remaining_names = {d["name"] for d in get_remaining(session_id)}
        narrowed = [dish for dish in candidates if dish.get("name") in remaining_names]
        if not narrowed:
            # Every candidate has already been shown this session — start
            # the rotation over rather than returning nothing.
            reset_shown(session_id)
            narrowed = candidates
        candidates = narrowed
    else:
        session_id = create_session(candidates)

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
        return {"recommendations": [], "session_id": session_id}

    dish = {
        "name": str(pick.get("name", "Chef's special")),
        "price": pick.get("price"),
        "description": str(pick.get("description", "")),
        "ingredients": list(pick.get("ingredients", []) or []),
        "reason": str(pick.get("reason", "Recommended by AI")),
    }

    mark_shown(session_id, dish["name"])

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
        ],
        "session_id": session_id,
    }