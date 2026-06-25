---
name: to-intent
description: Extract the human's intent from the current conversation and write it as a structured markdown file into the project's intents/ directory. Use when user says "save intent", "write intent", "capture this as intent", "to-intent", or invokes /to-intent.
---

# To Intent

Capture what the human actually wants — their goals, priorities, constraints, and preferences — and persist it to `intents/` so future skills can read it.

## Step 1: Derive the topic

From the current conversation, identify the core topic or concern being expressed (e.g. `testing`, `architecture`, `code-style`, `workflow`). This becomes the filename: `intents/{topic}.md`.

If an `intents/{topic}.md` already exists, read it first — update or extend rather than overwrite.

## Step 2: Extract the intent

Pull out:
- **Goal** — what the human is trying to achieve
- **Priorities** — what matters most, what to optimize for
- **Constraints** — hard limits, things to avoid, non-negotiables
- **Preferences** — style, approach, tone preferences that shape how work is done
- **Context** — any background that explains why these intents exist

Only include things actually expressed or strongly implied in the conversation. Don't invent.

## Step 3: Write the file

Create or update `intents/{topic}.md` using this structure:

```markdown
# {Topic} Intent

## No format
```

Omit sections that have nothing to say. `mkdir -p intents` if the directory doesn't exist.

## Step 4: Confirm

Tell the user what was written and where. One sentence.
