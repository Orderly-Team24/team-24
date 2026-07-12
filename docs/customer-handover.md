# Customer Handover — Orderly

This page answers the practical questions a customer needs answered: what you're getting, what you can do with it today, what still depends on the team, and what to watch out for. It's updated whenever any of that changes.

## In short

- **The product is live and usable today** at https://team-24-navy.vercel.app/ — you can create an account and use it right now.
- **Hosting is still owned by the team**, not you. The website, the two backend services, the database, and the AI (OpenAI) account all run under the team's own accounts. You have not been given login access to any of them yet.
- **You have not taken over operating the product yourself.** If that's something you want, it's an open item — see "What's not decided yet" below.

## What you can do right now

| You want to... | Where |
|---|---|
| Use the app | https://team-24-navy.vercel.app/ |
| See what it does and how it's set up | [README.md](../README.md) — includes a plain "how do I use it" walkthrough |
| See everything that's changed, sprint by sprint | [CHANGELOG.md](../CHANGELOG.md) |
| See what's planned next | [docs/roadmap.md](roadmap.md) |
| Check a specific feature works the way it should | [docs/user-acceptance-tests.md](user-acceptance-tests.md) — step-by-step scenarios you (or the team, with you) can run |

## Who owns what, right now

| Piece | Who runs it today |
|---|---|
| The website (team-24-navy.vercel.app) | Team's Vercel account. Updates automatically whenever the team pushes code. |
| The two backend services (recommendations, menu photo scanning) | Team's Render account. Same auto-update behavior. |
| The database (user accounts, preferences) | Team's Render account. |
| The AI used for recommendations (OpenAI) | Team's OpenAI account/API key. Not shared with you. |
| The code itself (GitHub repository) | Public — anyone can read it — but the team still administers it. |

**Nothing above has been formally handed to you yet.** That's not necessarily a problem — plenty of teams keep operating a product for a customer rather than transferring hosting — but it's something to explicitly decide, not assume.

## What's not decided yet

- Whether you want your **own** hosting (your own Vercel/Render/OpenAI accounts) instead of continuing to depend on the team's, or whether the team continuing to host it is fine with you.
- What level of access you want (dashboard access to see logs/uptime? Full account ownership? Nothing, just use the product?).

These were raised as open questions at the Week 6 review — see `reports/week6/README.md` for that conversation's outcome once recorded.

## Things you should know before relying on this beyond the course

- **User accounts/passwords are on a hardcoded secret key**, not one only the team controls securely. In plain terms: the code that verifies login sessions uses a fixed value written directly into the source code instead of a private setting. This is fine for a course project but should be fixed (moved to a private setting, changed) before this is used as a real product with real users' data.
- **Order history and "disliked" dishes are not permanently saved yet** — they live in the server's short-term memory and disappear every time the service restarts (which happens periodically, even without anyone doing anything). Don't rely on order history sticking around long-term yet.
- **The AI won't always perfectly understand free-text requests** typed into the "what are you in the mood for" field. Allergies and things you've explicitly excluded are strictly enforced — those are never violated. But open-ended phrasing ("something light and warm") is best-effort, not a strict guarantee.
- **Scanning menu photos handles single-column and standard two-column layouts**, including $/€/£/₽ prices and both "12.50" and European "12,50" formats. It does not yet handle 3+ columns, unevenly split columns, or handwritten specials boards.

## If something breaks or needs to be recreated

- How to run it locally / redeploy: [README.md § Getting started](../README.md#getting-started-local-development).
- How to make a change: [CONTRIBUTING.md](../CONTRIBUTING.md).
- The exact settings (environment variables) each service needs are listed in [docs/development-process.md § Configuration Management](development-process.md#configuration-management) — this is the reference the team uses to recreate a service from scratch if needed.
- There is currently no customer-facing backup/restore process for the database — this is called out as a known gap, not hidden.

## Is the documentation good enough? What help do you still need?

**Team's own view going in:** we think README.md + this page are enough for someone technical to understand and run the product independently. We do **not** think it's enough yet for someone to take over *hosting/operating* it themselves — that's a separate step nobody has done yet (see "What's not decided yet" above).

**Customer's view (Week 6 review, 10.07.2026):** README.md and CONTRIBUTING.md were reviewed live. Feedback: this document and the README were missing a clear, non-technical user guide for using the product independently — noted as the main documentation gap. That gap has since been addressed (see the new "User guide" section in [README.md](../README.md) and the plain-language rewrite of this page) as a direct action item from that meeting.

## Where things stand on handover

We're using three straightforward labels to track this, so it's always clear where things stand — no reading between the lines required.

- **How far along is the handover?** → **Ready for you to use independently.** The product is live and usable end-to-end; you have not yet taken over hosting/operating it yourself (see "Who owns what" above) — that remains a separate, not-yet-started step if you want it.
- **Have you confirmed you're happy with where things stand?** → **Yes, with follow-up items.** At the Week 6 review (10.07.2026) you approved the delivered features (order history, dislikes, AI safety fixes) and accepted this handover document as an accurate reflection of the current state, "noting that while dependencies aren't ideal, the handover is acceptable for now."
- **Follow-up items from that review** (owned by the team, due before Week 7 wraps):
  - Add a clear, non-technical user guide — **done** this same day (README.md § User guide, and this page's plain-language rewrite).
  - Meal-type recommendation filtering (breakfast/lunch/dinner) felt unstable in places beyond the specific scenario tested — scheduled for Sprint 5.
  - Remove a stray/confusing "Recommendations" nav button — scheduled for Sprint 5.
  - Add a free-text dietary-preference field (vegan, halal, etc.) — scheduled for Sprint 5.
  - Whether you want your own hosting instead of continuing to depend on the team's — still an open question, not yet raised for a decision (see "What's not decided yet" above).

Full meeting record: [reports/week6/sprint-review-summary.md](../reports/week6/sprint-review-summary.md), [reports/week6/sprint-review-transcript.md](../reports/week6/sprint-review-transcript.md).
