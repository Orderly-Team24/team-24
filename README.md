# team-24

## Orderly: a website which based on your preferences, budget, allergies, and the photo of a menu gives you top-3 best dishes.

## Project structure

All services live under `src/`:

- `src/backend/` — FastAPI service with RAG food recommendation (`main.py`, `retriever.py`, `ai_service.py`, `parser.py`, `ocr_reader.py`)
- `src/upload-menu-backend/` — Photo upload service that forwards menu images to the OCR service (`main.py`)
- `src/frontend/` — Static HTML/JS/CSS prototypes: `food-recommender/` and `photo_from_gallery/`

Other top-level directories:

- `docs/` — design and reference material
- `reports/` — week reports and customer meeting notes
- `system_promts/` — LLM system prompts

## License
This project is licensed under the [MIT License](LICENSE).

## [User Stories](reports/week2/user_stories.md)

## Documentation
- [Week 2 README](reports/week2/README.md)
- [MVP v0 Report](reports/week2/mvp-v0-report.md)
- [Week 3 README](reports/week3/README.md)

## [Customer transcript](reports/week2/customer-meeting-transcript.md)

## [Customer meeting summary](reports/week2/customer-meeting-summary.md)

## [Week 2 analysis](reports/week2/analysis.md)

## [LLM report](reports/week2/llm-report.md)

---

*Figma prototype link is available in the [Week 2 README](reports/week2/README.md) due to technical limitations of automated link checkers.*
