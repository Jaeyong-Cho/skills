---
name: req-grill-me
description: Run a @skills/grill-me interview to build an agile Story in one pass — persona, user value, trigger, happy/alternate/edge/negative scenarios, dependencies, INVEST check. Feeds a plan's Gherkin-style acceptance criteria and a manual QA procedure.
disable-model-invocation: true
---

# Story Grill Me

**MUST RUN** `@skills/grill-me` covering every point in `../references/req-checklist.md` to build the Story. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in `../references/req-checklist.md`: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a grep/command output, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST** surface assertions aggressively wherever there is any uncertainty — for each, name the scenario it belongs to and whether it's a precondition, invariant, or postcondition, so `@skills/to-plan` can carry it into the plan's Assertions section.
**MUST NOT** draft the Gherkin file or QA procedure before the frontier is empty — every scenario bullet still open above is a scenario the spec would get wrong.

Once complete, next step is `@skills/to-plan` by human to turn the recorded scenarios into a plan: its Acceptance criteria table (Given/When/Then, per `../references/requirement-engineering.md`) already *is* this Story's Gherkin scenarios, one row per scenario bullet in `../references/req-checklist.md`; its QA Procedure section is the human-executable check for each of those rows. `@skills/do-plan` then copies that QA Procedure into its report as a "Try it yourself" checklist, so the human sees plainly what changed and how to check it works, no digging through the diff.
