FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY ai_service.py ./
COPY display_recommendations.py ./
COPY budget_filter.py ./
COPY order_history.py ./
COPY history_router.py ./
COPY another_option.py ./
COPY recommendation_session.py ./
COPY ocr_reader.py ./
COPY parser.py ./

RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

ENV PORT=8000 \
    AI_BACKEND=stub
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
