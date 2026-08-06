---
applyTo: "**"
---

# Global Instructions

## Skill Journal Logging
Today's journal file: `~/wiki/journal/$(date +%Y)/$(date +%Y-%m-%d).md`. If it doesn't exist, skip logging.

- On invoking any skill, append: `- HH:MM:SS: SKILL start (model: MODEL_ID)` then an indented `  - skill: SKILL_NAME` line.
- On finishing that skill's work, append: `- HH:MM:SS: SKILL end` then an indented `  - summary: ONE_LINE_SUMMARY` line and `  - result: ONE_LINE_SUMMARY` line.
- Use `date +%H:%M:%S` for timestamps and append with `>>` (never overwrite).
