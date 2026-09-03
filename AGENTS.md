# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

## Context Structure
- Knowledge base: `~/wiki/kb/` holds standing, reusable answers (preferences, decisions, facts) — check it before asking the human something that might already be settled there. Any hit — the KB already answers it — skip asking and mark the answer 📚, citing the doc path, so it stays visible/auditable. `@skills/to-kb` is the only thing that writes `hit_count`/`last_hit_at`.
- **MUST READ** first 10 line frontmatter when need to read some file — every `~/wiki`/`spec` document and first-party source-code file carries it; format in `references/document-style/frontmatter.md`. Always, even when the path is already known; skip the body entirely if the header alone answers the question. Applies to every wiki file touched by the rules below.
- Working area: `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` — write here during the day, no date path needed. `/end-of-day` archives both into the dated locations below at day's end.
- Journal: `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/}` — one nested directory per day; the directory contains journal.md (daily log), handoff.md (open items/decisions for tomorrow), report.md (end-of-day synthesis), and research/ (research tasks from that day).
- Index: `index.md` files under `~/wiki/` and `journal/` are nav chains (year -> month -> day). `/end-of-day` rebuilds affected chains on each archive.
- Today's context: before starting work, read `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` (if present) for what's already in progress today.
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/MM/YYYY-MM-DD/handoff.md` (highest date, may not be today or this month) for open items and carried decisions from the prior session.

@RTK.md
