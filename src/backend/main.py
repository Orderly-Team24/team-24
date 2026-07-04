import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_service import get_recommendation
from display_recommendations import router as display_router
from history_router import router as history_router
from another_option import router as another_option_router
from user_route import router as user_router
from auth import router as auth_router
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
app.include_router(another_option_router)
app.include_router(user_router)
app.include_router(auth_router)

MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "orderly-recommender"}


@app.post("/recommend")
def recommend_food(data: dict):
    answer = get_recommendation(data["message"])
    return {"recommendation": answer}


@app.post("/upload-menu")
async def upload_menu(photo: UploadFile):
    from ocr_reader import extract_text
    from parser import parse_menu

    contents = await photo.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 8 MB")

    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    temp_path = f"temp_{photo.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    try:
        raw_text = extract_text(temp_path)

        structured_menu = parse_menu(raw_text)

        return {
            "status": "success",
            "menu": structured_menu
        }
    finally:
        os.remove(temp_path)
