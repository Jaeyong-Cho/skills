---
name: dev-grill-me
description: Run a @skills/grill-me interview covering both feature and fix concerns in one pass — intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan.
disable-model-invocation: true
---

# Dev Grill Me

**MUST RUN** `@skills/grill-me` covering every point in `../references/dev-checklist.md`, whether the work is a feature or a fix. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical.

## Checklist handling

Pass every point in `../references/dev-checklist.md` to `@skills/grill-me`. The shared grill-me rules own mode, impact, uncertainty, and action handling for the whole session. **MUST NOT** silently drop any checklist point — every one appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a grep/command output, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST** surface assertions aggressively wherever there is any uncertainty — for each, name the function/file, and whether it's a precondition, invariant, or postcondition, so `@skills/to-plan` can carry it into the plan's Assertions section as a real runtime assert (not a comment, not test-only).
**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-plan` by human to dump the recorded answers into a plan document.
