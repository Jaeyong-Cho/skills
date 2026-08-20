# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

## Context Structure
- **MUST read frontmatter/header first, on every file, before the body** — every `~/wiki`/`spec` document and first-party source-code file carries it; format in `references/document-style/frontmatter.md`. Always, even when the path is already known; skip the body entirely if the header alone answers the question. Applies to every wiki file touched by the rules below.
- Working area: `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` — write here during the day, no date path needed. `/end-of-day` archives both into the dated locations below at day's end.
- Journal: `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/}` — one nested directory per day; the directory contains journal.md (daily log), handoff.md (open items/decisions for tomorrow), report.md (end-of-day synthesis), and research/ (research tasks from that day).
- Index: `index.md` files under `~/wiki/` and `journal/` are nav chains (year -> month -> day). `/end-of-day` rebuilds affected chains on each archive.
- Roadmap: `~/wiki/roadmap/{project}/{open,in-progress,done}/{epic-slug}/{story-slug}.md` — persistent EPIC/STORY/Task project schedule; state is which directory an item sits in, managed with `/roadmap`. Finished projects move to `~/wiki/roadmap/archive/{project}/`.
- Notes: `~/wiki/notes/{fleeting,literature,permanent}/{slug}.md` — Zettelkasten-style note wiki; permanent notes are durable, own-words, densely linked ideas, fleeting/literature notes are raw/session/source capture, managed with `/to-notes`.
- Today's context: before starting work, read `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` (if present) for what's already in progress today.
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/MM/YYYY-MM-DD/handoff.md` (highest date, may not be today or this month) for open items and carried decisions from the prior session.
- Notes: before starting work, skim `~/wiki/notes/permanent/index.md` (and its category indexes, if split) for existing ideas relevant to the task, so prior conclusions aren't re-derived from scratch.

@RTK.md

