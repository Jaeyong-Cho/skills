---
name: dev-grill-me
description: Run a @skills/grill-me interview covering both feature and fix concerns in one pass — intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan.
disable-model-invocation: true
---

# Dev Grill Me

**MUST RUN** `@skills/grill-me` covering every point below, whether the work is a feature or a fix. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical:

- Human Acceptance Criteria (HAC) - (**MUST CHECK** which result make human agree and satisfy when this topic is done: detailed step-by-step e.g. run test script, see the db result, found the expected column...)
- Intent and purpose
- Scope-in / scope-out
- Expected
- Root cause (for fix)
- Fundamental Solution (**MUST NOT** Ad-Hoc or Workaround)
- Architecture — components and interfaces
- Impact scope
- Observability and Monitoring
- Testability
- Branch (git)
- New simple and representative testcase with **built program integration test**, not just unit test
- Release and ship plan

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark.

For every point in the checklist above: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round.

**MUST** surface assertions aggressively wherever there is any uncertainty — for each, name the function/file, and whether it's a precondition, invariant, or postcondition, so `@skills/to-plan` can carry it into the plan's Assertions section as a real runtime assert (not a comment, not test-only).
**MUST NOT** skip this reference for low-impact findings: every finding still gets marked with its impact level and uncertainty and shown, even when the Action rule says to skip asking it outright.
**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-plan` by human to dump the recorded answers into a plan document.
