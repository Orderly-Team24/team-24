# Reports/week2/analysis

## Learning Points

- **User stories:** Our initial MoSCoW priorities were only partially correct — for example, proposing dishes according to the budget was marked as MUST instead of SHOULD, and high speed of the search system was SHOULD instead of COULD. We learned that direct customer review is necessary to calibrate priorities correctly.

- **Prioritization:** The customer's response shifted two stories down in priority and removed sign-in from MVP v1 entirely, showing that developer assumptions about "core" features do not always match customer expectations.

- **Prototyping:** We showed a basic prototype without final design. The customer ignored the looks and focused on functionality, which helped us get actionable feedback.

- **Interface design:** The customer got confused because we mixed "order now" buttons with "like/dislike" buttons on the same screen. We should separate them: ordering actions on the recommendation screen, and like/dislike in the order history.

- **MVP v0 deployment:** Budget input was placed in the onboarding questionnaire, but it belongs on the ordering screen since it changes per visit, not per user setup.

- **Customer validation:** A structured meeting with a plan and prepared questions was truly helpful — the customer managed to give us precise feedback.

---

## Validated Assumptions

- **Confirmed:** We assumed dish name alone is sufficient menu data for the recommendation system — confirmed.
- **Confirmed:** We assumed that a simple warning is enough when OCR confidence is low — confirmed.
- **Confirmed:** We assumed no human-readable explanation is needed alongside dish recommendations — confirmed.
- **Confirmed:** We assumed that if two or more dishes follow the user's preferences, the system should randomly pick one of them — confirmed.
- **Rejected:** We assumed budget input should be in the onboarding questionnaire — rejected.
- **Rejected:** We assumed like/dislike buttons belong on the recommendation screen — rejected. The recommendation screen should only have "I will order this" and "Dismiss / recommend another"; like/dislike belongs in order history.
- **Rejected:** We assumed sign-in is a MUST for MVP v1 — rejected.

---

## Needs Clarification

- Exact placement of the budget input field (after scanning the menu or before).

---

## Planned Response

- **US-001** (Propose dishes according to the budget): priority changed from MUST → SHOULD; removed from initial proposed MVP v1 scope.
- **US-006** (High speed of the search system): priority changed from SHOULD → COULD.
- **US-002** (Ability to sign in): removed from initial proposed MVP v1 scope.
- **Recommendation screen UI:** like/dislike buttons removed; replaced with "I will order this" and "Dismiss, another option" — affects Figma prototype: https://www.figma.com/proto/BK4oKfBZo6r8RxjTanLQ3z/Untitled?node-id=0-1&t=3PdFw5wmGupLDKLm-1
