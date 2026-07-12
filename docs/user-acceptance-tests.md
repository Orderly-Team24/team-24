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

---

## UAT-06 — End Session
**Related US:** [US-014 – Button "End session"](https://github.com/Orderly-Team24/team-24/issues/148)
**Precondition:** The app is deployed and accessible at https://team-24-navy.vercel.app/. The user is signed in and has reached the recommendation page (Step 3 of 3).

**Steps:**
1. On the recommendation page, click **"End session"**.
2. Observe the redirect.
3. Try to navigate back to `/food-recommender`.

**Expected result:**
- The user is redirected to `/upload` (the menu upload page).
- Session data is cleared from `localStorage`.
- Auth tokens are NOT cleared — the user remains logged in.
- Navigating back to `/food-recommender` starts a fresh session with no stale data.
- No error message is shown.

**Status history:**
| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |

---

## UAT-07 — Specify Today's Meal Intent Alongside Budget
**Related US:** [US-018 – Specify today's meal intent alongside budget](https://github.com/Orderly-Team24/team-24/issues/222)
**Precondition:** The app is deployed and accessible at https://team-24-navy.vercel.app/. The user is signed in and has reached the Budget & Menu Photo page (Step 2 of 3).

**Steps:**
1. On the Budget & Menu Photo page, locate the optional **"What are you in the mood for today?"** field.
2. Leave it empty and proceed to get a recommendation.
3. Go back and repeat, this time filling in the mood field (e.g. "something warm and light").
4. Proceed to get a recommendation.
5. Click **"End session"** and check if the mood field is cleared.

**Expected result:**
- The mood field is visible, optional, and shows the correct placeholder text.
- When left empty, the recommendation behaves as usual based on saved preferences.
- When filled, the recommendation reason reflects the entered craving.
- Clicking "End session" clears the mood field.
- No error message is shown in either case.

**Status history:**
| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 3 | <!-- fill after UAT --> | Customer | <!-- Pass / Fail --> | <!-- notes --> |

---

## UAT-08 — View Order History and Dislike a Dish

**Related US:** [US-015 – Managing history of orders](https://github.com/Orderly-Team24/team-24/issues/149)

**Precondition:** The app is deployed and accessible at https://team-24-navy.vercel.app/. The user is signed in.

**Steps:**
1. Reach the recommendation page and click **"I'll order it"** on a dish.
2. Click **"History"** in the top navigation.
3. Locate the dish just ordered in the list.
4. Click **"Dislike"** on that dish.
5. Go back and click **"Another option"** a few times from the same menu.

**Expected result:**
- The History page loads and shows the ordered dish (name, price, order date if available) — not a blank page.
- Clicking "Dislike" shows a brief "Saving…" state, then relabels the button "Disliked ✓" and greys out the card, without a full page reload.
- The disliked dish is never returned by "Another option" or future recommendations for this account.

**Status history:**
| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 4 | 10.07.2026 | Customer | **PASSED** | Verified ordering a dish, disliking it from History with a non-reloading "Saving…" → "Disliked ✓" transition and greyed-out card, then confirmed via "Another option" that the disliked dish never reappears. |

---

## UAT-09 — AI Never Recommends an Excluded or Allergen Food

**Related US:** [US-005 – No allergen suggestions](https://github.com/Orderly-Team24/team-24/issues/59)

**Precondition:** The app is deployed. The user is signed in with at least one allergy saved on the Profile page (e.g. "shellfish").

**Steps:**
1. Confirm an allergy (e.g. "shellfish") is saved on the Profile page.
2. Get a recommendation from a menu that includes both shellfish and non-shellfish dishes.
3. In the "What are you in the mood for today?" field, type a plain-language exclusion that is NOT one of your saved allergies (e.g. "I don't want steak").
4. Get a recommendation from a menu that includes steak and at least one alternative.
5. Repeat with a menu where every dish contains the excluded/allergen ingredient.

**Expected result:**
- The recommended dish never contains the saved allergen ingredient.
- The recommended dish never contains the food named as unwanted in the mood field, even though it wasn't entered as a formal allergy.
- If every available dish contains the excluded ingredient, the app shows no recommendation rather than recommending an unsafe dish.

**Status history:**
| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 4 | 10.07.2026 | Customer | **PASSED** | Verified recommendations exclude both formal (Profile) allergies and mood-field exclusions, and that the app shows no recommendation when every candidate dish is forbidden. |

---

## UAT-10 — AI Recognizes Meal Type and Never Recommends a Drink as the Dish

**Related US:** [US-018 – Specify today's meal intent alongside budget](https://github.com/Orderly-Team24/team-24/issues/222)

**Precondition:** The app is deployed. The user is signed in and has reached the Budget & Menu Photo page.

**Steps:**
1. In the "What are you in the mood for today?" field, type "something for breakfast".
2. Get a recommendation from a menu that includes both breakfast-style dishes (e.g. pancakes, eggs) and non-breakfast dishes (e.g. steak).
3. Repeat with a menu that also includes a beverage-only item (e.g. "Water", "Orange juice").

**Expected result:**
- When a breakfast-appropriate dish is available on the menu, it is recommended over a dinner-style dish.
- A beverage-only item (water, juice, soda, coffee, etc.) is never returned as the recommended dish — the recommendation is always an actual meal.

**Status history:**
| Sprint | Date | Executed by | Result | Notes |
|--------|------|-------------|--------|-------|
| Sprint 4 | 10.07.2026 | Customer | **PASSED** | Confirmed "something for breakfast" prioritized breakfast dishes over dinner options, and a beverage-only item was never returned as the recommendation. Customer separately flagged meal-type filtering as feeling unstable more broadly beyond this specific script — tracked as a Sprint 5 follow-up action item, not a failure of this scenario. |
