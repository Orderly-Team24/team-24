# Definition of Done

A Product Backlog Item (PBI) may be marked as Done only when all of the following conditions are satisfied.

## General Requirements

- All acceptance criteria defined in the issue are satisfied.
- The implementation matches the requirements described in the issue.
- The work has been reviewed by at least one other team member.
- Required tests and validation checks pass successfully.
- Verification evidence is available through normal workflow artifacts (issues, pull requests, comments, screenshots, test results, etc.).
- All related documentation is updated if affected by the change.

## User Stories

For a User Story to be considered Done:

- All linked supporting PBIs required for implementation are completed.
- Implementation evidence is available in linked issues and pull requests.
- Review evidence is available.
- Verification evidence is available.

## Implementation and Supporting PBIs

For implementation or supporting PBIs:

- The related pull request is linked to the issue.
- The pull request has been reviewed and approved.
- All required checks pass.
- The pull request is merged into the protected default branch using a merge commit.

## Repository Requirements

- The related issue is updated with the final status.
- The pull request references the related issue.
- Branch naming follows the project convention:
  `<issue-number>-short-description`.
- For every user-visible change, `CHANGELOG.md` is updated before the pull request is merged.

## Final Condition

A PBI may be marked Done only when:

1. Its issue-specific acceptance criteria are satisfied.
2. This Definition of Done is fully satisfied.
