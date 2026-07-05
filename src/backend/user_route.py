import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Preferences, RefreshTokens, OrderHistory, Dislikes
from users import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/me")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.delete(current_user)
    db.commit()

    return {"status": "deleted"}
