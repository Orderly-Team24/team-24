# Roadmap

## Sprint 1
- **Milestone:** [Milestone - Sprint 1](https://github.com/Orderly-Team24/team-24/milestone/1?closed=1)
- **Issues:** [Closed issues - Sprint 1](https://github.com/Orderly-Team24/team-24/issues?q=is%3Aissue%20state%3Aclosed%20milestone%3A%22Sprint%201%22)
- **Dates:** 15-06-2026 – 21-06-2026
- **Goal:** MVP-V1, enable users to upload a photo of a menu from the gallery and receive a dish recommendation based on the menu.
- **Focus or expected outcome statement:** 
	- Create frontend for pages with photo uploads and recommended dishes
	- The AI model can recommend a dish reading a menu from a json file
	- Write backend for uploading menu and displaying recommendations
- **Planned items:** 
	- [US-011: Upload photo of a menu - Issue #62](https://github.com/Orderly-Team24/team-24/issues/62)
	- [US-011-1: Choose photo from gallery - Issue #71](https://github.com/Orderly-Team24/team-24/issues/71)
	- [US-011-1: Frontend - Issue #92](https://github.com/Orderly-Team24/team-24/issues/92)
	- [US-011-1: Backend - Issue #93](https://github.com/Orderly-Team24/team-24/issues/93)
	- [US-011-2: Text parsing - Issue #72](https://github.com/Orderly-Team24/team-24/issues/72)
	- [US-011-3: Dish choice - Issue #73](https://github.com/Orderly-Team24/team-24/issues/73)
	- [US-011-4: Displaying menu recommendations - Issue #75](https://github.com/Orderly-Team24/team-24/issues/75)
	- [US-011-4: Frontend - Issue #94](https://github.com/Orderly-Team24/team-24/issues/94)
	- [US-011-4: Backend - Issue #95](https://github.com/Orderly-Team24/team-24/issues/95)
	- [US-011-5: Deploy publicly - Issue #122](https://github.com/Orderly-Team24/team-24/issues/122)


## Sprint 2
- **Milestone:** [Milestone - Sprint 2](https://github.com/Orderly-Team24/team-24/milestone/2?closed=1)
- **Issues:** [Closed issues - Sprint 2](https://github.com/Orderly-Team24/team-24/issues?q=is%3Aissue%20state%3Aclosed%20milestone%3A%22Sprint%202%22)
- **Dates:** 22-06-2026 – 28-06-2026
- **Goal:** End-to-end flow works on the live deployment. Users fill a preferences questionnaire (with mandatory allergens), upload a menu photo with a budget, OCR extracts the text, the parser structures it, and the recommender returns a dish that matches preferences, contains no allergens, and fits the budget.
- **Focus or expected outcome statement:** 
	- Create frontend for buttons "I'll order dish" and "Another option"
	- The AI model can recommend a dish according to the budget
	- The AI model can recommend a dish according to the preferences
- **Planned items:** 
	- [US-001: Propose dishes according to the budget - Issue #57](https://github.com/Orderly-Team24/team-24/issues/57)
	- [US-001-1: Budget: API + filter = Issue #154](https://github.com/Orderly-Team24/team-24/issues/154)
	- [US-001-2: Budget: UI - Issue #155](https://github.com/Orderly-Team24/team-24/issues/155)
	- [US-004: Propose dishes according to preferences - Issue #64](https://github.com/Orderly-Team24/team-24/issues/64)
	- [US-004-1: Preferences+API contract - Issue #150](https://github.com/Orderly-Team24/team-24/issues/150)
	- [US-004-2: Preferences: prompt + stub - Issue #151](https://github.com/Orderly-Team24/team-24/issues/151)
	- [US-004-3: Preferences: UI - Issue #152](https://github.com/Orderly-Team24/team-24/issues/152)
	- [US-004-4: Preferences: parser-binding - Issue #153](https://github.com/Orderly-Team24/team-24/issues/153)
	- [US-012: Button "I'll order dish" - Issue #146](https://github.com/Orderly-Team24/team-24/issues/146)
	- [US-012-1: Frontend - Issue #156](https://github.com/Orderly-Team24/team-24/issues/156)
	- [US-012-2: Backend - Issue #157](https://github.com/Orderly-Team24/team-24/issues/157)
	- [US-013: "Button "Another option" - Issue #147](https://github.com/Orderly-Team24/team-24/issues/147)
	- [US-013-1: Frontend - Issue #158](https://github.com/Orderly-Team24/team-24/issues/158)
	- [US-013-2: Backend - Issue #159](https://github.com/Orderly-Team24/team-24/issues/159)
	- [Migrate frontend to React - Issue #161](https://github.com/Orderly-Team24/team-24/issues/161)
	- [Re-deploy frontend after US-011/US-004/US-001 work - Issue #162](https://github.com/Orderly-Team24/team-24/issues/162)


## Sprint 3
- **Milestone:** [Milestone - Sprint 3](https://github.com/Orderly-Team24/team-24/milestone/3?closed=1)
- **Issues:** [Closed issues - Sprint 3](https://github.com/Orderly-Team24/team-24/issues?q=is%3Aissue%20state%3Aclosed%20milestone%3A%22Sprint%203%22)
- **Dates:** 29-06-2026 – 05.07.2026
- **Goal:** Polish existing features, add sign-in and sign-up pages, add history management.
- **Focus or expected outcome statement:** 
	- Create frontend for buttons "End session" and implement sign-in functionality
	- Allow users to specify today's meal intent alongside budget
	- Enable account management (sign-in, delete account)
	- Fix critical backend issues: OpenAI API key configuration, preferences ignored with budget, and broken OCR
- **Planned items:** 
	- [US-002: Ability to sign in - Issue #63](https://github.com/Orderly-Team24/team-24/issues/63)
	- [US-002-1: Create login page - Issue #74](https://github.com/Orderly-Team24/team-24/issues/74)
	- [US-002-2: Implement client-side validation and error handling - Issue #76](https://github.com/Orderly-Team24/team-24/issues/76)
	- [US-002-3: Implement password verification for login - Issue #77](https://github.com/Orderly-Team24/team-24/issues/77)
	- [US-002-4: Set up JWT token generation and storage - Issue #78](https://github.com/Orderly-Team24/team-24/issues/78)
	- [US-002-5: Implement redirect after successful login - Issue #79](https://github.com/Orderly-Team24/team-24/issues/79)
	- [US-002-6: Implement user registration - Issue #216](https://github.com/Orderly-Team24/team-24/issues/216)
	- [US-014: Button "End session" - Issue #148](https://github.com/Orderly-Team24/team-24/issues/148)
	- [US-017: Delete account - Issue #221](https://github.com/Orderly-Team24/team-24/issues/221)
	- [US-018: Specify today's meal intent alongside budget - Issue #222](https://github.com/Orderly-Team24/team-24/issues/222)
	- [Fix: add OPENAI_API_KEY to Render environment - Issue #217](https://github.com/Orderly-Team24/team-24/issues/217)
	- [Fix: preferences ignored when max_budget is set in display_recommendations.py - Issue #218](https://github.com/Orderly-Team24/team-24/issues/218)
	- [Fix: OCR broken in both backend services - Issue #219](https://github.com/Orderly-Team24/team-24/issues/219)


## Sprint 4
- **Milestone:** [Milestone - Sprint 4](https://github.com/Orderly-Team24/team-24/milestone/4?closed=1)
- **Issues:** [Issues - Sprint 4](https://github.com/Orderly-Team24/team-24/issues?q=is%3Aissue%20milestone%3A%22Sprint%204%22)
- **Dates:** 06-07-2026 – 12-07-2026
- **Goal:** Implement order history management (view history, dislike a dish), polish existing AI recommendation quality, and fix bugs found during customer UAT.
- **Focus or expected outcome statement:**
	- Store dislikes and let the user view/manage order history from the frontend
	- Filter future recommendations by disliked dishes
	- Harden AI recommendation safety: never recommend an allergen/excluded ingredient even when the LLM backend is used, correctly parse plain-language exclusions ("I don't want steak") and meal-type intent (breakfast/lunch/dinner), never recommend a beverage on its own as "the dish"
	- Fix authentication/session bugs discovered during UAT (expired-token lockout, order history using a mismatched user identity, a missing frontend route)
- **Planned items:**
	- [US-015: Managing history of orders - Issue #149](https://github.com/Orderly-Team24/team-24/issues/149)
	- [US-015-1: Backend — dislike storage + endpoints - Issue #285](https://github.com/Orderly-Team24/team-24/issues/285)
	- [US-015-2: Backend — filter recommendations by dislikes - Issue #286](https://github.com/Orderly-Team24/team-24/issues/286)
	- [US-015-3: Frontend — History page + Dislike button - Issue #287](https://github.com/Orderly-Team24/team-24/issues/287)
	- [US-015-4: E2E + docs for dislike feature - Issue #288](https://github.com/Orderly-Team24/team-24/issues/288)
	- [BUG: Second menu photo upload/recommendation didn't work in customer UAT - Issue #283](https://github.com/Orderly-Team24/team-24/issues/283)
	- [BUG: Register gives no loading feedback, causing double-submit and false "email already in use" - Issue #282](https://github.com/Orderly-Team24/team-24/issues/282)
	- [BUG: Allergen/excluded ingredients can still be recommended when every candidate dish matches an exclude - Issue #298](https://github.com/Orderly-Team24/team-24/issues/298)
	- [BUG: Expired/invalid access token locks user out of login and register pages - Issue #295](https://github.com/Orderly-Team24/team-24/issues/295)
	- [BUG: Order history is always empty after saving recommended dishes - Issue #311](https://github.com/Orderly-Team24/team-24/issues/311)


## Sprint 5
- **Milestone:** [Milestone - Sprint 5](https://github.com/Orderly-Team24/team-24/milestone/5?closed=1)
- **Issues:** [Issues - Sprint 5](https://github.com/Orderly-Team24/team-24/issues?q=is%3Aissue%20milestone%3A%22Sprint%205%22)
- **Dates:** 13-07-2026 – 19-07-2026
- **Goal:** Polish all fucntions, fix existing bugs, transfer to customer.
- **Focus or expected outcome statement:**
  - Polish the UI/UX across the board: fix mobile layout issues, style the Order History page including the Dislike button, and remove the redundant "Recommendations" button
  - Stabilize core features: fix unstable meal-type filtering and improve Menu OCR to handle complex layouts like 3-column menus
  - Move order history and dislikes out of in-memory storage and into the actual database, so nothing's lost on restart
  - Prepare for customer handover: add a text field for dietary preferences, include a user guide for independent use, and clean up dead endpoints
  - Fix menu OCR so it handles 3-column and uneven column layouts properly
- **Planned items:**
  - [BUG: Mobile layout is unpolished sitewide, and Order History page (incl. Dislike button) has no styling at all - Issue #337](https://github.com/Orderly-Team24/team-24/issues/337)
  - [BUG: Meal type filtering (breakfast/dinner/drinks) is unstable - Issue #328](https://github.com/Orderly-Team24/team-24/issues/328)
  - [BUG: Remove extra "Recommendations" button from UI - Issue #329](https://github.com/Orderly-Team24/team-24/issues/329)
  - [BUG: Add user guide or clearer instructions for independent use - Issue #330](https://github.com/Orderly-Team24/team-24/issues/330)
  - [BUG: Implement text field for dietary preferences - Issue #331](https://github.com/Orderly-Team24/team-24/issues/331)
  - [BUG: Order history and dislikes are stored in-memory, not in the database - lost on every restart - Issue #338](https://github.com/Orderly-Team24/team-24/issues/338)
  - [BUG: Menu OCR doesn't handle 3 columns or uneven column splits - Issue #339](https://github.com/Orderly-Team24/team-24/issues/339)
  - [BUG: Dead /display/another-option endpoint has its own bugs and duplicates logic already in /display/recommendations - Issue #340](https://github.com/Orderly-Team24/team-24/issues/340)
