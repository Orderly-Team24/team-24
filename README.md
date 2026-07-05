# Orderly

A web app that recommends dishes based on your preferences, budget, allergies, and the photo of a restaurant menu.

## Live demo

| Service | URL |
|---------|-----|
| Frontend (Vercel, auto-deploy from `main`) | https://team-24-navy.vercel.app |
| Recommender API (Render) | https://team-24.onrender.com |
| Upload / OCR API (Render) | https://team-24-1.onrender.com |

> Free-tier services on Render may take 5–15 s to wake up after inactivity.

## Project structure

```
team-24/
├── src/
│   ├── backend/              # Recommender service (FastAPI + Python)
│   ├── upload-menu-backend/  # OCR / photo upload service (FastAPI + Tesseract)
│   └── new-frontend/         # React SPA (deployed via Vercel)
├── docs/                     # Design docs, quality requirements, testing strategy
├── reports/                  # Weekly reports and customer notes
├── CHANGELOG.md
└── README.md
```

## Getting started (local development)

### Prerequisites

- Python 3.12+
- Node.js 18+ and npm

### Backend services

The recommender service requires `DATABASE_URL` (PostgreSQL in production, see
[ADR-002](docs/architecture/adr/ADR-002-postgresql-sqlalchemy.md)) — it will not start without it.
For local development, SQLite works fine since it's just a SQLAlchemy connection string:

```bash
# Create and activate a virtualenv
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies for both backend services
pip install -r src/backend/requirements.txt
pip install -r src/upload-menu-backend/requirements.txt

# Point at a local SQLite file (swap for a real postgres:// URL to match production)
export DATABASE_URL="sqlite:///$(pwd)/local.db"

# Create the tables
cd src/db
alembic upgrade head
cd ../..

# Run the recommender service (http://localhost:8003)
cd src/backend
AI_BACKEND=stub uvicorn main:app --reload --port 8003

# In a separate terminal — run the OCR upload service (http://localhost:8002)
# Requires tesseract-ocr to be installed on the host:
#   Ubuntu/Debian: sudo apt-get install tesseract-ocr
#   macOS:         brew install tesseract
cd src/upload-menu-backend
uvicorn main:app --reload --port 8002
```

### Frontend (React)

```bash
cd src/new-frontend
npm install
REACT_APP_API_URL=http://localhost:8003 npm start
# Opens http://localhost:3000
```

### Running tests

```bash
# Recommender backend
cd src/backend
pytest tests/ -v --cov=. --cov-report=term-missing

# Upload backend
cd src/upload-menu-backend
pytest tests/ -v --cov=. --cov-report=term-missing
```

## Documentation

- [User stories](docs/user-stories.md)
- [Architecture documentation](docs/architecture/README.md) — component, sequence, and deployment views, plus ADRs
- [Development process](docs/development-process.md) — git workflow, PR process, CI pipeline, configuration management
- [Quality requirements](docs/quality-requirements.md)
- [Quality requirement tests](docs/quality-requirement-tests.md)
- [Testing strategy](docs/testing.md)
- [Definition of Done](docs/definition-of-done.md)
- [User acceptance tests](docs/user-acceptance-tests.md)
- [Roadmap](docs/roadmap.md)
- [MVP v0 Report](reports/week2/mvp-v0-report.md)
- [CHANGELOG](CHANGELOG.md)
- [Week 2 report](reports/week2/README.md)
- [Week 3 report](reports/week3/README.md)
- [Week 4 report](reports/week4/README.md)
- [Week 5 report](reports/week5/README.md)

Hosted (browsable) version of the docs above: https://orderly-team24.github.io/team-24/

## License

[MIT](LICENSE)