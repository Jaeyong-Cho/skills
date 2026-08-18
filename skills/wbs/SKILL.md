---
name: wbs
description: Break a big idea into an EPIC/STORY backlog — EPICs as business value, STORIES as the user-facing value delivered when done — no task-level breakdown. Invoke as /wbs.
disable-model-invocation: true
---

# WBS

A work breakdown stops at STORY, never Task. An EPIC is a slice of business value big enough to matter on its own; a STORY is the smallest slice where you can still answer "what can the user do, or get, once this ships?" A candidate that can't answer that is a Task — too small for this skill, and `/to-plan`'s action items handle it per STORY instead.

**MUST NOT** write into the target project's repo — this is a draft, not the persisted spec. It lands in the personal wiki; a STORY's own `/to-plan` materializes its slice into the target project's `spec/{epic-slug}/{story-slug}.md` (per `../references/spec-convention.md`) when that STORY is actually picked up.

1. **Follow document style.** Read `../references/document-style.md` first — conclusion (the destination) before detail (EPICs, then STORIES) governs every file this skill writes.
2. **Name the destination.** One or two sentences: what shipping the whole effort looks like, in business terms, not a feature list. Write it as the top of `wbs/overview.md` (see location below). Completion criterion: the destination sentence exists and the user has confirmed it.
3. **Fan out breadth-first.** Call the Skill tool for `grill-me`, breadth-first across the whole idea rather than deep on one thread — surface every EPIC first, then every STORY inside each, and for each ask what observable state proves it's done. Completion criterion: every EPIC has a name, a one-line business value, and a one-line completion criteria; every STORY under it has a name, a one-line user-facing value, and a one-line completion criteria.
4. **Reject task-sized candidates.** For every candidate STORY, ask "if this ships alone, what does the user notice?" No answer, or an internal/technical answer (e.g. "refactored the X module") → it's a Task: fold it into the STORY it serves instead of listing it separately. Completion criterion: every listed STORY has a user-observable value line.
5. **Write the backlog.** Same file shapes as the target project's spec convention, reused as drafts: one `{epic-slug}/index.md` per EPIC from `../template/spec-epic-index.md` (Business value and Completion criteria filled in, Stories list linking every STORY file), one `{epic-slug}/{story-slug}.md` per STORY from `../template/spec.md` (Value to user and Completion criteria filled in, AC left for `/to-plan` to fill when that STORY is picked up), and a top-level `index.md` from `../template/spec-index.md` linking every EPIC. Completion criterion: every EPIC and STORY from step 3 has its file with both its Business/Value and Completion criteria lines filled, and both index files link to it.
6. **Mark what's not yet sharp.** Anything sensed as part of the destination but not yet nameable as an EPIC or STORY goes one line per item into `index.md`'s Not yet specified section — never invented to hit a quota. Anything ruled out during grilling goes one line per item, with why, into its Out of scope section. Completion criterion: no filler EPIC/STORY exists solely to look complete.

## Location

Write everything under `~/wiki/today/research/{NN}-{slug}/wbs/` — `{slug}` a kebab-case slug of the destination (step 2), `{NN}` the zero-padded sequence number for today (count existing `NN-*` directories under `~/wiki/today/research/`, starting at `00`; reuse the same `{NN}-{slug}` directory if this session already has one for the same effort). `@skills/end-of-day` archives `today/research/` into the dated `~/wiki/research/` path at day's end.

Tell the user the EPIC/STORY count and the `wbs/index.md` path when done. Next: pick a STORY and run `/dev-grill-me` → `/to-plan` → `/do-plan` to break it into action items and ship it — `/to-plan` is what actually writes into the target project's `spec/`.
