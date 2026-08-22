---
name: story-grill-me
description: Run a @skills/grill-me interview to build an agile Story in one pass — persona, user value, trigger, happy/alternate/edge/negative scenarios, dependencies, INVEST check. Feeds a Gherkin specification and a manual QA procedure.
disable-model-invocation: true
---

# Story Grill Me

**MUST RUN** `@skills/grill-me` covering every point below to build the Story. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms:

- Persona (who hits this — a real user role, not "the system")
- User value (the "so that" — what they get, what breaks or stays missing without it)
- Trigger (the event or context this scenario starts from)
- Happy path scenario (Given/When/Then — the one flow that must work)
- Alternate scenarios (other valid Given/When/Then paths to the same value)
- Edge cases (boundary: empty, max, first-of-its-kind, exactly-at-the-limit)
- Negative scenarios (invalid input, denied permission, failure — Given/When/Then too)
- Out of scope
- Dependencies / preconditions (data, state, other stories that must land first)
- Git branch (fit/*, feature/*, refactor/*, ...)
- **INVEST** check (Independent, Negotiable, Valuable, Estimable, Small, Testable) — a Story failing any letter goes back into the round, not into the spec

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark.

For every point in the checklist above: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round.

**MUST** surface assertions aggressively wherever there is any uncertainty — for each, name the scenario it belongs to and whether it's a precondition, invariant, or postcondition, so `@skills/to-plan` can carry it into the plan's Assertions section.
**MUST NOT** draft the Gherkin file or QA procedure before the frontier is empty — every scenario bullet still open above is a scenario the spec would get wrong.

Once complete, next step is `@skills/to-plan` by human to turn the recorded scenarios into a Story spec: its Acceptance criteria table (Given/When/Then, per `../references/requirement-engineering.md`) already *is* this Story's Gherkin scenarios, one row per scenario bullet above; its Spec changes section already covers the persona/user-value ("Value to user"); its QA Procedure section is the human-executable check for each of those rows. `@skills/do-plan` then copies that QA Procedure into its report as a "Try it yourself" checklist, so the human sees plainly what changed and how to check it works, no digging through the diff.
