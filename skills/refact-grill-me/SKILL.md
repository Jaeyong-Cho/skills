---
name: refact-grill-me
description: Run a @skills/grill-me interview to refactor a named function or usecase sequence against references/abstraction-levels.md's L1/L2/L3 rule — current shape and smells, behavior-preservation baseline, target decomposition. Invoke as /refact-grill-me.
disable-model-invocation: true
---

# Refact Grill Me

**MUST RUN** `@skills/grill-me` covering every point in `../references/refact-checklist.md`, for the function or usecase sequence the user names. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical.

## Rule this refactor follows

Read `../references/abstraction-levels.md` first — every "Current shape" and "Target decomposition" answer classifies against its L1/L2/L3 table and smells table. Open `../references/abstraction-levels/full-guidelines.md` only when the human asks why a smell matters or wants the Good/Bad example behind it.

## Impact Level and Uncertainty

Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in `../references/refact-checklist.md`: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a test-run output, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST NOT** refactor while RED. If the Behavior-preservation baseline point finds no test covering the target, the first action item is writing that characterization test and getting it green — before any structural change, per `tdd-refactoring.md`.
**MUST NOT** change behavior. Refactoring changes structure only; a test that breaks mid-refactor means behavior changed — undo and retry, don't push through.
**MUST NOT** start the refactor before the frontier is empty.

Once complete, next step is `@skills/to-plan` by human: each Target decomposition line becomes its own action item tagged `[L1]`/`[L2]`/`[L3]`, per `to-plan`'s Abstraction level mark step, so `@skills/do-plan` builds each resulting function to that level's rule.
