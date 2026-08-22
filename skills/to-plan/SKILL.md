---
name: to-plan
description: Write up this session's decisions as a plan document — spec changes, acceptance criteria, action items. Invoke as /to-plan.
disable-model-invocation: true
---

# To-Plan

Turn this session's decisions into a plan document instead of leaving them to evaporate at the end of the chat.
Write a handoff document summarising the current conversation so a fresh agent can continue the work.
**MUST** instruct the detailed step-by-step so a cheap agent model can run.
**MUST NOT** skip or abstract the action items.

1. **Follow document style.** Read `../references/document-style.md` first — its Introduction/Abstraction/Detailed structure and size limits govern the draft.
2. **Follow ponytail style.** Run `/ponytail` (Skill tool) over the action items — cut speculative scope, keep each item to the smallest change that works.
3. **Follow deep module.** Read `../references/deep-modules.md` first - follow this philosophy.
4. **Follow TDD Rule.** Read `../references/tdd.md` to plan tdd development plan.
5. **Follow requirements engineering.** Read `../references/requirement-engineering.md` first — its Acceptance Criteria table (Given-When-Then, Category, Verification Method) is the format for step 6's Spec changes and Acceptance criteria below; Verification Method is what keeps the spec traceable to a real test.
6. **Follow ELI5.** Make plan the so a fresh cheapest model agent can understand.
7. **Draft the plan**, covering:
   - Target project (e.g. path of the repo)
   - Spec changes — locate the target project's spec file(s) per `../references/spec-convention.md` (`spec/{epic-slug}.md`, one per EPIC; create `spec/` if it doesn't exist yet). List each requirement being added, changed, or removed, one line each, grouped under its STORY.
   - Acceptance criteria — the same requirements as a table per `../references/requirement-engineering.md`; each row's Verification Method must name a real test file/path (existing or to be written), not "manual" unless the check genuinely can't be automated. This table is the link between the spec and its test cases — write it once, reuse it in both places. Pass all of the unit + integration test.
   - QA Procedure — one numbered, human-executable step per Acceptance criteria row, same order (precondition, exact steps to do, exact observable result to expect). No jargon — this is the doc a human with zero context uses to check the feature actually works.
   - Assertions — one line per point of uncertainty found in this session: name the function/file it belongs to, what it checks (precondition, invariant, or postcondition), and that it's a real runtime assert statement written directly in the implementation code at that point (`assert` in Python, `assert()`/`static_assert` in C++, etc.) — not a comment, not test-only. `@skills/do-plan` writes each line's assert as part of the action item that touches that function.
   - Commit
   - Release - **MUST CONFIRM** to the human before release.
   - Build — the target project's build command (e.g. `npm run build`, `make`), and confirmation it currently passes
   - Action items, each as `- [ ] {item}` — must include one item that writes the Spec changes and Acceptance Criteria rows into the target project's `spec/{epic-slug}/{story-slug}.md` file(s) and updates both `spec/{epic-slug}/index.md` and the top-level `spec/index.md`, so the persisted spec stays synchronized with this plan. `@skills/do-plan` executes and checks these off in place.
8. **Write it** to `~/wiki/today/research/{NN}-{slug}/plans/{nn}-{slug}.md`, creating the directory if needed — `{slug}` a kebab-case slug of the plan's topic, `{NN}` the zero-padded sequence number for today, starting at `00` (count existing `NN-*` directories under `~/wiki/today/research/`), `{nn}` the next zero-padded sequence number inside `plans/` (count existing files there; starts at `01`). `@skills/end-of-day` archives `today/research/` into the dated `~/wiki/journal/YYYY/MM/YYYY-MM-DD/research/` path at day's end.
9. **Split if too large.** If the file is large and many topics split it into `{nn}-{slug}-{part-slug}.md` files in the same `plans/` directory, one file per vertical slice — each file a complete, independently executable unit with its own acceptance criteria and action items, not a horizontal layer (e.g. not "backend" + "frontend" for one feature).

Completion criterion: the file (or files, if split) exists; spec changes, acceptance criteria, and action items are each present and traceable to something decided in this session; every acceptance criteria row names a real Verification Method; and an action item exists to write those rows into the target project's spec document.

Tell the user the file path(s), and that `@skills/do-plan` executes it, when done.
