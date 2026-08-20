# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

## Context Structure
- Working area: `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` — write here during the day, no date path needed. `/end-of-day` archives both into the dated locations below at day's end.
- Journal: `~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` — one file per day, daily log.
- Research: `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/` — one directory per day; `NN-{job}` is a zero-padded sequence number plus a short slug per one-off research task that day (e.g. `01-vendor-eval/`).
- Index: `index.md` files under `~/wiki/`, `journal/`, and `research/` are nav chains (year -> month -> day). `/end-of-day` rebuilds affected chains on each archive.
- Advisor: `~/wiki/advisor/YYYY/MM/YYYY-MM-DD.md` — one file per day, recurring friction and automation candidates from the last 14 days.
- Roadmap: `~/wiki/roadmap/{project}/{open,in-progress,done}/{epic-slug}/{story-slug}.md` — persistent EPIC/STORY/Task project schedule; state is which directory an item sits in, managed with `/roadmap`. Finished projects move to `~/wiki/roadmap/archive/{project}/`.- Today's context: before starting work, read `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` (if present) for what's already in progress today.
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/MM/YYYY-MM-DD-handoff.md` (highest date, may not be today or this month) for open items and carried decisions from the prior session.
- Format: every `~/wiki`/`spec` document and first-party source-code file carries the metadata/header described in `references/document-style/frontmatter.md`; read its frontmatter/header first, on every file, before the body.

@RTK.md

