# Definition of Done

A Product Backlog Item (PBI) may be marked as **Done** only when all of the following conditions are satisfied.

## 1. Issue-Specific Requirements
- All acceptance criteria defined in the issue are satisfied.
- The implementation matches the requirements described in the issue.
- The work has been reviewed by at least one other team member, and review evidence (comments, approvals) is linked in the PR/MR.

## 2. Quality Assurance & Testing
- **Automated Tests:** All required unit tests, integration tests, and quality requirement tests (QRTs) pass successfully.
- **Coverage:** Critical modules meet the minimum automated line coverage threshold (30%).
- **Documentation:** All relevant documentation (including `docs/testing.md`, `docs/quality-requirements.md`, and `docs/user-acceptance-tests.md`) is updated to reflect changes.
- **Manual Evidence:** If automation is not feasible for a specific requirement, manual testing evidence is documented as per project standards.

## 3. CI/CD and Quality Gates
- **CI Pipeline:** All CI checks required for the product stack—including linting, formatting/type checking, and automated tests—must pass on the Pull Request.
- **Additional QA Check:** The mandatory additional automated QA check (e.g., dependency vulnerability scanning or static analysis) must pass.
- **Branch Protection:** The PR is merged into the protected default branch only after all status checks are passing.

## 4. Repository and Traceability Requirements
- **Traceability:** The PR references the related issue number.
- **Changelog:** For every user-visible change, `CHANGELOG.md` is updated before the PR is merged.
- **Branching:** Branch naming follows the convention: `<issue-number>-short-description`.
- **Status:** The related issue is updated with its final status upon merge.

## 5. Maintenance Obligation
- When project work changes the product stack, architecture, quality requirements, or CI configuration, the `Definition of Done` must be updated to maintain the current completion standard. 

---

**Final Condition:** A PBI may be marked Done only when its issue-specific acceptance criteria are satisfied AND this global Definition of Done is fully satisfied.
