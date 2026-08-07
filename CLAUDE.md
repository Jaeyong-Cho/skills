# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

@references/document-style.md

## Context Structure
- Working area: `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` — write here during the day, no date path needed. `/daily-report` archives both into the dated locations below at day's end.
- Journal: `~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` — one file per day, daily log.
- Research: `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/` — one directory per day; `NN-{job}` is a zero-padded sequence number plus a short slug per one-off research task that day (e.g. `01-vendor-eval/`).
- Goals: `~/wiki/goals/{slug}/` — persistent, multi-day research directory for an ongoing goal, tracked (active/done) in `~/wiki/goals.md`. Create with `daily-report/scripts/new_goal.sh <slug>`; `/daily-report` re-links every active goal into `today/research/NN-{slug}/` each day, and archives a goal marked `done` into `research/YYYY/MM/YYYY-MM-DD/NN-{slug}/` (that day's date) same as a one-off job.
- Index: `index.md` files under `~/wiki/`, `journal/`, `research/`, and `goals/` are nav chains (year -> month -> day); `/daily-report` rebuilds the `research/` and `goals/` chains on each archive.
- Advisor: `~/wiki/advisor/YYYY/MM/YYYY-MM-DD.md` — one file per day, recurring friction and automation candidates from the last 14 days.
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/MM/YYYY-MM-DD-handoff.md` (highest date, may not be today or this month) for open items and carried decisions from the prior session.

@RTK.md

