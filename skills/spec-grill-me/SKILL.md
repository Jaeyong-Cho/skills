---
name: spec-grill-me
description: Run a @skills/grill-me interview covering spec-writing concerns in one pass — intent, scope, functional/non-functional requirements, acceptance criteria, traceability, target spec file.
disable-model-invocation: true
---

# Spec Grill Me

**MUST RUN** `@skills/grill-me` covering every point below, whether the spec is new or an update. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical:

- Intent and purpose — what problem this spec solves, for whom
- Scope-in / scope-out
- User scenario — the concrete flow each acceptance criterion traces back to
- Functional requirements — what the system must do, one line each
- Non-functional requirements — performance, security, availability, usability
- Acceptance Criteria per `../references/requirement-engineering.md` — Given-When-Then, Category (normal/boundary/exception), Verification Method naming a real test
- Traceability — every AC row traces to a Requirements or User Scenario line; anything that doesn't goes to Out of Scope instead
- Conflicts and prioritization — any requirement that contradicts another, and which one wins
- Target spec file — per `../references/spec-convention.md` (`spec/{topic-slug}.md`, with `spec/index.md` updated in the same change)

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark.

**MUST** Use assertions aggressively wherever there is any uncertainty (e.g. an AC row with no automatable Verification Method).
**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-spec` by human to dump the recorded answers straight into the target project's spec — or `@skills/to-plan` instead if code work (action items, branch, release) is also needed.
