# ADR-001: Split OCR and Recommender into separate services

**Date:** 2026-06-22  
**Status:** Accepted

## Context

The product requires two distinct backend capabilities: extracting text from menu images (OCR using Tesseract) and generating dish recommendations (AI using OpenAI). Both could run in a single FastAPI process, but Tesseract requires system-level packages (`tesseract-ocr`, `tesseract-ocr-rus`) that significantly increase the Docker image size and add OS-level installation steps to the build.

## Decision

Split the backend into two independently deployed FastAPI services:
- `src/upload-menu-backend/` — handles image upload and OCR only
- `src/backend/` — handles recommendations, user data, order history, and AI calls

The frontend acts as the orchestrator: it calls the OCR service first, receives the structured menu, stores it in `localStorage`, then calls the Recommender service with the menu data.

## Consequences

**Positive:**
- Each service has a single responsibility and can be deployed, updated, and scaled independently.
- A failure or slow cold start in the OCR service does not affect the recommendation endpoint.
- The Recommender service Docker image stays small (no Tesseract dependency).
- Changes to the OCR engine (e.g., switching from Tesseract to a cloud OCR API) do not require touching the Recommender service.

**Negative:**
- Two Render deployments to maintain (two Dockerfiles, two `requirements.txt`, two environment variable sets).
- The frontend must handle partial failures explicitly (e.g., OCR succeeds but the menu is malformed).
- Render free-tier cold starts affect both services independently, so the first user request after inactivity may trigger two separate cold starts.

## Quality requirements addressed

- **QR-002 – Fault Tolerance:** service isolation prevents an OCR failure from taking down the recommender.
- **QR-003 – Maintainability:** single-responsibility services are easier to understand, test, and modify independently.
