from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

from database import get_db
from models import User, Preferences

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PreferencesRequest(BaseModel):
    cuisine: str | None = None
    allergies: list[str] = []
    likes: list[str] = []
    dislikes: list[str] = []


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    preferences: PreferencesRequest


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=409, detail="Username already taken")

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=pwd_context.hash(data.password),
    )
    db.add(user)
    db.flush()

    prefs = Preferences(
        user_id=user.id,
        allergies=data.preferences.allergies,
        likes=data.preferences.likes,
        dislikes=data.preferences.dislikes,
    )
    db.add(prefs)
    db.commit()

    return {"message": "User registered successfully", "user_id": user.id}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )
    return {
        "message": "Login successful",
        "user_id": user.id,
    }
