# Customer Review Summary - Sprint 5

**Date:** 17.07.2026

**Time:** 4:30 pm

---

## Participants

| Participant | Role |
| ------------- | ------ |
| Adelina Khafizova (adelinamikki) | Interviewer |
| Polina Kharlova (Kharlova) | Note taker |
| Omar Nader (Ramy678) | Note taker |
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

Consent to the public MIT-licensed development model and that sanitized transcript may be published in the repository *(told before the meeting)*.

---

## Sprint Goal reviewed

Sprint goal: Polish all functions, fix existing bugs, transfer to customer.

---

## Delivered increment discussed

### Artifacts Demonstrated

The team demonstrated the current state of the application deployed at **[Deployed App](https://team-24-navy.vercel.app)**

### Discussion Points

- A live walkthrough of the application’s user interface.
- Demonstration of the "handling of three columns menus" feature.
- Demonstration of the new "dietary preferences text field" within the user registration questionnaire.
- Verbal confirmation of completed issues (closed tickets) and results from the AI model.
- Access to the project repository (customer confirmed as admin).

### Decisions

- Sprint Goal Status: The customer approved that the Sprint 5 goal was achieved.
- Handover Documentation: The customer approved the current handover document.
- Feature Status:
  - Handling of three-column menus works correctly.
  - Dietary preferences text field works correctly (allergies, dislikes, likes, vegan/halal/etc.).
  - OCR and AI integration is confirmed (text extraction → AI processing).
  - Mobile layout is published and working correctly.
  - Meal type filtering works correctly.
- Acceptance Status: The current status is "Accepted with Follow-up Items."

---

## UAT results

No new User Acceptance Tests were added in this Sprint, all previous ones were successfully completed.

---

## Quality evidence discussed

The following quality metrics and checks were reviewed to ensure the stability of the Sprint 5 increment:

- **Deployment Status:**
  - The application is successfully deployed on Vercel ([App](https://team-24-navy.vercel.app)).
  - Mobile layout is published and functional.

- **Link Integrity (Lychee):**
  - Automated link checking was performed using Lychee.
  - Result: **0 broken links** found in `README.md` and project documentation.

- AI Logic Improvements:
  - Verified that allergy/likes/dislikes constraints are strictly enforced.
  - Verified that three-column menu handling works correctly.

- Remaining Items:
  - Non-critical issues marked with 'could' remain in the repository.
  - History page requires fixing.

---

## Feedback

### Positive

- Sprint goal is considered achieved.
- Dietary preferences feature works as expected.
- Three-column menu handling is functional.
- Mobile layout works correctly.
- Handover documentation is approved.

### Constructive

- History page is not functional and needs immediate fixing.
- A full video demonstration of all features is required after fixes.

---

## Customer approvals or requested changes

- Approved: Sprint 5 goal achieved.
- Approved: Current handover documentation.
- Approved: Product is ready for independent use by the customer (subject to fixes).
- Requested:
  - Fix the history page.
  - Provide a full system video demonstration after all fixes are completed.
  - Transfer the repository (pending).
  - Send finalized documentation for written confirmation.

---

## Risks

| Risk | Probability | Impact | Mitigation |
| ------ | ------------- | -------- | ------------ |
| History Page Failure | High | Blocks full UAT and final acceptance | Immediate fix planned after meeting. |
| Repository Transfer | Low | Minimal (customer already has admin access) | Formal transfer after final acceptance. |
| Missing Final Video | Medium | Delays written confirmation | Commit to providing video post-fixes. |

---

## Action Points

| Assignee | Task | Due Date |
| ---------- | ------ | --------- |
| All Team Members | Fix history page | Immediate (post-meeting) |
| All Team Members | Prepare and send full system video demonstration | After fixes complete |
| All Team Members | Transfer repository ownership | After final acceptance |
| Adelina Khafizova | Send finalized handover documentation for written confirmation | After fixes complete |
| All Team Members | Fix any other identified bugs | Immediate (post-meeting) |

---

## Resulting Product Backlog or scope changes

| Item | Previous State | New State | Location |
|------|----------------|-----------|----------|
| Mobile Layout | In progress | Published and working | Issue #337 |
| History Page | In progress | Not functional – needs immediate fix | Issue #337 |
| Dietary Preferences | Not implemented | Implemented (vegan, halal, etc.) | Issue #331 |
| Meal Type Filtering | Buggy | Fixed | Issue #328 |
| Three-Column Menus | Not handled | Implemented and working | Sprint 5 |
| Recommendations Button | Present | Removed | Issue #329 |
| Handover Documentation | Not Approved | Approved | customer-handover.md |
| Overall Acceptance Status | In progress | Accepted with Follow-up Items | Sprint 5 Review |