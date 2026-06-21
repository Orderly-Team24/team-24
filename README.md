# Orderly

A web app that recommends dishes based on your preferences, budget, allergies, and the photo of a restaurant menu.

## Live demo

- Frontend: https://frontend-pearl-sigma-1diis9tsn9.vercel.app
- Recommender API: https://team-24.onrender.com
- Upload API: https://team-24-1.onrender.com

> Free-tier services on Render may take 5-15s to wake up after inactivity.

## Project structure

```
team-24/
├── src/
│   ├── backend/              # Recommender service
│   ├── upload-menu-backend/  # Photo upload service
│   └── frontend/             # Static SPA (Vercel)
├── docs/                     # Design docs and user stories
├── reports/                  # Weekly reports and customer notes
├── CHANGELOG.md
└── README.md
```

## Getting started

```bash
# Create venv and install deps
python -m venv venv
source venv/bin/activate
pip install -r src/backend/requirements.txt
pip install -r src/upload-menu-backend/requirements.txt

# Run services
cd src/backend            && uvicorn main:app --reload --port 8003 &
cd src/upload-menu-backend && uvicorn main:app --reload --port 8002 &

# Serve frontend (any static server)
cd src/frontend && python -m http.server 8080
```

## Documentation

- [User stories](docs/user-stories.md)
- [CHANGELOG](CHANGELOG.md)
- [Week 2 report](reports/week2/README.md)
- [Week 3 report](reports/week3/README.md)

## License

[MIT](LICENSE)