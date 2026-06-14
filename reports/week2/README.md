# Week 2 Report – Orderly

## Project information
- **Name:** Orderly – Food Recommendation App
- **Short description:** A web app that helps users choose dishes from restaurant menus based on their preferences and budget.
- **License:** [MIT](../../LICENSE) 

## Documents
- [User Stories](user_stories.md)
- [MVP v0 Report](mvp-v0-report.md)
- [Customer Meeting Summary](customer-meeting-summary.md)
- [Customer Meeting Transcript](customer-meeting-transcript.md)
- [Analysis](analysis.md)
- [LLM Report](llm-report.md)

## Prototype (Figma)
[Figma Prototype](https://www.figma.com/design/BK4oKfBZo6r8RxjTanLQ3z/Untitled?t=Dx8jl21S5zCeA3az-0)

## MVP v0 deployment
- **Deployment URL:** https://keen-pegasus-a95a6a.netlify.app/
- **Run instructions:** Open the link above. No installation required.
- **Video demonstration:** https://youtu.be/CKgT0l3MgDk?si=0FWBhFiLGvoZRtDo

## Screenshots
- [Branch protection settings](images/branch-protection.png)
- [Reviewed MR example](images/mr-review.png)
- [Prototype screenshots](images/prototype.png)
- [MVP v0 screenshot](images/mvp-v0.png)

## Coverage

### Prototype (Figma)
The prototype covers the following user story IDs:
**US-001, US-002, US-004, US-005**

It demonstrates:
- Preferences screen
- Budget input + menu upload
- Recommendation result with three action buttons


### MVP v0 (technical foundation)
The deployed MVP v0 establishes the client-side infrastructure for:
- **US-001** - Propose dishes according to the budget
- **US-004** – Propose dishes according to preferences
- **US-005** - No allergen suggestions

Full implementation of these stories is planned for MVP v1.

## Customer meeting
- [Meeting summary](customer-meeting-summary.md)
- [Transcript published](customer-meeting-transcript.md)
## Links verification (Lychee)
- **Configuration:** [.lychee.toml](../../.lychee.toml)
- **Latest pipeline:**
- **Excluded links justification:** 
  - `https://www.figma.com/*` – Figma blocks automated requests (403). All Figma links were manually verified in a browser on 2026-06-14 and work correctly.
- **Manual verification date:** 2026-06-14 – all excluded links confirmed accessible 

## Merge Requests & Code Review
- **MR Template:** [.gitlab/merge_request_templates/Default.md](../../.gitlab/merge_request_templates/Default.md)
- **Example reviewed MR:** [PR #16 - Create .lychee.toml](https://github.com/Orderly-Team24/team-24/pull/16)
