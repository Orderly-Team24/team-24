# Sprint 4 Retrospective

## What went well

- We managed to close:
  - US-015-1: Backend — dislike storage + endpoints, US-015-2: Backend — filter recommendations by dislikes, US-015-3: Frontend — History page + Dislike button, US-015-4: E2E + docs for dislike feature (US-015: Managing history of orders)
- We fix:
  - Register gives no loading feedback, causing double-submit and false 'email already in use'
  - Second menu photo upload/recommendation didn't work in customer UAT
  - Allergen/excluded ingredients can still be recommended when every candidate dish matches an exclude
  - Expired/invalid access token locks user out of login and register pages
  - Order history is always empty after saving recommended dishes

## What did not go well

- Problems with the AI in recognizing menus
- Customer noted the lack of a clear user guide for independent use, indicating our documentation is still too technical or incomplete for end-users

## What the team changed or attempted to change based on the previous Sprint Retrospective, and what results they observed

In the previous retrospective (Sprint 3), we identified two main action points:

- Implement US-015: Managing history of orders.
- Polish all features.

### Results observed

- We successfully implemented the order history and dislike management system. The customer confirmed during UAT that saving orders and excluding disliked dishes works as expected. This directly addresses the action point from Sprint 3.
- We focused heavily on polishing the AI recommendation engine. We fixed the logic regarding allergies and meal types, which significantly improved the quality of recommendations.

## Action points

- Implement text field for dietary preferences (vegan, halal, etc.)
- Prepare the final handover package
- Final polish of AI service and OCR (support more menu types)
- Create a simple user guide or enhance existing documentation for independent use
