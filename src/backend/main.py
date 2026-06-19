from fastapi import FastAPI
from ai_service import get_recommendation

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()


@app.post("/recommend")
def recommend_food(data: dict):

    answer = get_recommendation(
        data["message"]
    )

    return {
        "recommendation": answer
    }