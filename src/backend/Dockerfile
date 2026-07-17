FROM python:3.12-slim

WORKDIR /app

# Build context must be the repository root (not src/backend) — this service
# imports src/db/database.py and models.py via a `../db` sys.path hack, which
# Docker can only satisfy if db/ is inside the same build context as backend/.
COPY src/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend/main.py ./
COPY src/backend/ai_service.py ./
COPY src/backend/display_recommendations.py ./
COPY src/backend/budget_filter.py ./
COPY src/backend/order_history.py ./
COPY src/backend/history_router.py ./
COPY src/backend/recommendation_session.py ./
COPY src/backend/parser.py ./
COPY src/backend/user_route.py ./
COPY src/backend/auth.py ./
COPY src/backend/users.py ./
COPY src/backend/jwt_handler.py ./

# Sibling of /app, matching os.path.join(os.path.dirname(__file__), '..', 'db')
# as resolved from /app/<module>.py.
COPY src/db/ /db/

RUN useradd --create-home appuser && chown -R appuser /app /db
USER appuser

ENV PORT=8000 \
    AI_BACKEND=stub
EXPOSE 8000
CMD ["sh", "-c", "alembic -c /db/alembic.ini upgrade e38340943a94 && uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
