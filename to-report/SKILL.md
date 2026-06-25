---
name: to-report
description: Write the current conversation or discussion as a structured markdown report to reports/{timestamp}-{slug}.md in the current directory. Use when user says "write a report", "save this discussion", "export to markdown", "to-report", "save report", or invokes /to-report.
---

# To Report

If `intents/` exists in the project root, read files relevant to reporting, documentation, or communication style.

Capture the current conversation into a clean markdown report file.

## Steps

1. **Derive the slug** — 2–5 kebab-case words summarizing the topic (e.g. `auth-middleware-refactor`, `team-budget-problem`).

2. **Get the timestamp** — run `date +%Y%m%d-%H%M%S` to get the current timestamp.

3. **Ensure the directory exists** — run `mkdir -p reports` in the current working directory.

4. **Write the report** to `reports/{timestamp}-{slug}.md`.

## Report structure

```markdown
# {Title}

**Date:** {YYYY-MM-DD HH:MM}
**Topic:** {one-line summary}

## Summary

{2–4 sentence overview of what was discussed and what was concluded}

## Discussion

{The key points raised, questions asked, and answers given — written as flowing prose or structured sections, whichever fits the content. Preserve decisions, insights, and important nuances. Not a raw transcript.}

## Conclusions

{What was decided, agreed, or understood by the end}

## Next Steps

{Concrete actions, if any. Omit this section if none were identified.}
```

## Notes

- Write the report from the perspective of a neutral observer summarizing the session.
- Omit filler and meta-commentary ("the user asked…") — write the substance directly.
- If the discussion has multiple distinct topics, use H2 sections under Discussion.
- After writing, tell the user the file path.
