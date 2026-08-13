# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

@references/document-style.md

## Context Structure
- Working area: `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` — write here during the day, no date path needed. `/end-of-day` archives both into the dated locations below at day's end.
- Journal: `~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` — one file per day, daily log.
- Research: `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/` — one directory per day; `NN-{job}` is a zero-padded sequence number plus a short slug per one-off research task that day (e.g. `01-vendor-eval/`).
- Goals: `~/wiki/goals/{slug}/` — persistent, multi-day research directory for an ongoing effort, created directly (`mkdir`) and symlinked into `today/research/NN-{slug}/` when the work is judged to be multi-day. No registry file; existence and lifecycle are model-tracked from journal/handoff context. `/end-of-day` asks which goal symlinks are finished, then moves those into `goals/YYYY/MM/NN-{slug}/` (archived by the month it finished, not by day); still-active ones are archived as symlinks alongside that day's research.
- Index: `index.md` files under `~/wiki/`, `journal/`, and `research/` are nav chains (year -> month -> day); `goals/` is a year -> month chain. `/end-of-day` rebuilds affected chains on each archive.
- Advisor: `~/wiki/advisor/YYYY/MM/YYYY-MM-DD.md` — one file per day, recurring friction and automation candidates from the last 14 days.
- Today's context: before starting work, read `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` (if present) for what's already in progress today.
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/MM/YYYY-MM-DD-handoff.md` (highest date, may not be today or this month) for open items and carried decisions from the prior session.
- Human: `~/wiki/human/` — human-only space. Never write, edit, or delete here.

@RTK.md
