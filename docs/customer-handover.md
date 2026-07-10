# Customer Handover — Orderly

This document describes the **actual current** handover state of Orderly, as of Sprint 4 (Week 6). It is updated whenever access, ownership, limitations, or confirmed status change — most recently after the Sprint 4 review/transition-readiness discussion (see `reports/week6/README.md` for that meeting's outcome).

## What has been transferred / delegated / retained

| Item | Status | Notes |
|---|---|---|
| GitHub repository (`Orderly-Team24/team-24`) | Public, readable by anyone | Repo ownership itself (org admin rights) is **retained by the team** — no separate transfer has happened yet. |
| Frontend deployment (Vercel, `team-24-navy.vercel.app`) | Auto-deploys from `main` | Hosting account is **retained by the team**. Customer has not been given Vercel dashboard access. |
| Recommender API (Render, `team-24`) | Live | Hosting account is **retained by the team**. Free-tier service — wakes up in 5–15s after inactivity. |
| OCR/upload API (Render, `team-24-1`) | Live | Same as above. |
| Database (PostgreSQL, Render-managed) | Live | Retained by the team; no customer-side backup/export has been provided yet. |
| OpenAI API key | Configured in Render env vars only | Belongs to the team; **not** shared with the customer. |

**Open item:** whether the customer needs/wants their own deployment (their own Render/Vercel/OpenAI accounts) instead of continuing to depend on the team's, has not been decided yet — this is a Week 6 transition-readiness discussion point (see `docs/customer-handover.md` history below and Assignment requirements Part 5).

## Configuration the customer must know about

Environment variables required to run/redeploy the services (see [docs/development-process.md § Configuration Management](development-process.md#configuration-management) for the full table):

| Variable | Where | Purpose |
|---|---|---|
| `DATABASE_URL` | Recommender service | PostgreSQL connection string |
| `OPENAI_API_KEY` | Recommender service | Required if `AI_BACKEND=openai` (production setting) |
| `OPENAI_BASE_URL` | Recommender service | OpenAI API base URL |
| `AI_BACKEND` | Recommender service | `openai` in production; `stub` for offline/local dev with no API cost |
| `NEGATION_LLM_EXTRACTION` | Recommender service | Optional; set to `false` to disable the LLM-backed exclusion-phrase detector if its extra API cost/latency isn't wanted |
| `ALLOWED_ORIGINS` | Both backend services | Comma-separated CORS allow-list |

**Known security gap the customer should be aware of before relying on this beyond course use:** the JWT signing secret in `src/backend/jwt_handler.py` is currently a hardcoded string in the source code, not sourced from an environment variable. This must be externalized (moved to an env var, rotated) before this codebase is used for anything beyond the course project — it is called out here so it isn't missed at handover.

## Setup / deploy / recovery

- Local development setup: [README.md § Getting started](../README.md#getting-started-local-development).
- Contribution/PR workflow: [CONTRIBUTING.md](../CONTRIBUTING.md).
- Both Render services and the Vercel frontend auto-deploy on every push to `main` — there is no manual deploy step under normal operation.
- Recovery: if a Render service needs to be recreated, the required env vars are listed above; the Dockerfiles for both backend services live at `src/backend/Dockerfile` and `src/upload-menu-backend/Dockerfile`.
- **No customer-facing backup/restore procedure exists yet** for the PostgreSQL database. Order history (`/history/orders*`) is stored **in-process memory, not the database** — it is lost on every service restart or redeploy regardless of backup strategy. This is a known limitation, not a bug to restore from.

## Main documentation entry points

| For... | Start at |
|---|---|
| Understanding what the product does and how to run it | [README.md](../README.md) |
| Contributing a change | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| An AI coding agent making a change | [AGENTS.md](../AGENTS.md) |
| Architecture / design decisions | [docs/architecture/](architecture/README.md) |
| What's tested and how | [docs/testing.md](testing.md), [docs/quality-requirement-tests.md](quality-requirement-tests.md) |
| Verifying a specific user-facing behavior | [docs/user-acceptance-tests.md](user-acceptance-tests.md) |
| What's planned / already done, sprint by sprint | [docs/roadmap.md](roadmap.md) |
| Full change history | [CHANGELOG.md](../CHANGELOG.md) |

Hosted (browsable) version of all of the above: https://orderly-team24.github.io/team-24/

## Known limitations (current, as of Sprint 4)

- Order history and dislikes are stored in-memory on the recommender service — not persisted to the database yet, lost on every restart/redeploy.
- The AI's understanding of free-text requests (mood/craving field) is heuristic (regex) plus a best-effort LLM-backed supplement for phrasing the regex misses — it is **not** a hard guarantee for arbitrary natural language, unlike allergy/exclusion handling, which is a hard, code-enforced guarantee.
- OCR menu parsing is tuned for a specific common layout (dish name on its own line, description + price following). Two-column menus, handwritten inserts, and non-Latin currency symbols are not yet reliably handled.
- No automated test suite exists for the frontend (`src/new-frontend/`); frontend changes are verified manually.
- `cuisine` as a preference was removed in Sprint 4 (it was accepted by the UI/API but never actually used) — if the customer expects cuisine-based filtering, this is a gap to raise explicitly.

## Is the current documentation sufficient? What support remains necessary?

**This section reflects the team's self-assessment going into the Week 6 meeting — it is not yet a confirmed customer answer.**

- The team believes README.md + CONTRIBUTING.md + this document are sufficient for a technically literate customer to run and understand the current state of the product independently.
- Deployment (Render/Vercel account ownership) has **not** been transferred — if the customer wants to operate the product themselves rather than depend on the team's hosting, that is still outstanding work, not yet started.
- <!-- TODO after the Week 6 transition-readiness meeting: fill in the customer's own assessment of doc sufficiency (clear / unclear / missing, per docs/development-process.md Part 3 review), and any support they say they still need. -->

## Handover level and confirmation status

<!-- TODO: fill in after the Week 6 (and, if applicable, Week 7) transition-readiness meeting with the customer. Per Assignment 6 Part 8, these are two independent axes — do not infer one from the other. -->

- **Handover level reached:** <!-- Ready for independent use | Independently used by customer | Deployed/operated on customer side — pick one, with justification -->
- **Customer confirmation status:** <!-- Accepted | Accepted with follow-up items | Not yet accepted -->
- **If a stronger level/confirmation wasn't reached:** <!-- explain why not, whose blocker (team/customer/external), evidence of readiness already obtained, remaining actions -->
