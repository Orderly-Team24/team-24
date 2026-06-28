# Customer Review Summary — Sprint 2

**Date:** <!-- fill: e.g. 27 Jun 2026 -->
**Participants:** <!-- fill: roles only, no full names — e.g. Product Owner, Customer, Scrum Master -->
**Format:** <!-- fill: e.g. online video call -->

---

## Sprint Goal reviewed

End-to-end flow works on the live deployment: users fill a preferences questionnaire (with mandatory allergens), upload a menu photo with a budget, OCR extracts the text, parser structures it, and the recommender returns a dish matching preferences, containing no allergens, and fitting the budget.

## Delivered increment shown

- Budget filtering (US-001): max budget input, backend post-filter, 422 on invalid input
- Order history backend stub (US-012-1): save, retrieve, check endpoints
- OCR integration and menu parser wired into the recommender flow

## UAT results

<!-- fill after session -->

## Quality evidence discussed

- QR-01 (fault tolerance): AI fallback verified by automated test — system returns HTTP 200 even when AI backend is unavailable
- QR-02 (response time): stub response ≤ 500 ms confirmed in CI
- QR-03 (input validation): blank name and negative budget rejected with correct HTTP status

## Customer feedback

<!-- fill after session -->

## Approvals / requested changes

<!-- fill after session -->

## Remaining risks

- Frontend "I'll order it" button not yet deployed
- OCR quality varies on low-contrast photos
- No persistent storage — order history is lost on backend restart

## Action points and resulting Product Backlog changes

<!-- fill after session -->
