# LLM Report

## 1. Application AI/LLM Integration

Our project integrates LLM capabilities as a core feature for food recommendation.

- **Model Implementation:** We integrated an `ai_service.py` module that supports multiple backends:
- **Stub/Mock Mode:** A deterministic fallback mechanism for development and testing.
- **OpenAI/LM Studio Mode:** We implemented an interface to interact with OpenAI-compatible APIs.
- **Purpose:** The LLMs are used to parse user preferences (cuisine, ingredients, allergies) and recommend dishes based on the uploaded menu structure.
- **Prompt Engineering:** We developed custom system prompts to ensure the AI responds only with valid JSON, respecting the defined recommendation schema and constraints (budget, exclusions).

## 2. Development & Productivity Usage

- AI was used to generate some parts of code and to fix bugs. 
- It was also used to reformulate sentences in reports to make them clearer and more concise.
- Besides, the team used AI to understand tasks better. 
- AI was used to resolve complex Git merge conflicts between the `main` branch and feature branches, particularly in `display_recommendations.py` and `ai_service.py`.
- We utilized AI to draft test cases (e.g., verifying preference filtering logic), which helped ensure our ACs (Acceptance Criteria) were met.
