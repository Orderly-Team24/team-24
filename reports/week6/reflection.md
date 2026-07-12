## Week 6 Reflection

## Learning points
- Learned that small frontend routing mistakes (missing route, wrong redirect) can completely block users from using the app.
- Learned that AI recommendations need extra safety checks on the backend (right now the LLM can still suggest allergens, since filtering logic isn't strict enough).
- Understood that transition documentation (CONTRIBUTING.md, AGENTS.md, customer handover doc) needs to be written before the last sprint, not during it.

## Validated assumptions
- Confirmed that customer UAT is the most effective way to find real usability issues.
- Confirmed that fixing bugs found during UAT is more valuable than adding new features at this stage of the project.

## Friction and gaps
- Several bugs were found only during the customer meeting, which means that internal testing wasn't careful enough.
- Some issues (allergen filtering, order history identity mismatch) turned out to be more complex than expected.
- Transition documentation was added late in the sprint, which left less time to review it properly.

## Planned response
- Start writing handover and transition documents earlier in future sprints.
- Add more edge case checks to the AI recommendation pipeline to prevent safety issues.
- Keep running UAT sessions to catch issues before the final handover.
