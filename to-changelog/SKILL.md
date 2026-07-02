---
name: to-changelog
description: Manage .sot/changelog/{year}/{month-day}.md — append dated entries summarizing what changed. Use when the user says "add to changelog", "log this change", "write a changelog entry", "update the changelog", or after an implementation step lands and the change should be recorded.
---

# To Changelog

Manage `.sot/changelog/{year}/{month}-{day}.md` — one file per day, entries appended as changes land.

Format:
```markdown
# {YYYY-MM-DD}

- {summary of what changed} (`.sot/adr/{slug}.md` if it came from a plan)
```

## Add
1. Get today's date: run `date +%Y` for the year folder and `date +%m-%d` for the filename.
2. Read `.sot/changelog/{year}/{month-day}.md` (create it with a `# {YYYY-MM-DD}` header if missing — `mkdir -p .sot/changelog/{year}` first).
3. Append one bullet summarizing the change. Link the ADR if this change came from one.

Completion criterion: the day's changelog file has one bullet per change, each specific enough to understand what happened without opening the ADR.
