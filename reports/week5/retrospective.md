# Sprint 3 Retrospective

## What went well

- We managed to close:
  - US-002-1: Create login page, US-002-2: Implement client-side validation and error handling, US-002-3: Implement password verification for login, US-002-4: Set up JWT token generation and storage, US-002-5: Implement redirect after successful login and US-002-6: Implement user registration (US-002: Ability to sign in)
  - US-014: Button "End session"
  - US-017: Delete account
  - US-018: Specify today's meal intent alongside budget
- We fix:
  - Add OPENAI_API_KEY to Render environment
  - Preferences ignored when max_budget is set in display_recommendations.py
  - OCR broken in both backend services

## What did not go well

- Misunderstanding between the backend and the frontend
- Problems with network while connecting all parts of the Product

## What the team changed or attempted to change based on the previous Sprint Retrospective, and what results they observed

In the previous retrospective (Sprint 2), we identified that different parts of the Product caused numerous merge conflicts during the React migration.

We focused on resolving merge conflicts manually as they arose during integration and improved communication between team members when working on intersecting files.

## Action points

- Implement US-015: Managing history of orders
- Polish all features