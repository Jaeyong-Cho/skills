---
name: observe
description: Run a proto prototype, analyze what it produced, and write a short analytical report to proto/<slug>/observe/<timestamp>-<slug>.md. Reads the source to understand intent, runs a use case, picks meaningful output excerpts, and synthesizes findings. Use when user wants to observe, analyze, or report on a prototype, or says "observe", "run and observe", "analyze this proto".
---

# Observe

Run a prototype from `proto/<slug>/` and write an analytical report. Not a raw log — a synthesis.

## Workflow

1. **Read** the prototype source files in `proto/<slug>/` — understand what was implemented and why
2. **Read** `proto/<slug>/run.sh` — identify available use cases
3. **Run** the target use case via Bash: `bash proto/<slug>/run.sh N`
4. **Collect** whatever was produced — stdout, files in `output/`, responses
5. **Write** the report to `proto/<slug>/observe/<timestamp>-<slug>.md`

## Report format

```md
# <slug> — <use case description>

**date**: <YYYY-MM-DD HH:MM:SS>

## What was implemented
<1-3 sentences: what the prototype does, what approach was taken — derived from reading the source>

## Output
<relevant excerpt or summary — pick the parts that explain the finding, skip noise>

## Observations
- <what's interesting, surprising, or confirmed>
- <what worked / what didn't>
- <anything worth exploring next>
```

## Rules

- Read the source before running — "What was implemented" must reflect intent, not just output
- Never dump full stdout; summarize or excerpt
- Output files in `output/` count as output — reference or quote them as needed
- Timestamp format: `YYYYMMDD-HHMMSS`
