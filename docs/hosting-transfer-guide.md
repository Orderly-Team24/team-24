# Hosting Transfer Guide — Render + Vercel

Practical, step-by-step instructions for moving Orderly's hosting from the team's accounts to the customer's own accounts. Written for the specific situation where the customer's Render account is a **free-tier personal workspace** (which cannot have members invited — see "Why not a Render Team" below), so services are recreated fresh rather than transferred in place.

This is separate from the GitHub repository transfer, which is already complete (`docs/customer-handover.md` §1).

## Why not a Render Team

Render only supports inviting other people (Members) into a **Team** workspace, not a personal one. Creating a Team is a paid feature. If the customer is fine paying for it, the cleaner alternative is:
- Move the existing services into a Team you own (Render supports this via each service's Settings → Transfer Service).
- Invite the customer as Owner/Admin.
- The current service URLs (`team-24.onrender.com`, `team-24-1.onrender.com`) are preserved, so none of the steps below (frontend config, data migration) are needed — just the Team invite.

Everything below assumes the customer is **not** paying for a Render Team, so services get recreated under their personal free account with new URLs.

## Prerequisites

- Customer has their own Render account (free tier is fine).
- Customer has their own OpenAI account + API key (do **not** hand over the team's key — billing for AI requests would stay on the team's card otherwise).
- Repository is already accessible to the customer (already done — see `docs/customer-handover.md`).

## Step 1 — Deploy the two backend services on the customer's Render account

Both services deploy the same way as documented in `src/backend/README.md` § "Deploy to Render":

### Recommender service (`src/backend`)
1. Render Dashboard → **New → Web Service** → select the repository.
2. **Root Directory:** leave empty (repository root) — the service imports `src/db/` via a relative path, and Docker needs both directories in the same build context.
3. **Dockerfile Path:** `src/backend/Dockerfile`
4. **Runtime:** Docker · **Instance type:** Free
5. Environment variables — see the table below.
6. Create Web Service. Render will build and deploy; the Dockerfile's `CMD` already runs `alembic upgrade heads` automatically before starting the server, so a fresh database gets its schema created with no manual migration step.

### OCR / upload service (`src/upload-menu-backend`)
Same steps, but:
- **Dockerfile Path:** `src/upload-menu-backend/Dockerfile`
- Only needs `ALLOWED_ORIGINS` (and optionally `TESSERACT_PATH`) — no database, no JWT.

### Environment variables

| Variable | Service | Value |
|---|---|---|
| `DATABASE_URL` | Recommender | New Postgres connection string (Step 2 below) |
| `JWT_SECRET_KEY` | Recommender | **Generate a new one** — `openssl rand -hex 32`. Never reuse the team's old value; anyone with the old value could otherwise forge session tokens even after transfer. |
| `AI_BACKEND` | Recommender | `openai` |
| `OPENAI_API_KEY` | Recommender | Customer's **own** OpenAI key, not the team's |
| `OPENAI_BASE_URL` | Recommender | Optional, has a default |
| `ALLOWED_ORIGINS` | Both | The Vercel frontend URL, once known (Step 4) |
| `TESSERACT_PATH` | OCR | Optional |

## Step 2 — Create a fresh PostgreSQL database

1. Render Dashboard → **New → PostgreSQL** (free tier).
2. Copy its **Internal Database URL** (for the recommender service's `DATABASE_URL` — internal is fine since both live in the same Render account) and its **External Database URL** (needed for the data migration in Step 3, since that runs from a machine outside Render's network).

## Step 3 — Migrate data from the old database

Run from a machine with `pg_dump`/`psql` installed (e.g. locally). You'll need the **External Database URL** for both the old (team-owned) and new (customer-owned) databases — get the old one from the team's Render dashboard.

```bash
# Dump the old database
pg_dump "OLD_EXTERNAL_DATABASE_URL" -F c -f orderly_backup.dump

# Restore into the new one (schema already exists from alembic upgrade heads
# on first boot — use --data-only to avoid conflicting with it, or restore
# to the fresh DB *before* the recommender service's first deploy so there's
# no schema yet to conflict with)
pg_restore --data-only --no-owner -d "NEW_EXTERNAL_DATABASE_URL" orderly_backup.dump
```

Do not paste either connection string into chat/Slack/etc. — treat them like passwords.

## Step 4 — Point the frontend at the new backend URLs

The frontend's backend URLs are a single config point (`src/new-frontend/src/config.js`), overridable via build-time environment variables — no source code changes needed:

| Vercel environment variable | Value |
|---|---|
| `REACT_APP_API_URL` | New recommender service URL, e.g. `https://<new-name>.onrender.com` |
| `REACT_APP_UPLOAD_URL` | New OCR service URL + `/upload-menu`, e.g. `https://<new-name>.onrender.com/upload-menu` |

Set these in the Vercel project (Settings → Environment Variables) — either on the team's Vercel project before transferring it, or on the customer's own Vercel project if they're hosting the frontend themselves too. Redeploy after setting them (env var changes require a new build to take effect, since Create React App bakes them in at build time).

## Step 5 — Smoke test

On the new URLs, end to end:
1. Register a new account, log in.
2. Set preferences, upload a menu (or skip to the sample menu).
3. Get a recommendation, click "I'll order it".
4. Open **History** — the order should appear and survive a page reload.
5. Click **Dislike** on it — reload again, it should still show "Disliked ✓" (requires the fix from issue #395, once merged).

## After transfer

- Update `docs/customer-handover.md` §1 (who owns what) and §9 (remaining actions) to reflect the new hosting.
- The team can decommission the old Render services once the customer confirms the new ones work.
