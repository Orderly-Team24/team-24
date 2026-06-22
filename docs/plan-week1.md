# Plan — next 4 weeks (4 work weeks → defense on week 5)

**Source:** `docs/user-stories.md` (updated 2026-06-22).
**Today:** Mon 2026-06-22.

## Team

| Person | Area |
|---|---|
| Vika, Vilena | Frontend (everything) |
| Dasha, Polina, Adelina | AI: model, prompts, recommendations, parser-binding |
| Omar | Other backend (endpoints, DB, auth), deployment (except documentation) |

## Sprint map

| Sprint | Dates (4 weeks → defense) | Goal | Stories |
|---|---|---|---|
| W1 | 22-06 – 28-06 | Close US-011 leftovers + start recommendations | US-011-2, US-011-3, US-004 |
| W2 | 29-06 – 05-07 | Login + UI buttons | US-002 (1..5), US-012, US-013, US-014, US-015 |
| W3 | 06-07 – 12-07 | Budget + finish login | US-001, remaining US-002 |
| W4 | 13-07 – 19-07 | Polish, bugfix, defense | — |

> W5 = defense. All Must stories must be closed by end of W3.

---

## Week 1 — 22-06 … 28-06

**Goal:** close US-011 entirely (already ~80% done) and start US-004.

### Tasks

| ID | Story | MoSCoW | Subtask | Owner | SP | What we do | Definition of Done |
|---|---|---|---|---|---|---|---|
| **US-011-2** | OCR | 🔴 Must | — | Adelina | 3 | E2E on 3 menu photos (clean / noisy / EN+RU), negative cases 413/415/422 | Photo fixtures in `tests/fixtures/`, pytest green, README updated, PR `feat/ocr-real-photos` merged |
| **US-011-3** | Parsing | 🔴 Must | — | Polina | 3 | Migrate `test_parser.py` to pytest, cover 8 cases (4 price formats, no price, separators, empty line, multiple prices) | `src/backend/tests/test_parser.py` ≥ 8 cases, all green, contract documented, PR `feat/menu-parser-skeleton` merged |
| **US-004-1** | Preferences: API contract | 🔴 Must | US-004 | Omar | 1 | Extend `RecommendationRequest`: add Pydantic `Preferences{cuisine, exclude_ingredients, favorite_ingredients}`, keep legacy `message` | Parsing unit test, backward compat with current frontend |
| **US-004-2** | Preferences: prompt + stub | 🔴 Must | US-004 | Dasha + Adelina | 2 | Honour `Preferences` in `_openai()` and stub-filter `_FALLBACK_POOL` by `exclude_ingredients`/cuisine | Locally: `cuisine="italian"` → italian dish; `exclude=["nuts"]` → no nuts; fallback to full pool on empty |
| **US-004-3** | Preferences: UI | 🔴 Must | US-004 | Vika | 1 | Form: cuisine select + "dislike"/"like" chips, send `{preferences: {...}}` to POST `/recommendations` | Form renders, card changes on cuisine switch, empty preferences = current behaviour |
| **US-004-4** | Preferences: parser-binding | 🔴 Must | US-004 | Dasha + Polina | 1 | Endpoint accepts `dishes` from `parser.py`, filters by `exclude_ingredients`, picks from list | E2E: photo → parse → `exclude=["nuts"]` → dish without nuts; empty result → 200 with `[]`, not 500 |
| **US-004-5** | Preferences: docs | 🔴 Must | US-004 | Vika + Vilena | 0.5 | Section in `src/backend/README.md` with curl example + UI screenshot in `docs/screenshots/us-004.png` | README contains example, screenshot attached to PR |

**W1 total:** 11.5 SP (US-004-4 waits for US-011-3; US-004-3 parallel to US-004-2)

**US-001 — W3 (Should):**

| ID | Story | MoSCoW | Subtask | Owner | SP | What we do | Definition of Done |
|---|---|---|---|---|---|---|---|
| **US-001-1** | Budget: API + filter | 🟠 Should | US-001 | Omar | 1 | Field `max_budget: float \| None` in `Preferences`, backend filter `price <= max_budget` | Unit test: `max_budget=10` excludes a dish with `price=12`; empty after filter → 200 with `[]` |
| **US-001-2** | Budget: UI | 🟠 Should | US-001 | Vilena | 1 | "Max budget" field with validation (>0), message "No dishes under $X" on empty response | Field works, client-side validation, message shown |
| **US-001-3** | Budget: E2E + docs | 🟠 Should | US-001 | Vilena + Omar | 1 | E2E: budget=10 + cuisine=italian → card ≤ $10, curl example in README, screenshot | E2E passed, README updated |

### Parallel work (does not block W1, but needed)

- **Omar:** spin up Postgres on Render for the future US-002 (login). Free tier. No schema yet — only the instance + env variables.
- **Vika, Vilena:** prepare mockups for US-002-1 (login) and US-012-014 (buttons). Figma/paper — doesn't matter, lock it down before W2 starts.

### W1 risks

1. **OCR on real photos** may work poorly — Polina+Dasha may get stuck. Plan B: plug in OCR.space as a fallback (free API).
2. **US-004 without owner** — if Polina+Adelina don't pick it up in the first 2 days, W2's login has nothing to base on (user is needed for preferences).

### W1 PR plan

- `feat/ocr-real-photos` → `main` (Adelina)
- `feat/menu-parser-skeleton` → `main` (Polina)
- `feat/recommend-by-preferences` → `main` (Dasha + Adelina)
- `chore/postgres-render-setup` → `main` (Omar)

---

## Week 2 — 29-06 … 05-07

**Goal:** login in full + UI buttons.

### Tasks

| # | Story | Owner | Notes |
|---|---|---|---|
| 4 | US-002-1 Login page | Vika | Email/password form, no backend yet (mocks) |
| 5 | US-002-2 Client-side validation | Vilena | Bind to US-002-1 |
| 6 | US-002-3 Password verification (backend) | Dasha | Endpoint `POST /auth/login` |
| 7 | US-002-4 JWT | Omar | **Critical.** Don't write from scratch — use `fastapi-users` or equivalent |
| 8 | US-002-5 Redirect after login | Vilena | localStorage token, redirect to /display/recommendations |
| 9 | US-002-6 Registration (signup) | Dasha | Backend: `POST /auth/register` (hash + store). Frontend: signup form, **separate from login page** |
| 9 | US-012 "I'll order dish" button | Vika | Small feature, ~2-3h |
| 10 | US-013 "Another option" button | Vilena | ~2-3h |
| 11 | US-014 "End session" button | Vika | Resets the session, ~2h |
| 12 | US-015 Managing order history | Vilena + Vika | UI + backend binding |

---

## Week 3 — 06-07 … 12-07

**Goal:** budget + finish login.

### Tasks

| ID | Story | Owner |
|---|---|---|
| **US-001-1** | Budget: API + filter | Omar |
| **US-001-2** | Budget: UI | Vilena |
| **US-001-3** | Budget: E2E + docs | Vilena + Omar |
| US-002 final polish | All |
| E2E: photo → parse → preferences → budget → dish | All |

---

## Week 4 — 13-07 … 19-07

**Goal:** defense-ready.

- Fix bugs from W1-W3
- Deploy all new features
- Run the demo scenario 3 times
- Prepare presentation (Omar + Dasha)
- Buffer for force-majeure (if W3 went sideways)

---

## Notes

- **US-005 (allergens) — Removed**, not doing it.
- **US-007 (dislike), US-008 (history) — Removed** in the table, but US-015 effectively covers history.
- **GitHub issues for US-012-015** don't exist yet. Create them this week.
- **GitHub labels** diverge from the table (US-005 is Must in GitHub, Removed in table). Verify before defense.