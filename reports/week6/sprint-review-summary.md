# Customer Review Summary - Sprint 4

**Date:** 10.07.2026

**Time:** 4:30 pm

---

## Participants

| Participant | Role |
| ------------- | ------ |
| Daria Gorshikova (dayeon761) | Interviewer |

## Team Members

- Daria Gorshikova (dayeon761)
- Polina Kharlova (Kharlova)
- Adelina Khafizova (adelinamikki)
- Omar Nader (Ramy678)
- Viktoriia Iakovleva (rxxtzz)
- Vilena Zulkarnaeva (vianevi)

---

## Consent

Consent to the public MIT-licensed development model and that sanitized transcript may be published in the repository *(told before the meeting)*.

---

## Sprint Goal reviewed

Sprint goal: implement history managment, polish existing features, fix detected bugs.

---

## Delivered increment discussed

### Artifacts Demonstrated

The team demonstrated the current state of the application deployed at **[Deployed App](https://team-24-navy.vercel.app/register)**

### Discussion Points

- Implemented "Dislike" functionality: skipping or disliking a dish saves it to user preferences as a disliked item, ensuring it is not recommended again.
- Allergy Safety: Strict rules implemented to ensure AI never recommends food containing allergens or excluded items, even when other options are selected.
- AI now avoids recommending drinks as main dishes unless explicitly requested. Previously, if a specific dish (e.g., steak) was unavailable, AI might incorrectly recommend a drink (e.g., orange juice); this has been fixed.
- The team presented the customer-handover.md document. Clarified that the document reflects the current state of the transfer, not the final completed state. Customer accepted the document in its current state, noting that while dependencies aren't ideal, the handover is acceptable for now.
- Customer requested a user guide or clearer instructions for independent use.

### Decisions

- **Data Persistence Strategy:** Temporary workarounds (cookies/localStorage) for order history are rejected. A **simple registration mechanism** is required to make order history meaningful.
- **Priority Sequence:**
  1. Implement minimal user registration/profile persistence.
  2. Implement "Order History" functionality.
- **UI Changes:**
  - Remove "Cuisine" selection field (redundant in restaurant setting).
  - Add 2–3 specific taste preference questions (e.g., "Likes sweet", "Likes spicy") as dropdowns/buttons.
- **Feature Status:**
  - "I’ll order this dish" button remains non-functional until backend integration is complete.
  - OCR and AI menu processing fixes are deferred to the next sprint.

---

## UAT results

| ID | Scenario | Related US | Status | Notes |
| ---- | ---------- | ------------ | -------- | ------- |
| **UAT-08** | View Order History and Dislike a Dish | US-015 | **PASSED** | The test verifies that ordering a dish, disliking it from the History page with a non-reloading "Saving…" → "Disliked ✓" transition and greyed-out card, and then using "Another option" ensures that disliked dish never reappears in recommendations. |
| **UAT-09** | AI Never Recommends an Excluded or Allergen Food | US-005 | **PASSED** | The test validates that recommendations exclude both formal allergies and mood‑field exclusions, and show nothing if every dish is forbidden. |
| **UAT-10** | AI Recognizes Meal Type and Never Recommends a Drink as the Dish | US-018 | **PASSED** | The test confirms that "something for breakfast" prioritizes breakfast-style meals over dinner options and never returns a beverage-only item as the recommendation. |

---

## Quality evidence discussed

The following quality metrics and checks were reviewed to ensure the stability of the Sprint 4 increment:

- **Deployment Status:**
  - The application is successfully deployed on Vercel ([App](https://team-24-navy.vercel.app)).
  - Zero downtime during the demo.

- **Link Integrity (Lychee):**
  - Automated link checking was performed using Lychee.
  - Result: **0 broken links** found in `README.md` and project documentation.

- AI Logic Improvements:
  - Verified that allergy constraints are strictly enforced.
  - Verified that meal-time context prevents inappropriate recommendations (e.g., drinks as mains).

- Documentation:
  - README.md and CONTRIBUTING.md were reviewed.
  - Customer noted the need for a more user-friendly guide or instructions for independent use.

---

## Feedback

### Positive

- AI recommendation logic is significantly improved and safer regarding allergies and meal context.
- Order history and dislike features are functional and meet expectations.
- Handover documentation is accepted in its current state.

### Constructive

- Meal type filtering (breakfast/dinner/drinks) is unstable and needs fixing.
- UI contains an erroneous extra button that needs removal.
- Documentation lacks a clear user guide for independent operation.

---

## Customer approvals or requested changes

- Approved: Current state of AI fixes, order history, and dislike functionality.
- Approved: customer-handover.md as a reflection of the current transfer state.
- Requested:
  - Fix unstable meal type filtering.
  - Remove erroneous UI button.
  - Add a user guide or clearer instructions for independent use.

---

## Risks

| Risk | Probability | Impact | Mitigation |
| ------ | ------------- | -------- | ------------ |
| Unstable Meal Filtering | High | Poor user experience | Fix filtering logic in next sprint. |
| Lack of User Guide | Medium | Difficulty in independent use | Create simple user guide or enhance README. |
| AI Service Stability | Low | Incorrect recommendations | Final polish of AI service planned for next sprint. |

---

## Action Points

| Assignee | Task | Due Date |
| ---------- | ------ | --------- |
| All Team Members | Fix meal type filtering (breakfast/dinner/drinks) | 17.07.26 |
| Viktoriia Iakovleva, Vilena Zulkarnaeva | Remove erroneous "Recommendations" button from UI | 17.07.26 |
| All Team Members | Add user guide or enhance documentation for independent use | 17.07.26 |
| Adelina Khafizova, Omar Nader | Final polish of AI service and OCR (support more menu types) | 17.07.26 |
| Viktoriia Iakovleva, Vilena Zulkarnaeva | Implement text field for dietary preferences (vegan, halal, etc.) | 17.07.26 |
| All Team Members | Development Team Prepare final handover package | 17.07.26 |

---

## Resulting Product Backlog or scope changes

| Item | Previous State | New State | Location |
|------|----------------|-----------|----------|
| AI Recommendation Logic | Basic filtering | Strict allergy safety and meal-context awareness | AI Service |
| Order Management | Not implemented | Order history and dislike functionality implemented | User Stories / Product Backlog |
| Documentation | Basic README | Needs user guide for independent use | Documentation |
| Meal Filtering | Not implemented | Implemented but unstable | UI / Backend |
| Dietary Preferences | Not implemented | Planned: Text field for vegan/halal/etc. | Next Sprint |