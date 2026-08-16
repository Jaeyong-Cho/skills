---
name: spec-grill-me
description: Run a @skills/grill-me interview covering spec-writing concerns for one or more spec topics in one pass — intent, scope, functional/non-functional requirements, acceptance criteria, story-to-task todos, traceability, target spec and todo files.
disable-model-invocation: true
---

# Spec Grill Me

**MUST RUN** `@skills/grill-me` covering every point below, whether the spec is new or an update. First settle how many spec topics are in scope — one `spec/{topic-slug}.md` per topic per `../references/spec-convention.md` — as the tree's first-round question; a request that spans unrelated areas (e.g. "auth" and "billing") is two or more topics, not one. Run every point below once per topic, as separate branches of the same grill-me design tree, not separate sessions — shared decisions (e.g. a conflict between two topics' requirements) surface naturally where the tree joins. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms — even when the topic itself is technical:

- Intent and purpose — what problem this spec solves, for whom
- Scope-in / scope-out
- User scenario — the concrete flow each acceptance criterion traces back to
- Functional requirements — what the system must do, one line each
- Non-functional requirements — performance, security, availability, usability
- Acceptance Criteria per `../references/requirement-engineering.md` — Given-When-Then, Category (normal/boundary/exception), Verification Method naming a real test
- Story to task breakdown — each sub-topic is one STORY (done means the user gets a specific value/feature); break it into one or more TASKs, each a concrete `- [ ] action` checklist that completes end-to-end, not layered by frontend/backend
- Traceability — every AC row traces to a Requirements or User Scenario line; anything that doesn't goes to Out of Scope instead
- Conflicts and prioritization — any requirement that contradicts another (within or across this session's topics), and which one wins
- Task ordering — which tasks block which, across this session's stories; what can run in parallel
- Target spec file — per `../references/spec-convention.md` (`spec/{topic-slug}.md` per EPIC, with `spec/index.md` updated in the same change)
- Target todo file — per `../references/todo-convention.md` (`todo/{task-slug}.md` per TASK, temp scratch, with `todo/index.md` as the EPIC/STORY/TASK WBS guide)

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark.

**MUST** Use assertions aggressively wherever there is any uncertainty (e.g. an AC row with no automatable Verification Method).
**MUST NOT** implementation work has started.
Once complete, next step is `@skills/to-spec` by human to dump the recorded answers straight into the target project's spec — or `@skills/to-plan` instead if code work (action items, branch, release) is also needed.
