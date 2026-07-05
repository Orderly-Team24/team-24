diff --git a/docs/user-acceptance-tests.md b/docs/user-acceptance-tests.md
index 5673452..470da46 100644
--- a/docs/user-acceptance-tests.md
+++ b/docs/user-acceptance-tests.md
@@ -39,21 +39,22 @@ UAT scenarios are maintained product assets. Results are recorded per Sprint exe
 **Precondition:** The app is deployed. The user has completed the questionnaire and reached the recommendation page.
 
 **Steps:**
-1. Complete UAT-01 or UAT-02 to reach the recommendation page.
+1. Complete UAT-01 or UAT-03 to reach the recommendation page.
 2. Click the **"I'll order this dish"** button on the recommendation card.
-3. Observe the message that appears.
+3. Observe the button and the card.
 
 **Expected result:**
-- A confirmation message "Bon appétit!" is displayed.
+- The button label changes to **"Saved ✓"** and becomes disabled (can't be clicked twice).
 - No error message is shown.
-- The dish is NOT saved to order history (this feature is not implemented yet).
-- The button remains clickable and can be pressed again.
+- The dish is saved to the user's order history via `POST /history/orders` (verifiable through `GET /history/orders` with the same `X-User-Id`).
+- There is currently no dedicated page in the app to *view* this history — that lands with US-015 (Managing history of orders), planned for next sprint.
 
 **Status history:**
 
 | Sprint | Date | Executed by | Result | Notes |
 |--------|------|-------------|--------|-------|
-| Sprint 2 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+| Sprint 2 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | Originally written when order history wasn't implemented yet. |
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | Re-verify now that saving to history is live. |
 
 ---
 
@@ -82,3 +83,177 @@ UAT scenarios are maintained product assets. Results are recorded per Sprint exe
 | Sprint | Date | Executed by | Result | Notes |
 |--------|------|-------------|--------|-------|
 | Sprint 2 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+
+---
+
+## UAT-04 — Account Registration
+
+**Related US:** [US-002-6 – Implement user registration](https://github.com/Orderly-Team24/team-24/issues/216)
+
+**Precondition:** The app is deployed and accessible at https://team-24-navy.vercel.app/. The tester has a fresh, unused email address.
+
+**Steps:**
+1. Navigate to `/register` (e.g. via "Create account" link from the login page).
+2. Fill in email, username, password, and confirm password.
+3. Click **"Next: Set preferences →"**.
+4. Observe where the app navigates to.
+
+**Expected result:**
+- No error message is shown for valid, matching passwords.
+- The user is redirected to the preferences questionnaire (`/`).
+- The user is already signed in at this point (an access token has been issued) — reloading `/login` should redirect straight to `/upload` instead of showing the login form again.
+
+**Status history:**
+
+| Sprint | Date | Executed by | Result | Notes |
+|--------|------|-------------|--------|-------|
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+
+---
+
+## UAT-05 — Sign In With Existing Account
+
+**Related US:** [US-002 – Ability to sign in](https://github.com/Orderly-Team24/team-24/issues/63)
+
+**Precondition:** The app is deployed. An account already exists (e.g. created via UAT-04).
+
+**Steps:**
+1. Navigate to `/login`.
+2. Enter the correct email and password.
+3. Click **"Sign in"**.
+4. Repeat with an incorrect password.
+
+**Expected result:**
+- With correct credentials: the user is redirected to `/upload`, skipping the questionnaire (their saved preferences are loaded automatically in the background).
+- With an incorrect password: an inline error message is shown (e.g. "Invalid email or password."); the user stays on `/login`.
+- No unhandled crash or blank page in either case.
+
+**Status history:**
+
+| Sprint | Date | Executed by | Result | Notes |
+|--------|------|-------------|--------|-------|
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+
+---
+
+## UAT-06 — End Session
+
+**Related US:** [US-014 – Button "End session"](https://github.com/Orderly-Team24/team-24/issues/148)
+
+**Precondition:** The app is deployed. The user has reached the recommendation page (with or without being signed in).
+
+**Steps:**
+1. Complete UAT-01 or UAT-03 to reach the recommendation page.
+2. Click the **"End session"** button.
+3. Observe where the app navigates to.
+4. Navigate back to `/upload` manually.
+
+**Expected result:**
+- The user is redirected to `/` (the questionnaire).
+- The previously selected budget, mood, and uploaded menu are cleared — returning to `/upload` shows an empty budget/mood field and no photo preview.
+- If the user was signed in, they are signed out (tokens cleared) — navigating to `/profile` should not show their data / should require signing in again.
+
+**Status history:**
+
+| Sprint | Date | Executed by | Result | Notes |
+|--------|------|-------------|--------|-------|
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+
+---
+
+## UAT-07 — Delete Account
+
+**Related US:** [US-017 – Delete account](https://github.com/Orderly-Team24/team-24/issues/221)
+
+**Precondition:** The app is deployed. The tester is signed in to a disposable test account (do not use a real/shared account — this is irreversible).
+
+**Steps:**
+1. Navigate to `/profile`.
+2. Click **"Delete account"**.
+3. On the confirmation prompt, click **"Yes, delete my account"**.
+4. Try to sign in again with the same credentials.
+
+**Expected result:**
+- A confirmation step is shown before deletion (clicking "Delete account" alone must NOT delete immediately).
+- After confirming, the user is redirected to `/register` and all local session data is cleared.
+- Signing in again with the deleted account's credentials fails with an error (account no longer exists).
+
+**Status history:**
+
+| Sprint | Date | Executed by | Result | Notes |
+|--------|------|-------------|--------|-------|
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+
+---
+
+## UAT-08 — Specify Today's Meal Intent Alongside Budget
+
+**Related US:** [US-018 – Specify today's meal intent alongside budget](https://github.com/Orderly-Team24/team-24/issues/222)
+
+**Precondition:** The app is deployed. The user has completed the questionnaire and reached the budget/menu page (`/upload`).
+
+**Steps:**
+1. On `/upload`, enter a budget (e.g. `20`).
+2. In the **"What are you in the mood for today?"** field, enter a specific intent (e.g. `warm soup`).
+3. Click **"Skip photo — use default menu →"**.
+4. Observe the recommendation returned.
+
+**Expected result:**
+- A recommendation is returned within budget.
+- The recommended dish is plausibly related to the stated mood (e.g. a soup, when the underlying menu has one) more often than not — this is a soft/AI-dependent check, not a strict guarantee.
+- No error is shown when the mood field is left blank (it's optional).
+
+**Status history:**
+
+| Sprint | Date | Executed by | Result | Notes |
+|--------|------|-------------|--------|-------|
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+
+---
+
+## UAT-09 — Preferences Still Applied When Budget Is Set
+
+**Related US/Fix:** [Fix: preferences ignored when max_budget is set in display_recommendations.py – Issue #218](https://github.com/Orderly-Team24/team-24/issues/218)
+
+**Precondition:** The app is deployed. The tester has an account (or local preferences) with at least one entry in "Dislikes" or "Allergies", and a menu that contains both matching and non-matching dishes.
+
+**Steps:**
+1. On the questionnaire, add an ingredient to "Dislikes" or "Allergies" that appears in the default/uploaded menu (e.g. `mushrooms`).
+2. Proceed to `/upload`, set a budget that several dishes fit within (both dishes with and without the disliked ingredient).
+3. Skip photo / use default menu, or upload a menu photo.
+4. Observe the recommended dish.
+
+**Expected result:**
+- The recommended dish respects BOTH constraints at once: it is within budget AND does not contain the disliked/allergen ingredient.
+- This is a regression check for a bug where setting a budget caused preference filtering to be silently skipped.
+
+**Status history:**
+
+| Sprint | Date | Executed by | Result | Notes |
+|--------|------|-------------|--------|-------|
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
+
+---
+
+## UAT-10 — Menu Photo Upload and OCR Extraction
+
+**Related US/Fix:** [Fix: OCR broken in both backend services – Issue #219](https://github.com/Orderly-Team24/team-24/issues/219)
+
+**Precondition:** The app is deployed. The tester has a clear photo of a real restaurant menu (JPEG or PNG, under 8 MB).
+
+**Steps:**
+1. On `/upload`, click **"Choose Menu Photo"** and select the photo.
+2. Click **"Send for processing"**.
+3. Wait for processing to complete.
+4. Observe the outcome and the resulting recommendation.
+
+**Expected result:**
+- The upload does not fail with a 500 error or a generic "Upload failed" message.
+- The app proceeds to the recommendation page with a dish drawn from the uploaded menu (not silently falling back to the default menu without indication).
+- If OCR quality is poor (blurry photo, stylized fonts), the app should still return *something* rather than crash — worth noting in results if dish names/descriptions look garbled.
+
+**Status history:**
+
+| Sprint | Date | Executed by | Result | Notes |
+|--------|------|-------------|--------|-------|
+| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |
