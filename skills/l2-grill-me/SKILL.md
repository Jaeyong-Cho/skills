---
name: l2-grill-me
description: Run a @skills/grill-me interview to nail down one L2 business rule — its domain input, decision logic/branches, and L3 interface dependency (if any) — before @skills/l2-implement builds it. Invoke as /l2-grill-me.
disable-model-invocation: true
---

# L2 Grill Me

**MUST RUN** `@skills/grill-me` covering every point in `../references/l2-checklist.md`, for the single business rule the user names. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

## Rule this business rule follows

Read `../references/abstraction-levels.md` first — the Rule point must read as a domain decision, never a technical mechanism; the L3 dependency point must name an interface, never a concrete implementation, per that doc's L2 rules.

## Impact Level and Uncertainty

Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in `../references/l2-checklist.md`: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST NOT** cover persona, user value, testability, or release plan — those belong to `@skills/dev-grill-me` / `@skills/req-grill-me`; this skill is scoped to the rule itself only.
**MUST NOT** start building before the frontier is empty.

Once complete, next step is `@skills/l2-implement` by human: the recorded Rule (and its L3 dependency) is the description that skill builds from.
