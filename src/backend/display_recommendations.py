from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from ai_service import get_recommendation_struct

router = APIRouter(prefix="/display", tags=["display"])


class Preferences(BaseModel):
    budget: Optional[float] = None
    exclude_ingredients: list[str] = []
    cuisine: Optional[str] = None


class RecommendationRequest(BaseModel):
    message: str = ""
    menu: list[dict] = []
    preferences: Preferences = Preferences() 


@router.post("/recommendations")
def display_recommendations(data: RecommendationRequest):
    """
    Return a single recommendation formatted for the frontend card UI.

    Frontend expects:
        { recommendations: [{ id, name, price, description, ingredients, reason }] }
    """
    filtered_menu = data.menu
    budget = data.preferences.budget

    if budget is not None:
        temp_menu = []
        for dish in data.menu:
            price = dish.get("price")
            if price is not None:
                try:
                    if float(price) <= budget:
                        temp_menu.append(dish)
                except (ValueError, TypeError):
                    continue
        filtered_menu = temp_menu

    if not filtered_menu and data.menu:
        return {"recommendations": []}
    pick = get_recommendation_struct(
        user_message=data.message, 
        menu=filtered_menu, 
        preferences=data.preferences.dict()
    )

    if not pick:
        return {"recommendations": []}

    return {
        "recommendations": [
            {
                "id": 1,
                "name": pick.get("name", "Unknown Dish"),
                "price": pick.get("price"),
                "description": pick.get("description", ""),
                "ingredients": pick.get("ingredients", []),
                "reason": pick.get("reason", "Based on your preferences"),
            }
        ]
    }