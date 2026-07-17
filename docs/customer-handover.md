# Customer Handover

_Last updated: 2026-07-17 (Week 7, Sprint 5)_

## 1. Current Product Status & Handover Scope

<!-- Artifact Req #4: current product status and handover scope -->
<!-- Assignment 6 Part 4: which repository, service, deployment, account, access,
     or ownership arrangements were transferred, delegated, or intentionally
     retained by the team -->

Short paragraph: what the product does today (MVP v3), what was delivered in
Assignment 6 (Sprint 4 + Sprint 5), and the overall scope of what is being
handed over.

- **Repository:** transferred / access granted to `<customer-github-username>` as
  [Owner / Maintainer] — *or* retained by the team with customer given read access, explain why.
- **Deployment/hosting:** transferred to customer's account / retained on team's
  account with access granted / retained by team, explain why and until when.
- **Domain / hosting service account:** who owns it now.
- **CI/CD, monitoring, or other service accounts:** state ownership explicitly.

> Be concrete. "Repo ownership retained by team; customer added as Maintainer;
> deployment stays on team's [hosting provider] account until [date/condition]."

## 2. How the Customer Accesses and Uses the Product

<!-- Artifact Req #4: how the customer accesses and uses the product -->

- Production URL: `https://...`
- Login / access method (no credentials in this public file — see §4)
- Link to current product access artifact
- Brief walkthrough of the main user flow (2–4 sentences, not a full manual —
  link to more detailed usage docs if they exist)

## 3. Installation or Deployment Instructions

<!-- Artifact Req #4: installation or deployment instructions where relevant -->

If the customer needs to deploy or run it themselves:

- Prerequisites (runtime, services, accounts needed)
- Step-by-step deploy/run instructions, or a link to `README.md` / a deploy doc
  if the steps are long — but summarize the key steps here, don't just link.

## 4. Configuration & Secrets-Handling Expectations

<!-- Artifact Req #4: required configuration and secrets-handling expectations
     without exposing secrets -->
<!-- Assignment 6 Part 4: which environment variables, configuration values,
     external services, or secrets-handling steps the customer must know about
     without exposing secrets -->

- List **names** of required environment variables / config values (not values):
  `DATABASE_URL`, `API_KEY_X`, etc.
- External services the product depends on (e.g. hosting provider, email
  service, third-party API) and what account/plan they need.
- Where actual secrets live and how the customer obtains them (e.g. "shared
  privately via [instructor/customer channel], never committed to the repo").

## 5. Operational Notes for Normal Use

<!-- Artifact Req #4: operational notes needed for normal use where relevant -->

- Anything the customer needs to do periodically (backups, renewals, updates)
- Any manual steps not yet automated
- Monitoring / logs, if applicable and accessible to the customer

## 6. Troubleshooting & Support

<!-- Artifact Req #4: troubleshooting or support guidance -->

- Common issues and fixes (short table or list)
- Who to contact and how, and until when the team provides support
- Link to any issue tracker the customer can use to report problems

## 7. Known Limitations, Unfinished Areas, and Risks

<!-- Artifact Req #4: known limitations, unfinished areas, or important risks -->

- Explicitly list what is NOT done / NOT robust yet (e.g. mobile layout edge
  cases, filtering edge cases if not fully resolved by #337/#331/#328 — adjust
  once those are actually closed)
- Any risk that could affect future usefulness (e.g. free-tier hosting limits,
  unmaintained dependency, no CI after course ends)

## 8. Current Handover Status

<!-- Artifact Req #5: must be exactly one of the three levels -->

**Handover level reached:** `Ready for independent use` |
`Independently used by customer` | `Deployed or operated on customer side`

<!-- Assignment 6 Part 8: also state customer-confirmation status, separate
     from the level above -->

**Customer-confirmation status:** `Accepted` | `Accepted with follow-up items` |
`Not yet accepted`

Short paragraph justifying the chosen level and status — what happened in the
Week 7 meeting that supports this classification.

## 9. Remaining Actions

<!-- Artifact Req #4 + #6: remaining actions and whether they block full
     transition; if stronger levels not reached, explain blocker -->

| Action | Owner (team / customer / external) | Blocks full transition? |
|---|---|---|
| ... | ... | Yes/No |

If the confirmation status is not `Accepted`, explicitly explain:
- what follow-up items / requested changes remain
- whose side the blocker is on
- what evidence of readiness/usefulness was still obtained
- what would still be needed for full acceptance

## 10. Related Documentation

<!-- Artifact Req #4: links to related customer-relevant documentation -->

- [README.md](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [AGENTS.md](../AGENTS.md)
- [Hosted documentation site](<link>)
- [docs/user-acceptance-tests.md](./user-acceptance-tests.md)
- [docs/roadmap.md](./roadmap.md)
