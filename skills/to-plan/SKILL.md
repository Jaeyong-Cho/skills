---
name: to-plan
description: Write up this session's decisions as a plan document — acceptance criteria, action items. Does not write a spec document. Invoke as /to-plan.
disable-model-invocation: true
---

# To-Plan

Turn decisions into a plan document instead of leaving them to evaporate at the end of the chat.
Write a handoff document summarising the current conversation so a fresh agent can continue the work.
**MUST** instruct the detailed step-by-step so a cheap agent model can run.
**MUST NOT** skip or abstract the action items.

1. **Determine the input.** Default to this session's decisions — whatever `@skills/dev-grill-me`/`@skills/req-grill-me` (or plain conversation) settled so far. If instead the user names a specific target when invoking this skill (an issue, a feature, a topic not yet discussed this session), scope the plan to that named target instead — and if it hasn't been grilled yet, run the checklist that fits (`@skills/dev-grill-me` for a feature/fix, `@skills/req-grill-me` for a Story) on it first, don't draft from assumptions. Completion criterion: the plan's scope is stated as either "this session" or a named target, never assumed silently.
2. **Follow document style.** Read `../references/document-style.md` first — its Introduction/Abstraction/Detailed structure and size limits govern the draft.
3. **Follow ponytail style.** Run `/ponytail` (Skill tool) over the action items — cut speculative scope, keep each item to the smallest change that works.
4. **Follow deep module.** Read `../references/deep-modules.md` first - follow this philosophy.
5. **Follow TDD Rule.** Read `../references/tdd.md` to plan tdd development plan.
6. **Follow requirements engineering.** Read `../references/requirement-engineering.md` first — its Acceptance Criteria table (Given-When-Then, Category, Verification Method) is the format for step 8's Acceptance criteria below; Verification Method is what keeps each criterion traceable to a real test.
7. **Follow ELI5.** Make plan the so a fresh cheapest model agent can understand.
8. **Draft the plan**, covering:
   - Target project (e.g. path of the repo)
   - Acceptance criteria — the session's decisions as a table per `../references/requirement-engineering.md`; each row's Verification Method must name a real test file/path (existing or to be written), not "manual" unless the check genuinely can't be automated. Pass all of the unit + integration test.
   - QA Procedure — one numbered, human-executable step per Acceptance criteria row, same order (precondition, exact steps to do, exact observable result to expect). No jargon — this is the doc a human with zero context uses to check the feature actually works.
   - Deferred items — one line per `TODO:`-tagged deferred item from the grill-me session (empty if none).
   - Assertions — one line per point of uncertainty found in this session: name the function/file it belongs to, what it checks (precondition, invariant, or postcondition), its uncertainty tag (High/Low, per `../references/grill-impact.md`), and that it's a real runtime assert statement written directly in the implementation code at that point (`assert` in Python, `assert()`/`static_assert` in C++, etc.) — not a comment, not test-only. `@skills/do-plan` writes each line's assert as part of the action item that touches that function, and runs `@skills/experiment` on every High-tagged line instead of trusting the assert/test alone.
   - Commit — draft the commit message now (why this change, not a file list); `@skills/do-plan` runs the real `git commit` with it only once every action item is checked, the build passes, unit + integration tests pass, and every acceptance criterion holds.
   - Release / Branch merge - **MUST CONFIRM** with the human before releasing or merging any branch. Once merged, `@skills/do-plan` removes the worktree named below and runs `git worktree prune`.
   - Worktree — the branch named in the grill-me session and the worktree path it gets (sibling to the repo: `../{repo-name}-{branch}`), e.g. `feature/x` at `../myrepo-feature-x`.
   - Build — the target project's build command (e.g. `npm run build`, `make`), and confirmation it currently passes; also name the unit and integration test commands so `@skills/do-plan` can run both before committing
   - Action items, each as `- [ ] {item}` — the first item **MUST** be creating the git worktree named above (`git worktree add {path} -b {branch}`), before any other action item runs; every later action item runs with that worktree as the working directory, not the main checkout. `@skills/do-plan` executes and checks these off in place.
     - **Abstraction level mark.** For an item that creates or changes a function/method, read `../references/abstraction-levels.md` and tag it with the level it belongs at: `- [ ] [L1] {item}` / `[L2]` / `[L3]`. For an `[L1]` item, also list the `[L2]`/`[L3]` functions it needs as their own action items (existing or new) — an L1 item with no L2 item under it is a smell per that doc. Every `[L2]`/`[L3]` item's Verification Method (in Acceptance criteria above) is the test that item's TDD cycle produces, per `abstraction-levels.md`'s Testing by level section — not a manual check.
   - Dogfood test
9. **Write it.** **MUST ASK** confirmation of the directory first, per `../references/question-format.md`'s ❓/➡️ format — recommend the current directory (`./plans/`) as the default, unless the user asks to file it under the wiki instead, in which case read `../references/research-topic-directory.md` first and confirm `{NN}-{slug}` the same way; skip re-asking if already confirmed earlier this session. Once confirmed, write to `./plans/{nn}-{slug}.md` (creating `plans/` if needed) or `{NN}-{slug}/plans/{nn}-{slug}.md` under `~/wiki/today/research/`, whichever was confirmed — `{nn}` the next zero-padded sequence number inside `plans/` (count existing files there; starts at `01`).
10. **Split if too large.** If the file is large and many topics split it into `{nn}-{slug}-{part-slug}.md` files in the same `plans/` directory, one file per vertical slice — each file a complete, independently executable unit with its own acceptance criteria and action items, not a horizontal layer (e.g. not "backend" + "frontend" for one feature).

Completion criterion: the file (or files, if split) exists; acceptance criteria and action items are each present and traceable to a decision from step 1's determined input (this session or the named target); every acceptance criteria row names a real Verification Method. This plan document is the only artifact — no spec document is written.

Tell the user the file path(s), and that `@skills/do-plan` executes it, when done.
