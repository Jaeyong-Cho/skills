# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

@references/document-style.md

@RTK.md

## Context Structure
- Journal: `~/wiki/journal/YYYY/YYYY-MM-DD.md` — one file per day, daily log.
- Research: `~/wiki/research/YYYY/YYYY-MM-DD/NN-{job}/` — one directory per day; `NN-{job}` is a zero-padded sequence number plus a short slug per research task that day (e.g. `01-vendor-eval/`).
- Handoff: before starting work, check the most recent `~/wiki/journal/YYYY/YYYY-MM-DD-handoff.md` (highest date, may not be today) for open items and carried decisions from the prior session.

## Skill Journal Logging
Today's journal file: `~/wiki/journal/$(date +%Y)/$(date +%Y-%m-%d).md`. If it doesn't exist, skip logging.

- On invoking any skill, append: `- HH:MM:SS: SKILL start (model: MODEL_ID)` then an indented `  - skill: SKILL_NAME` line.
- On finishing that skill's work, append: `- HH:MM:SS: SKILL end` then an indented `  - summary: ONE_LINE_SUMMARY` line and `  - result: ONE_LINE_SUMMARY` line.
- Use `date +%H:%M:%S` for timestamps and append with `>>` (never overwrite).
