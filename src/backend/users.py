import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, Preferences
from jwt_handler import decode_token

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()


class PreferencesUpdate(BaseModel):
    allergies: list[str] | None = None
    likes: list[str] | None = None
    dislikes: list[str] | None = None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@router.get("/me/preferences")
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prefs = db.query(Preferences).filter(
        Preferences.user_id == current_user.id
    ).first()
    return {
        "allergies": prefs.allergies or [],
        "likes": prefs.likes or [],
        "dislikes": prefs.dislikes or [],
    }


@router.patch("/me/preferences")
def update_preferences(
    data: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prefs = db.query(Preferences).filter(
        Preferences.user_id == current_user.id
    ).first()

    if data.allergies is not None:
        prefs.allergies = data.allergies
    if data.likes is not None:
        prefs.likes = data.likes
    if data.dislikes is not None:
        prefs.dislikes = data.dislikes

    db.commit()
    db.refresh(prefs)

    return {
        "allergies": prefs.allergies,
        "likes": prefs.likes,
        "dislikes": prefs.dislikes,
    }