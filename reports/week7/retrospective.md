# Sprint 5 Retrospective

## What went well

- We successfully closed the Sprint 5 goal: polished all functions, fixed existing bugs.
- We implemented the dietary preferences text field (vegan, halal, etc.) as requested by the customer (Issue #331).
- We fixed meal type filtering bug (Issue #328), breakfast/lunch/dinner now works correctly.
- We implemented handling of three-column menus (Issue #339).
- Mobile layout fixes were completed and published (Issue #337).
- Fixed dead /display/another-option endpoint and removed duplicate logic (Issue #340).
- Fixed order history and dislikes to persist in database instead of in-memory storage (Issue #338).
- Removed extra "Recommendations" button from UI (Issue #329).
- Added user guide and clearer instructions for independent use (Issue #330).
- The customer approved the sprint goal and handover documentation.

## What did not go well

- The history page required additional fixes after the customer meeting, which delayed full UAT completion.
- A demo video was not prepared ahead of time, though the customer expressed interest in having one for reference.

## What the team changed or attempted to change based on the previous Sprint Retrospective, and what results they observed

In the previous retrospective (Sprint 4), we identified four main action points:

1. **Implement text field for dietary preferences (vegan, halal, etc.)**
Completed. The field was successfully added to the registration questionnaire and integrates with AI recommendations.

2. **Prepare the final handover package**
Completed. Handover documentation was approved by the customer, though some items (demo video, final fixes) were delivered post-meeting.

3. **Final polish of AI service and OCR (support more menu types)**
Completed. AI logic for allergies and meal types was improved and verified by the customer. Three-column menus now work correctly.

4. **Create a simple user guide or enhance existing documentation for independent use**
Completed. Documentation was improved, but the customer still requested a full video demonstration for independent use.

### Results observed

- The dietary preferences feature works as expected and was well-received by the customer.
- AI recommendation logic is significantly safer regarding allergies and meal context.
- The customer confirmed they will use the app themselves, validating that the product solves a real problem.
- However, the lack of a prepared demo video and the history page failure during the demo created unnecessary friction in the final acceptance process.

## Action points

- **Improve internal testing procedures** — Run a full UAT-style test on all critical flows (registration, login, history, recommendations) before any customer demo to catch issues like broken pages.
- **Prepare handover artifacts earlier** — Complete all handover documentation and create a demo video before the final Sprint Review, not as a reaction to customer requests.
