# Week 6 Report – Orderly

## Project information
- **Name:** Orderly – Food Recommendation App
- **Short description:** A web app that helps users choose dishes from restaurant menus based on their preferences and budget.
- **License:** [MIT](../../LICENSE)

## Product Backlog
- [Product Backlog board/view](https://github.com/orgs/Orderly-Team24/projects/2)
- [Current Sprint Backlog board/view](https://github.com/orgs/Orderly-Team24/projects/3)
- [Sprint 4 milestone](https://github.com/Orderly-Team24/team-24/milestone/4)

### Sprint Details
- **Sprint Goal:** Implement order history management (view history, dislike a dish), polish AI recommendation quality, and fix bugs found during customer UAT.
- **Sprint Dates:** July 06 2026 – July 12 2026
- **Scope Summary:** Order history + dislike feature (US-015), AI recommendation safety hardening (allergen/exclusion guarantees, meal-type recognition, beverage exclusion), authentication and session bug fixes.
- **Total Sprint Size:** 8 Story Points

## Delivery Summary
**Delivered Product Changes:**
Order history + dislikes (US-015), AI safety hardening, meal-type recognition, no beverage as dish, no-repeat recommendations, OCR improvements, auth and session bug fixes, removed unused cuisine preference, added maintained docs.
- **Access/Run instructions:** [README.md](../../README.md)
- **Deployed Product (runnable artifact):** [product](https://team-24-navy.vercel.app/)

## Customer Feedback & Response
| Feedback Point | Resulting PBI / Issue |
| :--- | :--- |
| <!-- e.g. "second menu photo upload didn't work" --> | [#283](https://github.com/Orderly-Team24/team-24/issues/283) |

### Feedback Not Addressed

## Documentation
- **Contributing:** [CONTRIBUTING.md](../../CONTRIBUTING.md)
- **AGENTS.md:** [AGENTS.md](../../AGENTS.md)
- **Customer handover:** [docs/customer-handover.md](../../docs/customer-handover.md)
- **Roadmap:** [docs/roadmap.md](../../docs/roadmap.md)
- **Definition of Done:** [docs/definition-of-done.md](../../docs/definition-of-done.md)
- **Testing Strategy:** [docs/testing.md](../../docs/testing.md)
- **Quality Requirements:** [docs/quality-requirements.md](../../docs/quality-requirements.md)
- **Quality Requirement Tests:** [docs/quality-requirement-tests.md](../../docs/quality-requirement-tests.md)
- **User Acceptance Tests (UAT):** [docs/user-acceptance-tests.md](../../docs/user-acceptance-tests.md)
- **Development process:** [docs/development-process.md](../../docs/development-process.md)
- **README of Architecture** [docs/architecture/README.md](../../docs/architecture/README.md)
- **Hosted Documentation Site:** [Orderly Docs](https://orderly-team24.github.io/team-24/)

### Doc Review Results


### Transition-Readiness Summary


### Test Links
- **Unit Tests (backend):** `test_ai_service.py`, `test_auth.py` (new), `test_no_repeat_session.py` (new), `test_preferences.py`, `test_dislike_filter.py`, `test_history_router.py`, `test_budget_filter.py`, `test_user_route.py`, `test_users.py`
- **Unit Tests (OCR service):** `test_parser.py`, `test_ocr_layout.py` (new), `test_upload.py`
- **Automated Quality Requirement Tests:** `test_response_time.py`

## Architecture Views
- **Static View:** [Static Architecture View](../../docs/architecture/static-view/component-diagram.svg)
- **Dynamic View:** [Dynamic Architecture View](../../docs/architecture/dynamic-view/sequence-diagram.svg)
- **Deployment View:** [Deployment Architecture View](../../docs/architecture/deployment-view/deployment-diagram.svg)

### Architecture Decision Records (ADR)
- **ADR-001:** [Split backend services](../../docs/architecture/adr/ADR-001-split-backend-services.md)
- **ADR-002:** [Postgresql sqlalchemy](../../docs/architecture/adr/ADR-002-postgresql-sqlalchemy.md)
- **ADR-003:** [Openai integration](../../docs/architecture/adr/ADR-003-openai-integration.md)

## CI / CD & Branch Protection
- **CI Pipeline Definition:** [backend-ci.yml](../../.github/workflows/backend-ci.yml), [blank.yml (link check)](../../.github/workflows/blank.yml)
- **Branch Protection Rules Evidence:** [Rules](https://github.com/Orderly-Team24/team-24/settings/branches)

## Release & Changelog
- **CHANGELOG.md:** [CHANGELOG.md](../../CHANGELOG.md) 
- **SemVer Release:** [SemVer](https://github.com/Orderly-Team24/team-24/releases/tag/v0.3.0)

## Presentation & Media
- 

## UAT Results Summary


## Sprint Reports & Retrospectives
- **Sprint review transcript / notes:** [sprint-review-transcript.md](sprint-review-transcript.md)
- **Customer Review Summary:** [sprint-review-summary.md](sprint-review-summary.md)
- **Sprint Reflection:** [reflection.md](reflection.md)
- **Retrospective:** [retrospective.md](retrospective.md)
- **LLM Report:** [llm-report.md](llm-report.md)

## Current Status & Next Steps
- **Current Product Status:** Order history and dislikes are implemented end-to-end; AI recommendation safety (allergens/exclusions) and quality (meal type, no beverage-as-dish, no-repeat) have been substantially hardened this sprint; a cluster of authentication/session bugs found during UAT has been fixed.
- **Next Steps (expected Week 7 scope, pending Week 6 customer feedback):** Address any follow-up items from the Week 6 transition-readiness meeting; move order history from in-memory storage to PostgreSQL; continue OCR robustness work; prepare final MVP v3 transition/handover.

## Contribution Traceability

| Team Member | Issues | PRs/MRs | Review Activity | Testing | Quality/Automation | Documentation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Daria Gorshkova (dayeon761) | - | - | - | - | - | - |
| Viktoriia Iakovleva (rxxtzz) | - | - | - | - | - | - | 
| Polina Kharlova (Kharlova) | - | - | - | - | - | - |
| Vilena Zulkarnaeva (vianevi) | - | - | - | - | - | - |
| Omar Nader (Ramy678) | - | - | - | - | - | - |
| Adelina Khafizova (adelinamikki) | - | - | - | - | - | - |

## Visual Evidence
### Sprint Milestone
![Sprint Milestone](images/sprint-milestone.png)
### SemVer Release
![SemVer Release](images/SemVer-release.png)
### Example Reviewed Issue-linked PR/MR
![PR Review Example](images/example-reviewed-issue-linked-PR.png)
