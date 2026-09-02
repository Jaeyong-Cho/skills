---
name: to-code
description: Turn this session's l1-grill-me/l2-grill-me/l3-grill-me decisions directly into code, by invoking the matching l1-implement/l2-implement/l3-implement — no plan file. Invoke as /to-code.
disable-model-invocation: true
---

# To-Code

Turn a finished `l1-grill-me`/`l2-grill-me`/`l3-grill-me` session straight into working code, skipping `@skills/to-plan`'s plan file — the lighter path for a single flow/rule/mechanism that's already been grilled.

1. **Determine the input.** Default to this session's `l1-grill-me`/`l2-grill-me`/`l3-grill-me` decisions. If the user names a target not yet grilled this session, run the matching skill on it first (`l1-grill-me` for a flow, `l2-grill-me` for a business rule, `l3-grill-me` for a technical operation) — don't draft from assumption. Completion criterion: the level (L1/L2/L3) is stated, never assumed silently.
2. **Translate decisions into the description.** Fold every `Decision:`/`❓`-answered line from that level's checklist into the one plain-language description `l{1,2,3}-implement` expects — L1: Trigger + Sequence + Branches + End state; L2: Input + Rule + L3 dependency + Output; L3: Interface + Mechanism + Failure modes. No new decisions invented here — every sentence traces back to a line from step 1's session.
3. **Invoke the matching implement skill.** `@skills/l1-implement` / `@skills/l2-implement` / `@skills/l3-implement` with that description, per step 1's level.

Completion criterion: the matching `l{1,2,3}-implement` skill has run and reports a real file:line.

Tell the user exactly what that skill told you (file:line, what was reused vs. stubbed) — this skill adds no output of its own.
