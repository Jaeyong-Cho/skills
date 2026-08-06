---
name: dev-grill-me
description: Run a /grilling interview covering both feature and fix concerns in one pass — intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan.
disable-model-invocation: true
---

# Dev Grill Me

Run `/grilling` covering every point below, whether the work is a feature or a fix:

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

Completion criterion: each point above has an explicit, recorded answer — not skipped — and **MUST NOT** implementation work has started.
Once complete, next step is `/to-plan` to dump the recorded answers into a plan document.
