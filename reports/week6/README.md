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
- **Scope Summary:** Order history + dislike feature (US-015), AI recommendation safety hardening (allergen/exclusion guarantees, meal-type recognition, beverage exclusion), authentication/session bug fixes surfaced by UAT, Assignment 6 maintained documentation.
- **Total Sprint Size:** 8 Story Points tracked on US-015 subtasks (#285–#288); the AI-quality and auth/session fixes below were shipped as bug fixes discovered during Sprint 4 testing/UAT rather than pre-estimated PBIs — see [docs/roadmap.md](../../docs/roadmap.md) Sprint 4 section for the full list with issue links.

## Delivery Summary

**Delivered Product Changes:**
- Order history and dislikes (US-015): users can view their order history and mark a dish as disliked; disliked dishes are excluded from future recommendations.
- AI recommendation safety: excluded ingredients (allergies, dislikes, and plain-language exclusions typed into the mood field) are now a hard, code-enforced guarantee across every AI backend — including the case where every candidate dish matches the exclusion, and including phrasings the original regex-based parser missed (via an LLM-backed supplement, itself guarded against hallucinating an exclusion on a purely positive message).
- AI recommendation quality: recognizes meal type (breakfast/lunch/dinner) from the mood field and never recommends a beverage on its own as "the dish".
- "Another option" no longer relies on chance to avoid repeats — a dish shown once in a session is never shown again until every candidate has been shown.
- OCR: column-aware layout reconstruction, currency-symbol handling, and menu section detection.
- Fixed a cluster of authentication/session bugs surfaced during UAT: expired-token lockout on `/login`/`/register`, order history appearing empty (or pooling across users) due to a user-identity mismatch between login/registration and the history endpoints, and a missing `/history` route causing a blank page.
- Removed the `cuisine` preference, which was accepted end-to-end but never actually used.
- Added Assignment 6 maintained documentation: `CONTRIBUTING.md`, `AGENTS.md`, `docs/customer-handover.md`.

Full details: [CHANGELOG.md](../../CHANGELOG.md) `[Unreleased]` section.

- **Access/Run instructions:** [README.md](../../README.md)
- **Deployed Product (runnable artifact):** [product](https://team-24-navy.vercel.app/)

## Customer Feedback & Response

| Feedback Point | Resulting PBI / Issue |
| :--- | :--- |
| Documentation lacks a clear, non-technical user guide for independent use | Addressed same day: README.md "User guide" section + plain-language rewrite of `docs/customer-handover.md` |
| Meal-type filtering (breakfast/lunch/dinner/drinks) feels unstable beyond the demoed scenario | Sprint 5 action item (due 17.07.26) |
| Erroneous/confusing "Recommendations" nav button | Sprint 5 action item, assigned to Viktoriia Iakovleva & Vilena Zulkarnaeva (due 17.07.26) |
| Add a free-text dietary-preference field (vegan, halal, etc.) | Sprint 5 action item, assigned to Viktoriia Iakovleva & Vilena Zulkarnaeva (due 17.07.26) |

### Feedback Not Addressed
None raised as unaddressed — all feedback points above have either been resolved same-day or converted into a scheduled Sprint 5 action item (see [sprint-review-summary.md](sprint-review-summary.md) Action Points).

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
Reviewed live with the customer on 10.07.2026: README.md and CONTRIBUTING.md. **Clear:** feature set, setup/run instructions. **Missing:** a plain, non-technical walkthrough of how to actually use the product — addressed same day (README.md § User guide). `docs/customer-handover.md` was reviewed and **accepted as an accurate reflection of the current transfer state**, "noting that while dependencies aren't ideal, the handover is acceptable for now."

### Transition-Readiness Summary
**Ready:** order history/dislikes, AI safety guarantees (allergens/exclusions), deployment access instructions, customer-handover.md (accepted). **Needs changes before Week 7 close:** meal-type filtering stability, an erroneous nav button, a dietary-preference field (all scheduled, due 17.07.26). **Not yet decided:** whether the customer wants their own hosting (Vercel/Render/OpenAI accounts) or continues depending on the team's — not yet raised as a decision point. Customer is not yet using/operating the product independently of the team's hosting; handover level is "Ready for independent use" (see `docs/customer-handover.md`).

### Test Links
- **Unit Tests (backend):** `test_ai_service.py`, `test_auth.py` (new), `test_no_repeat_session.py` (new), `test_preferences.py`, `test_dislike_filter.py`, `test_history_router.py`, `test_budget_filter.py`, `test_user_route.py`, `test_users.py`
- **Unit Tests (OCR service):** `test_parser.py`, `test_ocr_layout.py` (new), `test_upload.py`
- **Automated Quality Requirement Tests:** `test_response_time.py`

## Architecture Views
- **Static View:** [Static Architecture View](../../docs/architecture/static-view/component-diagram.svg)
- **Dynamic View:** [Dynamic Architecture View](../../docs/architecture/dynamic-view/sequence-diagram.svg)
- **Deployment View:** [Deployment Architecture View](../../docs/architecture/deployment-view/deployment-diagram.svg)

No architecture changes this sprint — see [reports/week5/README.md](../week5/README.md) for the last architecture summary/alignment discussion, still current.

### Architecture Decision Records (ADR)
- **ADR-001:** [Split backend services](../../docs/architecture/adr/ADR-001-split-backend-services.md)
- **ADR-002:** [Postgresql sqlalchemy](../../docs/architecture/adr/ADR-002-postgresql-sqlalchemy.md)
- **ADR-003:** [Openai integration](../../docs/architecture/adr/ADR-003-openai-integration.md)

## CI / CD & Branch Protection
- **CI Pipeline Definition:** [backend-ci.yml](../../.github/workflows/backend-ci.yml), [blank.yml (link check)](../../.github/workflows/blank.yml)
- **Branch Protection Rules Evidence:** [Rules](https://github.com/Orderly-Team24/team-24/settings/branches)

## Release & Changelog
- **CHANGELOG.md:** [CHANGELOG.md](../../CHANGELOG.md) — see `[Unreleased]` for this sprint's full change list.
- <!-- TODO: tag and link the Week 6 trial/handover-candidate SemVer release once cut. -->

## Presentation & Media
- <!-- TODO: link the rehearsed presentation video (private, Moodle PDF only) and, if applicable, the customer review recording/transcript. -->

## UAT Results Summary

<!-- TODO after Week 6 meeting: execute and record results for the scenarios below (new this sprint) plus any previously-passing scenario worth re-checking. -->

| ID | Scenario | Related US | Status |
|----|----------|-------------|--------|
| UAT-08 | View Order History and Dislike a Dish | US-015 | <!-- Pass/Fail --> |
| UAT-09 | AI Never Recommends an Excluded or Allergen Food | US-005 | <!-- Pass/Fail --> |
| UAT-10 | AI Recognizes Meal Type and Never Recommends a Drink as the Dish | US-018 | <!-- Pass/Fail --> |

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

<!-- PRs merged during Sprint 4 (2026-07-06 onward), grouped by author. See individual PRs for issue links (Closes #N). -->

| Team Member | PRs (Sprint 4) | Focus Area |
| :--- | :--- | :--- |
| Daria Gorshkova (dayeon761) | [#299](https://github.com/Orderly-Team24/team-24/pull/299), [#300](https://github.com/Orderly-Team24/team-24/pull/300), [#302](https://github.com/Orderly-Team24/team-24/pull/302), [#305](https://github.com/Orderly-Team24/team-24/pull/305), [#306](https://github.com/Orderly-Team24/team-24/pull/306), [#307](https://github.com/Orderly-Team24/team-24/pull/307), [#308](https://github.com/Orderly-Team24/team-24/pull/308), [#312](https://github.com/Orderly-Team24/team-24/pull/312), [#313](https://github.com/Orderly-Team24/team-24/pull/313), [#314](https://github.com/Orderly-Team24/team-24/pull/314), [#316](https://github.com/Orderly-Team24/team-24/pull/316), [#317](https://github.com/Orderly-Team24/team-24/pull/317), [#297](https://github.com/Orderly-Team24/team-24/pull/297), [#294](https://github.com/Orderly-Team24/team-24/pull/294), [#290](https://github.com/Orderly-Team24/team-24/pull/290), [#284](https://github.com/Orderly-Team24/team-24/pull/284) | AI recommendation safety/quality (allergens, negation parsing, meal type, beverage exclusion, no-repeat), auth/session bug fixes, US-015-1, Assignment 6 docs |
| Polina Kharlova (Kharlova) | [#309](https://github.com/Orderly-Team24/team-24/pull/309), [#310](https://github.com/Orderly-Team24/team-24/pull/310) | Expired-token lockout fix, order-history user-identity fix |
| Vilena Zulkarnaeva (vianevi) | [#293](https://github.com/Orderly-Team24/team-24/pull/293), [#301](https://github.com/Orderly-Team24/team-24/pull/301), [#276](https://github.com/Orderly-Team24/team-24/pull/276) | Frontend History page + Dislike button (US-015-3) |
| Omar Nader (Ramy678) | [#304](https://github.com/Orderly-Team24/team-24/pull/304) | Filter recommendations by dislikes (US-015-2) |
| Adelina Khafizova (adelinamikki) | [#291](https://github.com/Orderly-Team24/team-24/pull/291), [#315](https://github.com/Orderly-Team24/team-24/pull/315) | Menu parser name/description fix, OCR layout improvements |
| Viktoriia Iakovleva (rxxtzz) | [#292](https://github.com/Orderly-Team24/team-24/pull/292) | Registration loading-state fix |

<!-- TODO: fill in Review Activity / Testing / Quality-Automation / Documentation columns per person once finalized — the PR list above is derived directly from `gh pr list --state merged` and is accurate; reviewer assignments were not pulled for this draft. -->

## Visual Evidence
<!-- TODO: add screenshots to reports/week6/images/ and embed them here (Sprint 4 milestone view, Sprint board, latest CI run, example reviewed issue-linked PR, deployed History page, customer trial evidence) — matching the set used in reports/week5/README.md. -->
