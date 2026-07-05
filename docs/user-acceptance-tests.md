# User Acceptance Tests

UAT scenarios are maintained product assets. Results are recorded per Sprint execution.

---

## UAT-01 — Budget-Filtered Recommendation

**Related US:** [US-001 – Propose dishes according to the budget](https://github.com/Orderly-Team24/team-24/issues/57)

**Precondition:** The app is deployed and accessible at https://team-24-navy.vercel.app/

**Steps:**
1. Open the app. The questionnaire page loads automatically.
2. Select a cuisine type (e.g. Italian).
3. Click "No allergies" (or select specific allergies).
4. Click **"Next: Upload Menu →"**.
5. On the Budget & Menu Photo page, enter a max budget (e.g. `15`).
6. Click **"Skip photo — use default menu →"**.
7. Wait for the recommendation to load.

**Expected result:**
- A recommendation card is displayed.
- The recommended dish price is ≤ $15.
- No error or "Failed to fetch" message is shown.

**Status history:**

| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 2 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |

---

## UAT-02 — Order Dish Confirmation

**Related US:** [US-012 – Button "I'll order this dish"](https://github.com/Orderly-Team24/team-24/issues/146)

**Precondition:** The app is deployed. The user has completed the questionnaire and reached the recommendation page.

**Steps:**
1. Complete UAT-01 or UAT-02 to reach the recommendation page.
2. Click the **"I'll order this dish"** button on the recommendation card.
3. Observe the message that appears.

**Expected result:**
- A confirmation message "Bon appétit!" is displayed.
- No error message is shown.
- The dish is NOT saved to order history (this feature is not implemented yet).
- The button remains clickable and can be pressed again.

**Status history:**

| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 2 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |

---

## UAT-03 — View Another Recommendation Option

**Related US:** [US-013 – Button "Another option"](https://github.com/Orderly-Team24/team-24/issues/147)

**Precondition:** The app is deployed. The user has completed the questionnaire and reached the recommendation page.

**Steps:**
1. Complete UAT-01 or UAT-02 to reach the recommendation page.
2. Click the **"Another option"** button below the recommendation card.
3. Wait for the new recommendation to load.
4. Observe the new dish recommendation.
5. Repeat steps 2-4 two more times.

**Expected result:**
- A new dish recommendation is displayed each time.
- The new dish is different from the previous recommendation(s).
- The dish price still respects the user's budget constraint.
- No error or "Failed to fetch" message is shown.
- The button remains functional for multiple uses.

**Status history:**

| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 2 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |

---

## UAT-04 — Sign In With Existing Account

**Related US:** [US-002 – Ability to sign in](https://github.com/Orderly-Team24/team-24/issues/63)

**Precondition:** The app is deployed and accessible at https://team-24-navy.vercel.app/. An account already exists (e.g. created via the registration page).

**Steps:**
1. Navigate to `/login`.
2. Enter the correct email and password.
3. Click **"Sign in"**.
4. Repeat with an incorrect password.

**Expected result:**
- With correct credentials: the user is redirected to `/upload`, skipping the questionnaire (their saved preferences are loaded automatically in the background).
- With an incorrect password: an inline error message is shown (e.g. "Invalid email or password."); the user stays on `/login`.
- No unhandled crash or blank page in either case.

**Status history:**

| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |

---

## UAT-05 — Delete Account

**Related US:** [US-017 – Delete account](https://github.com/Orderly-Team24/team-24/issues/221)

**Precondition:** The app is deployed. The tester is signed in to a disposable test account (do not use a real/shared account — this is irreversible).

**Steps:**
1. Navigate to `/profile`.
2. Click **"Delete account"**.
3. On the confirmation prompt, click **"Yes, delete my account"**.
4. Try to sign in again with the same credentials.

**Expected result:**
- A confirmation step is shown before deletion (clicking "Delete account" alone must NOT delete immediately).
- After confirming, the user is redirected to `/register` and all local session data is cleared.
- Signing in again with the deleted account's credentials fails with an error (account no longer exists).

**Status history:**

| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
