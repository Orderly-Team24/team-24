# Development Process – Orderly

This document describes the team's development workflow, branching strategy, configuration management, and Definition of Done enforcement. It reflects the actual process used from Sprint 1 onward and is maintained as a living document.

---

## Table of Contents

- [Git Workflow](#git-workflow)
- [Branch Naming](#branch-naming)
- [Pull Request Process](#pull-request-process)
- [Configuration Management](#configuration-management)
- [CI Pipeline](#ci-pipeline)
- [Sprint Process](#sprint-process)
- [Definition of Done](#definition-of-done)

---

## Git Workflow

The team uses a feature-branch workflow based on GitHub Flow. All work happens on short-lived feature branches that are merged into `main` via reviewed pull requests. The `main` branch is protected: direct pushes are not allowed and at least one approving review is required. Passing CI is expected but not currently enforced by branch protection (see [CI Pipeline](#ci-pipeline)) — reviewers should confirm the checks are green before approving.

```mermaid
gitGraph
   commit id: "initial commit"
   branch 62-us-011-upload-photo
   checkout 62-us-011-upload-photo
   commit id: "add upload page"
   commit id: "add OCR endpoint"
   checkout main
   merge 62-us-011-upload-photo id: "PR #101 merged"
   branch 57-us-001-budget-filter
   checkout 57-us-001-budget-filter
   commit id: "implement budget filter"
   checkout main
   merge 57-us-001-budget-filter id: "PR #120 merged"
   branch 223-setup-postgresql
   checkout 223-setup-postgresql
   commit id: "add models.py"
   commit id: "add alembic migrations"
   checkout main
   merge 223-setup-postgresql id: "PR #232 merged"
   commit id: "v0.3.0 – MVP v2" tag: "v0.3.0"
```

### How the team uses this workflow

1. A developer picks an issue from the Sprint Backlog.
2. They create a branch from `main` following the naming convention below.
3. They implement the work in small commits.
4. They open a pull request referencing the issue number (e.g. `Closes #223`).
5. At least one other team member reviews the PR and approves it.
6. The reviewer confirms CI is green before approving (branch protection requires the review, not the checks themselves — see [CI Pipeline](#ci-pipeline)).
7. The issue is closed automatically when the PR is merged.

---

## Branch Naming

All branches follow the convention:

```
<issue-number>-short-description
```

Examples:
- `223-setup-postgresql-database-and-sqlalchemy-models`
- `221-us-017-delete-account`
- `74-us-002-1-create-login-page`

This convention ensures every branch is traceable to a specific issue, makes the purpose of each branch immediately visible in the branch list, and avoids naming conflicts.

---

## Pull Request Process

Every PR must:

- Reference the related issue with `Closes #<number>` in the description
- Have at least one reviewer who is not the author
- Include a description of what was done and how to test it
- Update `CHANGELOG.md` for any user-visible change

CI checks are not currently required by branch protection (a PR can be merged even if they're red or still running) — reviewers are responsible for checking their status manually before approving.

PRs that change architecture, deployment, or quality requirements must also update the relevant documentation in `docs/`.

Reviewers are expected to check:
- Acceptance criteria from the issue are satisfied
- No credentials or secrets are committed
- Tests cover the changed logic
- CI is green
- No other open PR is implementing the same endpoint/feature — a route collision from two parallel PRs has already broken `main` once

---

## Configuration Management

### Secrets and credentials

No secrets, API keys, database URLs, or passwords are committed to the repository. The following environment variables are required for production and must be set in the Render dashboard:

| Service | Variable | Purpose |
|---|---|---|
| Recommender (team-24) | `DATABASE_URL` | PostgreSQL connection string |
| Recommender (team-24) | `JWT_SECRET_KEY` | Signing key for access/refresh tokens |
| Recommender (team-24) | `OPENAI_API_KEY` | OpenAI API authentication |
| Recommender (team-24) | `OPENAI_BASE_URL` | OpenAI API base URL |
| Recommender (team-24) | `AI_BACKEND` | Set to `openai` in production |
| Recommender (team-24) | `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins |
| OCR (team-24-1) | `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins |

For local development, create a `.env` file (git-ignored) or export variables in the shell. Never commit `.env` files.

### Database migrations

Schema changes require an Alembic migration:

```bash
# From src/db/ with DATABASE_URL set in the shell
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Migration files in `src/db/alembic/versions/` are committed to the repository and reviewed in PRs like any other code change.

### Dependency management

Backend dependencies are pinned in `requirements.txt` files:
- `src/backend/requirements.txt`
- `src/upload-menu-backend/requirements.txt`

Frontend dependencies are managed by `npm` and locked in `package-lock.json`.

---

## CI Pipeline

The CI pipeline runs on every push and pull request via GitHub Actions. It includes:

| Check | What it verifies |
|---|---|
| Unit tests (`pytest`, both backends) | Business logic correctness, min. 30% coverage |
| Security scan (`bandit`) | Unsafe code patterns (not a dependency/CVE scanner) |
| Link checking (`lychee`) | No broken links in documentation |

There is no linter (flake8 or otherwise) and no dependency vulnerability scanner (e.g. `pip-audit`, Dependabot) configured yet — if the team wants those, they need to be added to `.github/workflows/backend-ci.yml`.

None of these checks are required by branch protection — a PR can currently be merged with failing or unfinished CI. The CI configuration lives in `.github/workflows/`.

---

## Sprint Process

The team follows Scrum with one-week Sprints.

| Event | When | Artifact |
|---|---|---|
| Sprint Planning | Start of Sprint | Sprint milestone, Sprint Backlog |
| Daily Standup | Each working day | Async updates in team channel |
| Sprint Review | End of Sprint | Customer demo, UAT results |
| Sprint Retrospective | After Sprint Review | `reports/weekN/retrospective.md` |

Sprint work is tracked on the [GitHub Projects board](https://github.com/orgs/Orderly-Team24/projects/3). Issues are assigned to the Sprint milestone and move through columns: To Do → In Progress → In Review → Done.

---

## Definition of Done

A PBI is Done only when all conditions in [docs/definition-of-done.md](definition-of-done.md) are satisfied. Key gates:

- All acceptance criteria from the issue are met
- At least one peer review with approval
- CI is green on the PR (checked manually by the reviewer — not yet enforced by branch protection)
- `CHANGELOG.md` updated for user-visible changes
- Relevant documentation updated
