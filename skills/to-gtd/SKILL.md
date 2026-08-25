---
name: to-gtd
description: File a @skills/gtd-grill-me session's bucketed items into the GTD system at ~/wiki/gtd/ — Next Actions, Projects, Waiting For, Someday/Maybe, Calendar, Reference — and keep it live afterward (check items off, move completed items/projects to ~/wiki/gtd/archive/yyyy/mm/). Invoke as /to-gtd.
disable-model-invocation: true
---

# To-GTD

The GTD system lives at `~/wiki/gtd/`, one file per list plus one file per project. **State is location**: a completed item isn't marked done in place, it's moved out to `~/wiki/gtd/archive/{yyyy}/{mm}/`, so nothing done keeps cluttering an active list. `next-actions.md` etc. already *are* the "what's next" view — no separate read/report step needed.

1. **Follow document style.** Read `../references/document-style/frontmatter.md` first — every list/project file below carries OKF frontmatter (six fields); `index.md`/`log.md` are exempt (reserved names).
2. **First run only — scaffold.** If `~/wiki/gtd/` doesn't exist yet: `mkdir -p ~/wiki/gtd/{projects,archive}`, write `index.md` and `projects/index.md` from `../template/gtd-index.md` and `../template/gtd-projects-index.md`. Don't create a list file (`next-actions.md`, etc.) until step 3 has something to put in it — an empty list is noise.
3. **File each bucketed item**, per its `@skills/gtd-grill-me` bucket (create the target file from its template on first use, whichever order the buckets were hit in):
   - **Next Action** — append `- [ ] {action}` to `next-actions.md` (from `../template/gtd-next-actions.md`), under its `## @{context}` heading if a context was given, else under `## Next`.
   - **Project** — write/update `projects/{project-slug}.md` from `../template/gtd-project.md`: an `## Outcome` line, and a `## Next Actions` checklist of its broken-down leaves. Link it from `projects/index.md`. Also `projects/context/{context-slug}.md` for context. 
   - **Waiting For** — append `- [ ] {what} — waiting on {who}, follow up {YYYY-MM-DD}` to `waiting-for.md` (from `../template/gtd-waiting-for.md`).
   - **Calendar** — append `- [ ] {YYYY-MM-DD}: {item}` to `calendar.md` (from `../template/gtd-calendar.md`), keeping the list sorted by date.
   - **Someday/Maybe** — append `- [ ] {item}` to `someday-maybe.md` (from `../template/gtd-someday-maybe.md`).
   - **Reference** — append `- {item}` to `reference.md` (from `../template/gtd-reference.md`).
   - **Trash / Do now** — nothing written; say so.
   Completion criterion: every non-Trash, non-Do-now bucket from the session has a corresponding line or file on disk.
4. **Link `~/wiki/gtd/index.md`** to any list file created for the first time in step 3.
5. **Complete or cancel an item** — asked for directly, any time, not just right after a grill-me session:
   - **Complete, single line** (Next Action / Waiting For / Calendar / Someday-Maybe) — remove its line from the source file, append one line to `archive/{yyyy}/{mm}/log.md` (today's date; `mkdir -p` the month dir and write its `index.md` from `../template/gtd-archive-month-index.md` if missing): `- {ISO timestamp} [{source list}] {item text}`.
   - **Complete, whole Project** (every leaf under `## Next Actions` checked) — append a `Completed: {date}` line to the project file, then move it to `archive/{yyyy}/{mm}/{project-slug}.md`; remove its entry from `projects/index.md`.
   - **Cancel** (no longer relevant, not done) — delete the line or project file outright, same places as Complete would touch, but skip the archive write — cancelled work doesn't get a log entry.
   - Link the month's `archive/{yyyy}/{mm}/index.md` to `log.md` and to any project archived that month; link that month from `archive/index.md` (from `../template/gtd-archive-index.md` if it's the first archive entry ever).
6. **Lint.** Run `python3 scripts/lint_gtd.py ~/wiki/gtd` (relative to this skill's directory) after every write in steps 3-5. Fix every reported violation and re-run before finishing — a red lint is not a done write.

Tell the user which files changed, and the lint result, when done.
