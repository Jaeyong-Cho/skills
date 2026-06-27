---
name: to-sot
description: Extract the human's intent from the current conversation and write it as a structured markdown file into the project's source-of-truth/ directory. Use when user says "save intent", "write intent", "capture this", "to-sot", "source of truth", or invokes /to-sot.
---

# To Source of Truth

Capture what the human actually wants — their goals, priorities, constraints, and preferences — and persist it to `source-of-truth/` so future skills can read it.

## Step 1: Derive the topic

From the current conversation, identify the core topic or concern being expressed (e.g. `testing`, `architecture`, `code-style`, `workflow`). This becomes the filename: `source-of-truth/{topic}.md`.

If an `source-of-truth/{topic}.md` already exists, read it first — update or extend rather than overwrite.

## Step 2: Extract the intent

Pull out:
- **Goal** — what the human is trying to achieve
- **Priorities** — what matters most, what to optimize for
- **Constraints** — hard limits, things to avoid, non-negotiables
- **Preferences** — style, approach, tone preferences that shape how work is done
- **Context** — any background that explains why these source-of-truth exist

Only include things actually expressed or strongly implied in the conversation. Don't invent.

## Step 3: Write the file

Create or update `source-of-truth/{topic}.md` using this structure:

```markdown
# {Topic} Intent

## No format
```

Omit sections that have nothing to say. `mkdir -p source-of-truth` if the directory doesn't exist.

## Step 4: Confirm

Tell the user what was written and where. One sentence.
