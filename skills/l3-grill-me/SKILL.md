---
name: l3-grill-me
description: Run a @skills/grill-me interview to nail down one L3 technical operation — its interface, the mechanism itself, and its failure modes — before @skills/l3-implement builds it. Invoke as /l3-grill-me.
disable-model-invocation: true
---

# L3 Grill Me

**MUST RUN** `@skills/grill-me` covering every point in `../references/l3-checklist.md`, for the single technical operation the user names. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical.

## Rule this mechanism follows

Read `../references/abstraction-levels.md` first — the Mechanism point must hide the SDK/HTTP/DB details behind the Interface point, with no business decision inside, per that doc's L3 rules.

## Impact Level and Uncertainty

Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in `../references/l3-checklist.md`: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a `--help`/vendor-doc reference, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST NOT** cover persona, user value, testability, or release plan — those belong to `@skills/dev-grill-me` / `@skills/req-grill-me`; this skill is scoped to the mechanism itself only.
**MUST NOT** start building before the frontier is empty.

Once complete, next step is `@skills/l3-implement` by human: the recorded Interface and Mechanism (and its Failure modes) is the description that skill builds from.
