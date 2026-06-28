# Week 3 Report – Orderly

## Project information
- **Name:** Orderly – Food Recommendation App
- **Short description:** A web app that helps users choose dishes from restaurant menus based on their preferences and budget.
- **License:** [MIT](../../LICENSE) 

# User Stories & PBI Summary

**Current scope:** 33 PBIs
29 User Stories: 6 done in MVP v1, 23 planned for next sprints
4 Tasks: all done in MVP v1

**Changes since Assignment 2:**
- Decomposed US-002 (Ability to sign in), US-003 (Guarantee safety of user information), US-010 (Admin functions for analysis) and US-011 (Upload photo of a menu) into smaller sub-tasks.
- Added story point estimates to all tasks (range 2–8 SP).
- Completed US-011 (Upload photo of a menu). All sub-tasks implemented and closed.


## Customer Feedback Addressed in MVP v1
- US-011 added to scope per customer request: photo upload + AI recommendations implemented
- US-004 and US-005 moved to next sprint

## Links
- Historical: [`reports/week2/user_stories.md`](../week2/user_stories.md)
- Current: [`docs/user-stories.md`](../../docs/user-stories.md)
- Closed issues: [#62](https://github.com/Orderly-Team24/team-24/issues/62), [#71](https://github.com/Orderly-Team24/team-24/issues/71), [#72](https://github.com/Orderly-Team24/team-24/issues/72), [#73](https://github.com/Orderly-Team24/team-24/issues/73), [#75](https://github.com/Orderly-Team24/team-24/issues/75), [#92](https://github.com/Orderly-Team24/team-24/issues/92), [#93](https://github.com/Orderly-Team24/team-24/issues/93), [#94](https://github.com/Orderly-Team24/team-24/issues/94), [#95](https://github.com/Orderly-Team24/team-24/issues/95), [#122](https://github.com/Orderly-Team24/team-24/issues/122)

## Product Backlog
- [Product Backlog board/view](https://github.com/orgs/Orderly-Team24/projects/2)
- [Current Sprint Backlog board/view](https://github.com/orgs/Orderly-Team24/projects/3)
- [Current Sprint milestone](https://github.com/Orderly-Team24/team-24/milestone/1)

### Story Points
- Total Product Backlog size: 85 SP
- Total current Sprint size: 29 SP

### Included in MVP v1
| ID | Title | Type | Status | SP |
|----|-------|------|--------|----|
| US-011 | Upload photo of a menu | User Story | Closed | - |
| US-011-1 | Choose photo from gallery | Task | Closed | 3 |
| US-011-2 | Text parsing | Task | Closed | 8 |
| US-011-3 | Dish choice | Task | Closed | 8 |
| US-011-4 | Displaying menu recommendations | Task | Closed | 5 |
| US-011-5 | Deploy publicly | Task | Closed | 5 |

### Description of the selected MVP v1 scope.
MVP v1 focuses on the core functionality, allowing users to upload a menu photo and receive AI-powered dish recommendations. This was identified as the most critical missing feature.

### MVP v1 view
- [MVP v1 filtered view](https://github.com/Orderly-Team24/team-24/issues?q=is%3Aissue%20state%3Aclosed%20milestone%3A%22Sprint%201%22)
- [Sprint 1 Milestone](https://github.com/Orderly-Team24/team-24/milestone/1)

### PBI types used
User Story — functional requirements from user perspective.
Task — technical implementation sub-items decomposed from User Stories.
Course Task — tracked work for course reporting/grading.

### Work Status
To Do -	In Product Backlog, not ready to start.
Ready -	Selected for Sprint, assigned, estimated, has description + AC.
In Progress -	Work started.
Review- Implementation ready for review, PR open.
Done - AC satisfied, DoD satisfied, PR/MR merged into protected default branch.

### Sprint milestone
Each Sprint = one GitHub Milestone.
Milestone groups all Sprint-selected PBIs.
Milestone shows:
- Progress, percentage of closed issues
- Due date, sprint end date
- Remaining work, open issues in the sprint

### MVP version tracking
Milestones = Sprint 1 -> MVP v1, Sprint 2 -> MVP v2, etc.
Labels = mvp-v1, mvp-v2, mvp-v3 on PBIs.

### Task decomposition
Split large tasks by technical sub-tasks (frontend, backend).
Each sub-task: 2–8 SP, independent, testable.
Naming: parent ID + sub-number (US-011-1, US-011-2, ...).

### Current (Sprint 1 — MVP v1):
Completed. Delivered US-011 (photo upload + AI recommendations).

### Next (Sprint 2 — MVP v2):
- US-002 (Login), US-004 (Preferences), US-005 (Allergens)
- [docs/roadmap.md](../../docs/roadmap.md)

### Contribution traceability
| Team Member | Issues | PRs | Reviews |
|-------------|--------|-----|---------|
| Daria Gorshkova (dayeon761) | [#122](https://github.com/Orderly-Team24/team-24/issues/122), [#93](https://github.com/Orderly-Team24/team-24/issues/93) | #135, #128, #127, #126, #125, #124, #118, #117, #112, #111, #110, #105, #102, #91, #88, #87, #86, #85, #56, #129, #62 | #130, #114, #107|
| Viktoriia Iakovleva (rxxtzz) | [#92](https://github.com/Orderly-Team24/team-24/issues/92) | #132, #120, #108, #90, #89 | #124, #123 |
| Polina Kharlova (Kharlova) | [#95](https://github.com/Orderly-Team24/team-24/issues/95) | #119 | #128, #118|
| Vilena Zulkarnaeva (vianevi) | [#94](https://github.com/Orderly-Team24/team-24/issues/94) | #123, #113, #107 | #121, #120, #108 |
| Omar Nader (Ramy678) | [#73](https://github.com/Orderly-Team24/team-24/issues/73) | #136, #131, #106, #104, #103, #101, #100, #97, #96, #99, #98 | #109,  #105|
| Adelina Khafizova (adelinamikki) | [#72](https://github.com/Orderly-Team24/team-24/issues/72) | #134, #133, #130, #121, #116, #115, #114, #109 | #119, #110, #106|

### Links
- **SemVer release (MVP v1):** [v0.1.0](https://github.com/Orderly-Team24/team-24/releases/tag/v0.1.0)
- **CHANGELOG.md:** [CHANGELOG.md](../../CHANGELOG.md)
- **Process_Requirements.md:** [Process Requirements](Process_Requirements.md)
- **Roadmap:** [docs/roadmap.md](../../docs/roadmap.md)
- **Definition of Done:** [docs/definition-of-done.md](../../docs/definition-of-done.md)
- **MVP v1 deployment (runnable artifact):** [v0.1.0](https://frontend-pearl-sigma-1diis9tsn9.vercel.app/)
- **Access/Run instructions:** [README.md](../../README.md)
- **Public sanitized video demonstration:** [Link to video](https://drive.google.com/file/d/1g1bFizNBVim8eWnxBqWMCoE8kA2pbjC1/view?usp=drive_link)
- **Customer review transcript (sanitized, English):** [Customer Meeting Transcript](customer-meeting-transcript.md)
- **Customer review summary:** [Customer Review Summary](customer-review-summary.md)
- **Week 3 reflection:** [Week 3 Reflection](reflection.md)
- **Retrospective:** [Week 3 Retrospective](retrospective.md)
- **LLM report:** [LLM Report](llm-report.md)

### Issue Templates
- [Pull Request Template](../../.github/pull_request_template.md)
- [User Story Template](../../.github/ISSUE_TEMPLATE/user-story.md)
- [Bug Report Template](../../.github/ISSUE_TEMPLATE/bug-report.md)
- [Course Task Template](../../.github/ISSUE_TEMPLATE/course-task.md)
- [Other PBI Template](../../.github/ISSUE_TEMPLATE/other-PBI.md)

### Reviewed PRs (Week 3 — MVP v1)
- [#136](https://github.com/Orderly-Team24/team-24/pull/136) — reflection (Ramy678)
- [#135](https://github.com/Orderly-Team24/team-24/pull/135) — connect backends deploy (dayeon761)
- [#134](https://github.com/Orderly-Team24/team-24/pull/134) — Tesseract env (adelinamikki)
- [#133](https://github.com/Orderly-Team24/team-24/pull/133) — OCR test (adelinamikki)
- [#132](https://github.com/Orderly-Team24/team-24/pull/132) — llm-report (rxxtzz)
- [#128](https://github.com/Orderly-Team24/team-24/pull/128) — changelog (dayeon761)
- [#123](https://github.com/Orderly-Team24/team-24/pull/123) — roadmap (vianevi)
- [#121](https://github.com/Orderly-Team24/team-24/pull/121) — change path (adelinamikki)
- [#120](https://github.com/Orderly-Team24/team-24/pull/120) — frontend changes (rxxtzz)
- [#119](https://github.com/Orderly-Team24/team-24/pull/119) — display recommendations backend (Kharlova)
- [#118](https://github.com/Orderly-Team24/team-24/pull/118) — test upload menu backend (dayeon761)
- [#117](https://github.com/Orderly-Team24/team-24/pull/117) — customer review summary (dayeon761)
- [#116](https://github.com/Orderly-Team24/team-24/pull/116) — week 3 retro (adelinamikki)
- [#115](https://github.com/Orderly-Team24/team-24/pull/115) — add new folder (adelinamikki)
- [#114](https://github.com/Orderly-Team24/team-24/pull/114) — Definition of Done (adelinamikki)
- [#113](https://github.com/Orderly-Team24/team-24/pull/113) — customer meeting transcript (vianevi)
- [#112](https://github.com/Orderly-Team24/team-24/pull/112) — refactor src/ (dayeon761)
- [#111](https://github.com/Orderly-Team24/team-24/pull/111) — remove stray file (dayeon761)
- [#110](https://github.com/Orderly-Team24/team-24/pull/110) — create file (dayeon761)
- [#109](https://github.com/Orderly-Team24/team-24/pull/109) — US-011-3 parser (adelinamikki)
- [#108](https://github.com/Orderly-Team24/team-24/pull/108) — US-011-1 frontend (rxxtzz)
- [#107](https://github.com/Orderly-Team24/team-24/pull/107) — US-011-4 frontend (vianevi)
- [#106](https://github.com/Orderly-Team24/team-24/pull/106) — OCR + Tesseract (Ramy678)
- [#105](https://github.com/Orderly-Team24/team-24/pull/105) — photo upload endpoint (dayeon761)
- [#104](https://github.com/Orderly-Team24/team-24/pull/104) — FastAPI + RAG (Ramy678)
- [#103](https://github.com/Orderly-Team24/team-24/pull/103) — menu (Ramy678)
- [#102](https://github.com/Orderly-Team24/team-24/pull/102) — PR template (dayeon761)
- [#101](https://github.com/Orderly-Team24/team-24/pull/101) — main.py (Ramy678)
- [#100](https://github.com/Orderly-Team24/team-24/pull/100) — ai_service.py (Ramy678)
- [#97](https://github.com/Orderly-Team24/team-24/pull/97) — system_promts (Ramy678)
- [#96](https://github.com/Orderly-Team24/team-24/pull/96) — user-stories (Ramy678)
- [#91](https://github.com/Orderly-Team24/team-24/pull/91) — CHANGELOG (dayeon761)
- [#90](https://github.com/Orderly-Team24/team-24/pull/90) — other-PBI (rxxtzz)
- [#89](https://github.com/Orderly-Team24/team-24/pull/89) — user-story (rxxtzz)
- [#88](https://github.com/Orderly-Team24/team-24/pull/88) — PR template (dayeon761)
- [#87](https://github.com/Orderly-Team24/team-24/pull/87) — bug-report (dayeon761)
- [#86](https://github.com/Orderly-Team24/team-24/pull/86) — course-task (dayeon761)
- [#85](https://github.com/Orderly-Team24/team-24/pull/85) — user-stories (dayeon761)
- [#56](https://github.com/Orderly-Team24/team-24/pull/56) — user_stories (dayeon761)

### Screenshots
**Product Backlog View**
![Product Backlog View](images/Product%20Backlog%20view.jpg)

**Sprint Backlog View**
![Sprint Backlog View](images/Sprint%20Backlog%20view.jpg)

**Sprint Milestone**
![Sprint Milestone](images/Sprint%20milestone.jpg) 

**MVP v1 Filtered / Grouped View**
![MVP Version Field](images/MVP%20version%20field%2C%20grouped%20view%2C%20or%20filtered%20view.jpg)

**SemVer Release**
![SemVer Release](images/SemVer%20release.jpg)

**Delivered MVP v1**
![Delivered MVP v1](images/Delivered%20MVP%20v1.jpg)

**Example Reviewed Issue-Linked PR**
![Example Reviewed Issue-Linked PR](images/Example%20reviewed%20issue-linked%20PR.jpg)
