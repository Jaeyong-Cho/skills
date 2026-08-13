---
name: dev-grill-me
description: Run a @skills/grill-me interview covering both feature and fix concerns in one pass — intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan.
disable-model-invocation: true
---

# Dev Grill Me

Run `@skills/grill-me` covering every point below, whether the work is a feature or a fix. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical:

- Intent and purpose
- Scope-in / scope-out
- Value for end-user
- Expected
- Root cause (for fix)
- Fundamental Solution (**MUST NOT** Ad-Hoc or Workaround)
- Architecture — components and interfaces
- Impact scope
- Observability and Monitoring
- Testability
- Branch (git)
- New simple and representative testcase
- Release and ship plan

## Grill ME Level
- 0: When the first feature or functionality implementation, ask the big, important decision branch (skip details)
- 1: When the revise the existing feature or functionality, ask more details decision branch
- 2: When the bug fix, important feature, ask maximum decision branch
**MUST SHOW** The level to user before starting grill-me session

**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-plan` to dump the recorded answers into a plan document.
