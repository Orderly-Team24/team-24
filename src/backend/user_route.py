import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Preferences, RefreshToken, OrderHistory, Dislike

router = APIRouter(prefix="/users", tags=["users"])

def _user_id(x_user_id: str | None) -> str:
    uid = (x_user_id or "").strip()
    if not uid:
        raise HTTPException(status_code=401, detail="Missing X-User-Id header")
    return uid

@router.delete("/me")
def delete_account(
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db)
):
    user_id = _user_id(x_user_id)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"status": "deleted"}