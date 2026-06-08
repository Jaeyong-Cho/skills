---
name: to-minutes
description: Write a markdown minutes file from the current session's conversation. Reads the discussion that happened in this Claude session and produces a well-structured minutes-YYYY-MM-DD.md in the current directory. Sections are derived from the discussion topics — no fixed template, structure follows what was actually discussed. Use when user says "to-minutes", "write minutes", "summarize this session", "make meeting notes", or "write up what we discussed".
---

# to-minutes

Read the current session conversation. Write a markdown minutes file in the current directory.

## Process

1. **Read the conversation** — scan the full session for topics, decisions, and action items
2. **Derive structure** — choose sections based on what was actually discussed (no fixed template)
3. **Write the file** — save to `./minutes-YYYY-MM-DD.md` using today's date
4. **Confirm** — tell user the file path

## Output format

```md
# Minutes — YYYY-MM-DD

## [Topic derived from discussion]

...

## [Next topic]

...
```

- Use H2 for top-level topics, H3 for subtopics
- Bullet decisions with **Decision:** prefix
- Bullet tasks with **Action:** prefix and owner if mentioned
- Keep prose tight — bullets over paragraphs
- Do not invent content not discussed

## Rules

- File name: `minutes-YYYY-MM-DD.md` (today's date, not session start)
- Save to current working directory
- If session has no meaningful discussion, tell user and don't write a file
