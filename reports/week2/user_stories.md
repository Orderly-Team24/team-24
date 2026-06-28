# Project Description

A website which, based on your preferences, budget, allergies, and the photo of a menu, gives you top-3 best dishes.

# User Roles / Personas

## Authorized User
A registered user who can log in, specify preferences, allergies, and budget, and receive personalized dish recommendations.

## Unauthorized User
A visitor who has not signed in yet and needs to authenticate before accessing personalized features.

## Administrator
A system administrator who monitors application usage and analyzes recommendation statistics.

# User Stories

## US-001: Propose dishes according to the budget

**Requirement status:** Active  
**MoSCoW priority:** Should Have

As an authorized user,
I want to order a dish according to my budget,
so that I do not need to calculate prices manually.

### Notes and constraints

The user provides a maximum budget for recommendations.

---

## US-002: Ability to sign in

**Requirement status:** Active  
**MoSCoW priority:** Must Have

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

**Requirement status:** Active  
**MoSCoW priority:** Must Have

As an authorized user who loves specific food,
I want to receive dish recommendations based on my preferences,
so that I can enjoy the suggested meals.

### Notes and constraints

Preferences may include favorite cuisines or ingredients.

---

## US-005: No allergen suggestions

**Requirement status:** Active  
**MoSCoW priority:** Must Have

As an authorized user with allergies,
I want allergen-containing dishes to be excluded from recommendations,
so that I can eat safely.

### Notes and constraints

Users should be able to specify their allergens.

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

**Requirement status:** Active  
**MoSCoW priority:** Should Have

As an authorized user,
I want to mark dishes that I dislike,
so that they are not recommended again.

### Notes and constraints

Disliked dishes should influence future recommendations.

---

## US-008: Save liked dishes to history

**Requirement status:** Active  
**MoSCoW priority:** Should Have

As an authorized user,
I want to save dishes to my history,
so that I can remember and order them again later.

### Notes and constraints

History should be associated with the user's account.

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

**Requirement status:** Active   
**MoSCoW priority:** Must  

As an authorized user, 
I want to upload photo of a menu from the gallery,
so that I can receive a recommendation.

### Noteas and constraints
User should upload photo, then we need to extract dish names and prices

---

# Initial proposed MVP v1 scope
- US-011

## Scope change log

All changes below were made during or immediately after the customer meeting on **11 Jun 2026**.
Evidence: [Customer Meeting Summary](customer-meeting-summary.md) · [Customer Meeting Transcript](customer-meeting-transcript.md)

| Story | Change | Customer evidence |
|-------|--------|-------------------|
| US-001 – Budget | **Priority MUST → SHOULD.** Removed from MVP v1 scope. | Customer explicitly stated: *"Proposing dishes according to the budget is not a MUST, but SHOULD"* (Decisions section). Budget setting deferred after onboarding questionnaire in a later sprint. |
| US-002 – Sign in | **Removed from MVP v1 scope.** Marked Active but deferred. | Customer explicitly stated: *"No sign-in for the first version of the project"* (Decisions section). Authentication blocks the core recommendation flow and adds complexity; customer accepted deferral. |
| US-004 – Preferences | **Deferred from MVP v1.** Allergen and preference input will be added once the core upload-and-recommend flow is proven. | Customer prioritised the photo upload flow (US-011) as the single core value for MVP v1. US-004 was agreed as the next priority after delivery of US-011. |
| US-005 – No allergens | **Deferred from MVP v1.** Same rationale as US-004; allergen filtering depends on structured preferences input. | Customer confirmed that a working photo-to-recommendation pipeline (US-011) is the MVP v1 deliverable. Allergen safety is Sprint 2 scope. |
| US-006 – High speed | **Priority SHOULD → COULD.** | Customer explicitly stated: *"High speed of the search system is not a SHOULD, but COULD"* (Decisions section). |
| US-011 – Upload photo | **Added to MVP v1 scope as the sole deliverable.** | Customer validated this as the core differentiating feature during the meeting. The minimum viable product is: upload a menu photo → receive a dish recommendation. |
