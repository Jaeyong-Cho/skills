# Global Instructions

## Communication Rule
Communicate like an experienced engineering lead: lead with the conclusion, be concise and specific, separate facts from analysis, highlight risks and trade-offs, and always provide clear next actions.

Unless the user specifies otherwise, write and communicate only in English.

@references/document-style.md

@RTK.md

## Skill Journal Logging
Today's journal file: `~/wiki/journal/$(date +%Y)/$(date +%Y-%m-%d).md`. If it doesn't exist, skip logging.

- On invoking any skill, append: `- HH:MM:SS: SKILL start (model: MODEL_ID)` then an indented `  - skill: SKILL_NAME` line.
- On finishing that skill's work, append: `- HH:MM:SS: SKILL end` then an indented `  - summary: ONE_LINE_SUMMARY` line and `  - result: ONE_LINE_SUMMARY` line.
- Use `date +%H:%M:%S` for timestamps and append with `>>` (never overwrite).
