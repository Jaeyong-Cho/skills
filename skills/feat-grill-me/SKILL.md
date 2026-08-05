---
name: feat-grill-me
description: Run a /grilling interview scoped to a new feature — scope, expected state, architecture, observability, testability, release plan.
disable-model-invocation: true
---

# Feat Grill Me

Grill a feature plan before building it — the same interview as `/grilling`, aimed at the questions a feature spec skips.

1. **Run `mattpocock-skills:grilling`** (Skill tool, plugin-qualified — `grilling` alone won't resolve, it's a plugin skill) against the feature plan in this session.
2. **Cover every branch below**, on top of whatever grilling surfaces on its own:
   - Scope-in / scope-out
   - Expected state
   - Architecture — components and interfaces
   - Observability
   - Testability
   - Release and ship plan

Completion criterion: each branch above has an explicit, recorded answer — not skipped — and no implementation work has started.
