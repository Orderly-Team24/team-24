from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jwt_handler import create_access_token, create_refresh_token, decode_token
from models import RefreshTokens
from datetime import datetime, timedelta
from database import get_db
from models import User, Preferences

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'db'))

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PreferencesRequest(BaseModel):
    allergies: list[str] = []
    likes: list[str] = []
    dislikes: list[str] = []
    dietary_preferences: str | None = None


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
        dietary_preferences=data.preferences.dietary_preferences,
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
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    db.add(RefreshTokens(
        user_id=user.id,
        token_hash=pwd_context.hash(refresh_token),
        expires_at=datetime.utcnow() + timedelta(days=7),
    ))
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id,
    }


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = int(payload["sub"])

    stored_tokens = db.query(RefreshTokens).filter(
        RefreshTokens.user_id == user_id,
        RefreshTokens.expires_at > datetime.utcnow(),
    ).all()

    valid = any(pwd_context.verify(data.refresh_token, t.token_hash) for t in stored_tokens)

    if not valid:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    return {
        "access_token": create_access_token(user_id)
    }