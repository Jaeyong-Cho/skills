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
- Deferred work (scoped out now but shouldn't be forgotten) — tag each with `TODO:` so `@skills/to-plan` records it in the plan's Deferred items list
- Root cause (for fix)
- Fundamental Solution (**MUST NOT** Ad-Hoc or Workaround)
- Architecture — components and interfaces
- Impact scope
- Observability and Monitoring
- Testability
- Branch to work this topic(git)
- New simple and representative testcase with **built program integration test**, not just unit test — name its fixture (real seed data, mock/stub setup, or existing state it needs) so the test isn't blocked writing it
- What I want — the observable outcome (a value, a state, a visible change), not a restatement of the intent above
- How to evaluate it — deterministic check for the line above: integration test or e2e test, per `../references/deterministic-evaluation.md`
- Release and ship plan
- Dogfood test

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark.

For every point in the checklist above: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one above appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST** surface assertions aggressively wherever there is any uncertainty — for each, name the function/file, and whether it's a precondition, invariant, or postcondition, so `@skills/to-plan` can carry it into the plan's Assertions section as a real runtime assert (not a comment, not test-only).
**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-plan` by human to dump the recorded answers into a plan document.
