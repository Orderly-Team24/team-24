import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User, Preferences, RefreshTokens, OrderHistory, Dislikes
from jwt_handler import decode_token

router = APIRouter(prefix="/users", tags=["users"])


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user


class PreferencesUpdate(BaseModel):
    # cuisine isn't a real column on Preferences yet — accepted and ignored
    # so ProfilePage.jsx (which always sends it) doesn't get a 422.
    cuisine: str | None = None
    # None (the "not sent") default vs. [] ("explicitly cleared") lets a
    # partial body update only the fields it names, per US-016's AC.
    allergies: list[str] | None = None
    likes: list[str] | None = None
    dislikes: list[str] | None = None


@router.delete("/me")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.delete(current_user)
    db.commit()

    return {"status": "deleted"}


@router.get("/me/preferences")
def get_my_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prefs = db.query(Preferences).filter(Preferences.user_id == current_user.id).first()
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")

    return {
        "allergies": prefs.allergies or [],
        "likes": prefs.likes or [],
        "dislikes": prefs.dislikes or [],
    }


@router.patch("/me/preferences")
def update_my_preferences(
    data: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prefs = db.query(Preferences).filter(Preferences.user_id == current_user.id).first()
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")

    if data.allergies is not None:
        prefs.allergies = data.allergies
    if data.likes is not None:
        prefs.likes = data.likes
    if data.dislikes is not None:
        prefs.dislikes = data.dislikes
    db.commit()

    return {
        "allergies": prefs.allergies,
        "likes": prefs.likes,
        "dislikes": prefs.dislikes,
    }
