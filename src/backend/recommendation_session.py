import uuid

from order_history import make_dish_id

sessions: dict = {}

def create_session(menu: list) -> str:
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "menu": menu,
        "shown": []
    }
    return session_id

def get_session(session_id: str) -> dict | None:
    return sessions.get(session_id)

def mark_shown(session_id: str, dish_name: str) -> None:
    session = sessions.get(session_id)
    if session and dish_name not in session["shown"]:
        session["shown"].append(dish_name)

def get_remaining(session_id: str, excluded_ids: set[int] | None = None) -> list:
    """Dishes not yet shown in this session, minus any disliked ids (US-015)."""
    session = sessions.get(session_id)
    if not session:
        return []
    shown = session["shown"]
    excluded_ids = excluded_ids or set()
    return [
        dish
        for dish in session["menu"]
        if dish["name"] not in shown and make_dish_id(dish) not in excluded_ids
    ]
