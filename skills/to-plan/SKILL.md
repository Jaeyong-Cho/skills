---
name: to-plan
description: Write up this session's decisions as a plan document — spec changes, acceptance criteria, action items. Invoke as /to-plan.
disable-model-invocation: true
---

# To-Plan

Turn this session's decisions into a plan document instead of leaving them to evaporate at the end of the chat.
Write a handoff document summarising the current conversation so a fresh agent can continue the work.

1. **Follow document style.** Read `../references/document-style.md` first — its Introduction/Abstraction/Detailed structure and size limits govern the draft.
2. **Follow ponytail style.** Run `/ponytail` (Skill tool) over the action items — cut speculative scope, keep each item to the smallest change that works.
3. **Follow deep module.** Read `../references/deep-modules.md` first - follow this philosophy.
4. **Follow TDD Rule.** Read `../references/tdd.md` to plan tdd development plan.
5. **Follow ELI5.** Make plan the so a fresh cheapest model agent can understand.
6. **Draft the plan**, covering:
   - Target project (e.g. path of the repo)
   - Spec changes
   - Acceptance criteria
   - Commit
   - Branch
   - Release
   - Action items, each as `- [ ] {item}` — `/do-plan` executes and checks these off in place
7. **Write it** to `~/wiki/research/{date}/{NN}-{slug}/plans/{nn}-{slug}.md`, creating the directory if needed — `{date}` from `date +%Y/%m/%Y-%m-%d`, `{slug}` a kebab-case slug of the plan's topic, `{NN}` the next zero-padded sequence number for that day (count existing `NN-*` directories under the day's folder), `{nn}` the next zero-padded sequence number inside `plans/` (count existing files there; starts at `01`).
8. **Split if too large.** If the file is large and many topics split it into `{nn}-{slug}-{part-slug}.md` files in the same `plans/` directory, one file per vertical slice — each file a complete, independently executable unit with its own acceptance criteria and action items, not a horizontal layer (e.g. not "backend" + "frontend" for one feature).

Completion criterion: the file (or files, if split) exists, and spec changes, acceptance criteria, and action items are each present and traceable to something decided in this session.

Tell the user the file path(s), and that `/do-plan` executes it, when done.
