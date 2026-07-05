# Customer Review Summary - Sprint 3

**Date:** 05.07.2026
**Time:** 10:00 аm

---

## Participants

| Participant | Role |
|-------------|------|
| Polina Kharlova (Kharlova) | Interviewer |
| Viktoriia Iakovleva (rxxtzz) | Note taker |
| Vilena Zulkarnaeva (vianevi) | Note taker |

## Team Members

- Daria Gorshikova (dayeon761)
- Polina Kharlova (Kharlova)
- Adelina Khafizova (adelinamikki)
- Omar Nader (Ramy678)
- Viktoriia Iakovleva (rxxtzz)
- Vilena Zulkarnaeva (vianevi)

---

## Consent

Consent to the public MIT-licensed development model and that sanitized transcript may be published in the repository *(told during the meeting)*.

---

## Sprint Goal reviewed

Polish existing features, add sign-in and sign-up pages, add history management.

---

## Delivered increment discussed

### Artifacts Demonstrated

The team demonstrated the current state of the application deployed at **[Deployed App](https://team-24-navy.vercel.app/register)**

### Discussion Points

- Successful implementation of simple user registration (email/password).
- Updated Preference UI: "Cuisine" field removed, "Specify today’s meal intent alongside budget" added.
- Added the button "End session"
- Account deletion is now available

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
|----|----------|------------|--------|-------|
| **UAT-04** | Sign In With Existing Account | US-002 | **PASSED** | On valid credentials, the user is redirected to /upload with saved preferences auto-loaded; on invalid password, an inline error appears on /login—no crashes or blank pages. |
| **UAT-05** | Delete Account | US-017 | **PASSED** | After confirmation, the user is redirected to /register, all local session data is cleared, and subsequent sign-in attempts with the deleted account fail with an error indicating the account no longer exists. |
| **UAT-06** | End Session | US-014 | **PASSED** | The The user is redirected to /upload with localStorage cleared but auth tokens retained (keeping them logged in), and navigating back to /food-recommender starts a fresh session with no stale data and no error messages. |
| **UAT-07** | Specify Today's Meal Intent Alongside Budget | US-018 | **PASSED** | The mood field is visible and optional with the correct placeholder text; leaving it empty defaults to saved preferences, while filling it tailors the recommendation reason to the entered craving, and clicking "End session" clears the field without any error messages. |

---

## Quality evidence discussed

The following quality metrics and checks were reviewed to ensure the stability of the Sprint 3 increment:

- **Deployment Status:** 
  - The application is successfully deployed on Vercel ([Link](https://team-24-navy.vercel.app)).
  - Zero downtime during the demo.

- **Link Integrity (Lychee):** 
  - Automated link checking was performed using Lychee.
  - Result: **0 broken links** found in `README.md` and project documentation.

- **Error Handling:** 
  - Registration errors (duplicate email, weak password) display clear user-facing messages.

---

## Feedback

### Positive
- Implemented features (sign in, end session, delete account, Specify Today's Meal Intent Alongside Budget) work correctly.
- Main product ideas align with customer expectations.

### Constructive
- Minor issues with the website's design.

---

## Customer approvals or requested changes

- Approval of completed registration, ending session and deleting account.
- Plan for the next sprint: Focus on implementation the history.

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AI recommendation accuracy | Medium | Irrelevant suggestions | Collect user feedback on recommendations; refine algorithm |
| Database scalability issues | Low | Slow queries with large datasets | Monitor query performance; add indexing as needed |


---


## Action Points

| Assignee | Task | Due Date |
|----------|------|---------|
| Viktoriia Iakovleva, Vilena Zulkarnaeva | refine minor design flaws | 10.07.26 |
| All Team Members | US-015 and polishing all features | 10.07.26 |

---

## Resulting Product Backlog or scope changes

| Item | Previous State | New State | Location |
|------|----------------|-----------|----------|
| Design Quality | Minor visual inconsistencies present | Refined UI/UX with polished design elements | UI tasks |
| Feature Completeness | Core features functional but rough | US-015 completed, all features polished and production-ready | User Stories / Product Backlog |
