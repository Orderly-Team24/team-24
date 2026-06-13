# Customer Meeting Summary

**Date:** 11:00 AM, 11.06.26

---

## Participants

| Participant | Role |
|-------------|------|
| Daria Gorshikova (dayon761) | Interviewer |
| Polina Kharlova (Kharlova) | Note taker |
| Adelina Khafizova (adelinamikki) | Interviewer |

## Team Members

- Daria Gorshikova (dayon761)
- Polina Kharlova (Kharlova)
- Adelina Khafizova (adelinamikki)
- Omar Nader (Ramy678)
- Viktoriia Iakovleva (rxxtzz)
- Vilena Zulkarnaeva (vianevi)

---

## Consent

Consent to the public MIT-licensed development model and that sanitized transcript may be published in the repository *(told during the meeting, reminded the customer after it ended)*.

---

## Artifacts Demonstrated

- **Interactive prototype (Figma):** https://www.figma.com/proto/BK4oKfBZo6r8RxjTanLQ3z/Untitled?node-id=0-1&t=3PdFw5wmGupLDKLm-1
- **User stories (Google Sheets):** https://docs.google.com/spreadsheets/d/1w0kKh7sBFx73ouXdOFs5OwUZCW_bYmZF5AQAmcbBWas/edit?usp=sharing

---

## Discussion Points

- User stories completeness (mandatory functionality)
- MoSCoW priorities validation: MUST vs. SHOULD vs. COULD classification
- MVP version 1 scope
- Design and interface approval
- Recommendation quality measurement
- What minimum information must a menu contain for the system to work?
- If OCR confidence is low, should we continue automatically or ask the user to verify?
- Is it enough to recommend dishes, or must every recommendation include a human-readable explanation?
- If multiple dishes appear equally suitable, should we rank them, randomize, or ask additional questions?

---

## Decisions

- Proposing dishes according to the budget is not a MUST, but **SHOULD**
- High speed of the search system is not a SHOULD, but **COULD**
- No sign-in for the first version of the project
- Setting the budget should be done after the onboarding questionnaire, before or after scanning the menu
- In the first version there should be no like/dislike buttons, just options "I will order this" and "Dismiss, another option"
- For recommendation quality measurement, very simple tests should be made to verify the system works correctly
- Minimum menu information for the system to work is a list of dish names
- If OCR confidence is low, display a warning and ask the user to verify
- No human-readable explanation needed with the recommendation
- If multiple dishes appear equally suitable, randomize them

---

## Action Points

| Assignee | Task | Due |
|----------|------|-----|
| adelinamikki | Update the MoSCoW priorities in the user stories | 13.06.26 |
| adelinamikki, Ramy678 | Update user interface in Figma | 13.06.26 |
| dayon761, Kharlova | Include all changes and suggestions in MVP0 | 13.06.26 |
| rxxtzz, vianevi | Create GitHub repository and configure it | 13.06.26 |

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Customer doesn't like the proposed design | Medium | Team will have to rework the entire UI, may miss the deadline | Alter the interface with all team members as soon as possible |
| Scope creep (+10 new feature requests for MVP) | Low | Failing the deadline | Choose only the most essential features for MVP-0, implement them first |

---

## Feedback

### Positive
- Good user stories
- Enough initial functions
- Good user interface

### Constructive
- Proposing dishes according to the budget is not a MUST, but SHOULD
- High speed of the search system is not a SHOULD, but COULD
- No sign-in for the first version of the project
- Setting the budget should be done after the onboarding questionnaire, before or after scanning the menu
- In the first version there should be no like/dislike buttons, just options "I will order this" and "Dismiss, another option"

---

## Customer Approvals

- The documented user stories
- The MoSCoW priorities (altered and then approved)
- The initial proposed MVP v1 scope (altered and then approved)
- Consent to the public MIT-licensed development model
- Permission for sharing recording and a sanitized English transcript privately with instructors for assessment

---

## Resulting Changes

- Proposing dishes according to the budget changed from MUST → **SHOULD** — updated in Google Sheets
- High speed of the search system changed from SHOULD → **COULD** — updated in Google Sheets
- Like/dislike buttons replaced with "I will order this" and "Dismiss, another option" — updated in Figma
