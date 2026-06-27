---
name: to-sot
description: Extract the human's intent from the current conversation and write it as a markdown file into the project's source-of-truth/ directory. Use when user says "save intent", "write intent", "capture this", "to-sot", "source of truth", or invokes /to-sot.
---

# To Source of Truth

Capture what the human actually wants — their goals, priorities, constraints, and preferences — and persist it to `source-of-truth/` in the current project root.

## Step 1: Derive the topic

From the current conversation, identify the core topic or concern (e.g. `testing`, `architecture`, `code-style`, `workflow`). This becomes the filename: `source-of-truth/{topic}.md`.

If `source-of-truth/{topic}.md` already exists, read it first — update or extend rather than overwrite.

## Step 2: Extract the intent

Pull out what was actually expressed or strongly implied. Don't invent.

## Step 3: Write the file

`mkdir -p source-of-truth` if the directory doesn't exist. Write freely — no enforced format.

## Step 4: Confirm

Tell the user what was written and where. One sentence.
