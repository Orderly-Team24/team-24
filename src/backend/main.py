import os

import subprocess
if os.path.isdir('/db'):
    subprocess.run(["alembic", "upgrade", "head"], cwd="/db")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Force Docker rebuild after cache issue
from ai_service import get_recommendation
from display_recommendations import router as display_router
from history_router import router as history_router
from user_route import router as user_router
from auth import router as auth_router
from users import router as users_router
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "DELETE", "PATCH"],
    allow_headers=["*"],
)
app.include_router(display_router)
app.include_router(history_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "orderly-recommender"}


@app.post("/recommend")
def recommend_food(data: dict):
    answer = get_recommendation(data["message"])
    return {"recommendation": answer}
