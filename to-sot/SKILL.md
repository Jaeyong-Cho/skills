---
name: to-sot
description: Extract the human's intent from the current conversation and write it as a structured markdown file into the project's ~/.sot/wiki/ directory. Use when user says "save intent", "write intent", "capture this", "to-sot", "source of truth", or invokes /to-sot.
---

# To Source of Truth

Capture what the human actually wants — their goals, priorities, constraints, and preferences — and persist it to `~/.sot/wiki/` so it becomes searchable via `sot search-cmd`.

## Step 1: Derive the topic

From the current conversation, identify the core topic or concern being expressed (e.g. `testing`, `architecture`, `code-style`, `workflow`). This becomes the filename: `~/.sot/wiki/{topic}.md`.

Run `sot search-cmd "<topic>" --k 3` first — if relevant chunks exist, update or extend rather than overwrite.

## Step 2: Extract the intent

Pull out:
- **Goal** — what the human is trying to achieve
- **Priorities** — what matters most, what to optimize for
- **Constraints** — hard limits, things to avoid, non-negotiables
- **Preferences** — style, approach, tone preferences that shape how work is done
- **Context** — any background that explains why these source-of-truth exist

Only include things actually expressed or strongly implied in the conversation. Don't invent.

## Step 3: Write the file

Create or update `~/.sot/wiki/{topic}.md` using this structure:

```markdown
# {Topic} Intent

## No format
```

Omit sections that have nothing to say. `mkdir -p ~/.sot/wiki` if the directory doesn't exist.

## Step 4: Re-index

Run `sot index ~/.sot` so the new content becomes searchable.

## Step 5: Confirm

Tell the user what was written and where. One sentence.
