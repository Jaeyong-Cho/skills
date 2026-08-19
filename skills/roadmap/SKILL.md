---
name: roadmap
description: Manage a project's roadmap with the user however it comes up — create/breakdown, read (today's work), update (deadlines, fixes, state), delete, or anything else about it. The only fixed rule is state = directory location. Invoke as /roadmap.
disable-model-invocation: true
---

# Roadmap

A project's roadmap as a tree — EPIC > STORY > Task — governed by exactly two fixed rules; nothing else about this skill's purpose is fixed:

1. **State is location.** Which of `open/`, `in-progress/`, `done/` an EPIC's directory sits under *is* its state — moving it (`mv`) is the state change, never a separate status field to drift out of sync. STORIES nest inside their EPIC as a single file (`{epic-slug}/{story-slug}.md`) and move with it.
2. **This manages the roadmap, not the spec.** It never writes into a target repo's `spec/`, and has nothing to do with `/to-plan` or `/do-plan`. A `{project}` here is personal/organizational, not a code repo — it may span several repos or none.

Follow the user's input, not a script: whatever they raise about a project's roadmap is in scope. The patterns in step 3 are what's been seen so far, not an exhaustive menu — something that fits none of them is still in scope if it's about the roadmap or its directory layout.

1. **Follow document style.** Read `../references/document-style/` first, starting with `understanding-and-structure.md` — every Goal below is conclusion-first and as long as the item warrants, never truncated to fit a fixed sentence count.
2. **Find the project(s) in play.** A topic scoped to one project (a deadline, a breakdown, a specific EPIC/STORY) needs `{project}` (kebab-case slug) named — ask if not given. A topic that spans the whole roadmap (e.g. "what's on my plate today") doesn't — scan every `~/wiki/roadmap/{project}/` instead.
3. **Run grill-me open-ended.** `@skills/grill-me` over whatever came up, grouped CRUD-style. Fix is an Update, not its own category — a misnamed, mis-scoped, or misplaced item gets corrected in place, same as a deadline edit.
   - **Create**
     - New project — `mkdir -p ~/wiki/roadmap/{project}/{open,in-progress,done}`, write `{project}/index.md` from `../template/roadmap-project-index.md`. Write `~/wiki/roadmap/index.md` from `../template/roadmap-index.md` too if it's the first project ever.
     - New EPIC — settle its name, goal, deadline, and STORIES (each with a goal, an optional own deadline that inherits the EPIC's when unset, and its first Tasks). Write `open/{epic-slug}/index.md` from `../template/roadmap-epic-index.md`, and `open/{epic-slug}/{story-slug}.md` per STORY from `../template/roadmap-story.md`.
     - Breakdown — a Goal too broad/fuzzy to act on directly: decompose it into new STORIES (or a STORY into new Tasks), same as a new EPIC.
   - **Read** — "what's next" / "today": report, don't write. Every unchecked `- [ ]` Task under any `in-progress/` STORY, plus every EPIC/STORY whose deadline has passed or falls within 7 days, sorted soonest-first, scoped per step 2.
   - **Update**
     - Deadline — edit the Deadline line in that EPIC's or STORY's `index.md`.
     - Content — edit a Goal or Task line in place.
     - Fix — rename a misnamed item (its directory/file + `#` heading), re-parent a STORY to a different EPIC (`mv {epic-a}/{story-slug}.md {epic-b}/{story-slug}.md`), or split/merge EPICs (`mkdir`/`mv`/`rmdir`).
     - State — `mv` the EPIC's whole directory between `open/`, `in-progress/`, `done/`; its STORIES move with it.
     - Project done — only once every EPIC under `{project}/` sits in `done/`: `mv ~/wiki/roadmap/{project} ~/wiki/roadmap/archive/{project}`, then move its entry in `~/wiki/roadmap/index.md` from Projects to Archive.
   - **Delete** — `rm -r` an EPIC's directory or `rm` a STORY's file outright (Task: edit its line out). Reserved for cancelled or no-longer-relevant work; finished work is an Update (`mv` to `done/`), never a delete.
4. **Keep every index.md in sync.** Apply each decision as it's reached rather than batching to the end. Completion criterion: every decision reached in the conversation is reflected on disk, and every index.md between the changed path and `~/wiki/roadmap/index.md` (its state's, its project's, the top-level one) links exactly what currently exists — no dangling links, no missing ones.

Tell the user which files changed and their paths when done.
