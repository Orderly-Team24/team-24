import uuid

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

def get_remaining(session_id: str) -> list:
    session = sessions.get(session_id)
    if not session:
        return []
    shown = session["shown"]
    return [dish for dish in session["menu"] if dish["name"] not in shown]

def reset_shown(session_id: str) -> None:
    """Clear the "already shown" list once every dish in the session has
    been shown, so "Another option" starts the rotation over instead of
    running out of candidates."""
    session = sessions.get(session_id)
    if session:
        session["shown"] = []
