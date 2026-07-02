# Project Description

A website which, based on your preferences, budget, allergies, and a photo of a menu, recommends the best matching dish. Users can request another option if the first suggestion does not suit them.

# User Roles / Personas

## Authorized User
A registered user who can log in, specify preferences, allergies, and budget, and receive personalized dish recommendations.

## Unauthorized User
A visitor who has not signed in yet and needs to authenticate before accessing personalized features.

## Administrator
A system administrator who monitors application usage and analyzes recommendation statistics.

# User Stories

## US-001: Propose dishes according to the budget

**Requirement status:** Delivered (Sprint 2)
**MoSCoW priority:** Should Have
**GitHub:** [#57](https://github.com/Orderly-Team24/team-24/issues/57)

As an authorized user,
I want to order a dish according to my budget,
so that I do not need to calculate prices manually.

### Notes and constraints

The user provides a maximum budget for recommendations.

---

## US-002: Ability to sign in

**Requirement status:** Active (Sprint 3)
**MoSCoW priority:** Must Have
**GitHub:** [#63](https://github.com/Orderly-Team24/team-24/issues/63) · sub-tasks: [#74](https://github.com/Orderly-Team24/team-24/issues/74) [#76](https://github.com/Orderly-Team24/team-24/issues/76) [#77](https://github.com/Orderly-Team24/team-24/issues/77) [#78](https://github.com/Orderly-Team24/team-24/issues/78) [#79](https://github.com/Orderly-Team24/team-24/issues/79) [#216](https://github.com/Orderly-Team24/team-24/issues/216)

As an unauthorized user,
I want to sign in to the application,
so that I can access all available features.

### Notes and constraints

Authentication is required for personalized recommendations.

---

## US-003: Guarantee safety of user information

**Requirement status:** Active
**MoSCoW priority:** Could Have

As an authorized user,
I want my information to be encrypted,
so that I can feel safe using the application.

### Notes and constraints

Personal data should be stored securely.

---

## US-004: Propose dishes according to preferences

**Requirement status:** Delivered (Sprint 2)
**MoSCoW priority:** Must Have
**GitHub:** [#64](https://github.com/Orderly-Team24/team-24/issues/64)

As an authorized user who loves specific food,
I want to receive dish recommendations based on my preferences,
so that I can enjoy the suggested meals.

### Notes and constraints

Preferences may include favorite cuisines or ingredients.

---

## US-005: No allergen suggestions

**Requirement status:** Removed — merged into US-004
**MoSCoW priority:** Must Have

As an authorized user with allergies,
I want allergen-containing dishes to be excluded from recommendations,
so that I can eat safely.

### Notes and constraints

Allergen filtering was merged into US-004 (preferences) in Sprint 2. Allergies are now a field in the preferences questionnaire filled during registration.

---

## US-006: High speed of the search system

**Requirement status:** Active
**MoSCoW priority:** Could Have

As an authorized user,
I want to quickly search for appropriate dishes in the menu,
so that my friends would not have to wait for me.

### Notes and constraints

Search results should be displayed with minimal delay.

---

## US-007: Reject and hide dislikes

**Requirement status:** Removed — superseded by US-015
**MoSCoW priority:** Should Have

As an authorized user,
I want to mark dishes that I dislike,
so that they are not recommended again.

### Notes and constraints

Replaced by US-015 which scopes disliking to dishes already in the user's order history, so the dislike is grounded in real experience rather than upfront input.

---

## US-008: Save liked dishes to history

**Requirement status:** Removed — superseded by US-012
**MoSCoW priority:** Should Have

As an authorized user,
I want to save dishes to my history,
so that I can remember and order them again later.

### Notes and constraints

Replaced by US-012 which makes the intent explicit: user saves what they intend to order via "I'll order it" button, not just liked dishes.

---

## US-009: Save the prices of ordered items

**Requirement status:** Active
**MoSCoW priority:** Could Have

As an authorized user,
I want to keep track of the dishes I purchase,
so that I can control my budget.

### Notes and constraints

The application may store past order costs.

---

## US-010: Admin functions for analysis

**Requirement status:** Active
**MoSCoW priority:** Could Have

As an admin,
I want to see usage frequency statistics,
so that I can analyze the product relevance.

### Notes and constraints

Only administrators should have access to analytics.

---

## US-011: Upload photo of a menu

**Requirement status:** Delivered (Sprint 1)
**MoSCoW priority:** Must Have
**GitHub:** [#62](https://github.com/Orderly-Team24/team-24/issues/62)

As an authorized user,
I want to upload a photo of a menu from the gallery,
so that I can receive a recommendation.

### Notes and constraints
User uploads a photo; OCR extracts the text; the parser structures it into a list of dishes with prices.

---

## US-012: Save ordered dish to history

**Requirement status:** Delivered (Sprint 2)
**MoSCoW priority:** Should Have
**GitHub:** [#146](https://github.com/Orderly-Team24/team-24/issues/146)

As an authorized user,
I want to save a dish I am going to order,
so that I can see my order history later.

### Notes and constraints
Dish is saved to history only when the user explicitly clicks "I'll order it". The recommendation itself is not saved automatically.

---

## US-013: Request another recommendation

**Requirement status:** Delivered (Sprint 2)
**MoSCoW priority:** Should Have
**GitHub:** [#147](https://github.com/Orderly-Team24/team-24/issues/147)

As an authorized user,
I want to request another dish recommendation,
so that I can choose a different option if the first suggestion does not suit me.

### Notes and constraints
Each additional request passes a different prompt variation to the AI so it does not return the same dish twice in the same session. Already-shown dishes are tracked server-side per session.

---

## US-014: End session

**Requirement status:** Active (Sprint 3)
**MoSCoW priority:** Should Have
**GitHub:** [#148](https://github.com/Orderly-Team24/team-24/issues/148)

As an authorized user,
I want to end my session at any moment,
so that I can safely stop using the application and clear my temporary data.

### Notes and constraints
Ending a session clears the current menu, budget, and meal intent. Saved preferences and order history are not affected.

---

## US-015: Dislike ordered dish

**Requirement status:** Active (Sprint 3)
**MoSCoW priority:** Should Have
**GitHub:** [#149](https://github.com/Orderly-Team24/team-24/issues/149)

As an authorized user,
I want to mark a dish I have ordered as disliked,
so that it is not recommended to me again.

### Notes and constraints
The dislike is stored per user in the backend. The recommender filters out disliked dishes before returning a recommendation.

---

## US-016: Edit preferences and allergies in profile

**Requirement status:** Active (Sprint 3)
**MoSCoW priority:** Must Have
**GitHub:** [#220](https://github.com/Orderly-Team24/team-24/issues/220)

As an authorized user,
I want to view and edit my preferences and allergies in my profile,
so that my recommendations stay relevant as my tastes change.

### Notes and constraints
Preferences are set once during registration and stored in the user profile. The profile page allows editing them at any time. Changes take effect on the next recommendation session.

---

## US-017: Delete account

**Requirement status:** Active (Sprint 3)
**MoSCoW priority:** Should Have
**GitHub:** [#221](https://github.com/Orderly-Team24/team-24/issues/221)

As an authorized user,
I want to delete my account,
so that all my personal data is permanently removed from the system.

### Notes and constraints
Deletion removes credentials, preferences, order history, and disliked dishes. The action is irreversible and requires confirmation.

---

## US-018: Specify today's meal intent

**Requirement status:** Active (Sprint 3)
**MoSCoW priority:** Must Have
**GitHub:** [#222](https://github.com/Orderly-Team24/team-24/issues/222)

As a user,
I want to describe what I feel like eating today alongside my budget,
so that the recommendation matches both my current craving and my saved preferences.

### Notes and constraints
This is a per-session input — not saved to the user profile. The field is optional; if left empty, the recommender uses saved preferences only.

---

# Initial proposed MVP v1 scope
- US-011

## Scope change log

### Customer meeting — 11 Jun 2026
Evidence: [Customer Meeting Summary](customer-meeting-summary.md) · [Customer Meeting Transcript](customer-meeting-transcript.md)

| Story | Change | Customer evidence |
|-------|--------|-------------------|
| US-001 – Budget | **Priority MUST → SHOULD.** Removed from MVP v1 scope. | Customer explicitly stated: *"Proposing dishes according to the budget is not a MUST, but SHOULD"* (Decisions section). |
| US-002 – Sign in | **Removed from MVP v1 scope.** Marked Active but deferred. | Customer explicitly stated: *"No sign-in for the first version of the project"* (Decisions section). |
| US-004 – Preferences | **Deferred from MVP v1.** | Customer prioritised the photo upload flow (US-011) as the single MVP v1 deliverable. US-004 agreed as next priority after US-011. |
| US-005 – No allergens | **Deferred from MVP v1.** Same rationale as US-004. | Customer confirmed US-011 is the MVP v1 deliverable; allergen safety is Sprint 2 scope. |
| US-006 – High speed | **Priority SHOULD → COULD.** | Customer explicitly stated: *"High speed of the search system is not a SHOULD, but COULD"* (Decisions section). |
| US-011 – Upload photo | **Added to MVP v1 scope as the sole deliverable.** | Customer validated this as the core differentiating feature. |

### Sprint 2 — 22 Jun 2026

| Story | Change | Reason |
|-------|--------|--------|
| US-005 – No allergens | **Removed.** Merged into US-004. | Allergen filtering is a field within the preferences model; keeping a separate story created duplicate scope. |
| US-007 – Reject and hide dislikes | **Removed.** Superseded by US-015. | US-015 scopes disliking to ordered dishes, grounding it in real experience rather than upfront input. |
| US-008 – Save liked dishes | **Removed.** Superseded by US-012. | US-012 makes the intent explicit: user saves what they intend to order via "I'll order it" button. |
| US-012 – Save ordered dish | **Added.** | Emerged from Sprint 2 implementation: "I'll order it" button as the explicit history-saving action. |
| US-013 – Another option | **Added.** | Customer feedback: users want to compare dishes before deciding. |

### Sprint 3 — 29 Jun 2026

| Story | Change | Reason |
|-------|--------|--------|
| US-002 – Sign in | **Re-scoped into active sprint.** Sub-tasks #74–#79, #216 created. | Core recommendation flow is proven; auth is the next logical step. |
| US-014 – End session | **Added.** | Needed to cleanly terminate a session and clear temporary data. |
| US-015 – Dislike ordered dish | **Added.** | Closes the recommendation feedback loop: disliked dishes are excluded from future recommendations. |
| US-016 – Edit preferences in profile | **Added.** | Preferences must be editable after registration; without this users are locked into their initial choices. |
| US-017 – Delete account | **Added.** | Users must be able to remove all their personal data. |
| US-018 – Specify today's meal intent | **Added.** | Per-session free-text input lets users fine-tune the recommendation beyond their saved preferences. |
