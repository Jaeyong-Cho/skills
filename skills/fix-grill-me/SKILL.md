---
name: fix-grill-me
description: Run a /grilling interview scoped to a bug fix — root cause, regeneration, impact scope, observation, monitoring.
disable-model-invocation: true
---

# Fix Grill Me

Grill a bug fix before building it — the same interview as `/grilling`, aimed at the questions a fix plan skips.

1. **Run `mattpocock-skills:grilling`** (Skill tool, plugin-qualified — `grilling` alone won't resolve, it's a plugin skill) against the fix plan in this session.
2. **Cover every branch below**, on top of whatever grilling surfaces on its own:
   - Root cause
   - Regeneration
   - Impact scope
   - Observation
   - Monitoring

**MUST NOT** write or edit code, or start implementing the fix, as part of this skill — grilling only. Stop once every branch is answered and hand back to the user to decide next steps.

Completion criterion: each branch above has an explicit, recorded answer — not skipped — and no implementation work has started.
