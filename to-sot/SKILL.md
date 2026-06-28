---
name: to-sot
description: Read the full conversation session and extract all truth — facts, human preferences, opinions, decisions, constraints, and anything else the human revealed — then write it to the project's source-of-truth/ directory. Use when user says "save intent", "write intent", "capture this", "to-sot", "source of truth", or invokes /to-sot.
---

# To Source of Truth

Read the entire conversation and extract every truth the human revealed — not just intent, but facts, preferences, opinions, decisions, constraints, and anything else that reflects who they are or what they want.

## Step 1: Derive the topic

Identify the core topic of the conversation (e.g. `testing`, `architecture`, `workflow`, `feeling`). This becomes the filename: `source-of-truth/{topic}.md`.

If `source-of-truth/{topic}.md` already exists, read it first — update or extend rather than overwrite.

## Step 2: Extract all truth

Read the full session and pull out everything the human actually expressed or strongly implied. Categories to look for:

- **Facts** — things stated as true about the world, the project, or the situation
- **Preferences** — what they like, dislike, or find comfortable
- **Opinions** — their judgments and assessments
- **Decisions** — choices they made or committed to
- **Constraints** — what they can't, won't, or don't want to do
- **Goals** — what they're trying to achieve
- **Concerns** — what worries or weighs on them
- **Patterns** — recurring themes across multiple messages

Do not invent. Do not infer beyond what was expressed. If something is ambiguous, omit it.

## Step 3: Write the file

`mkdir -p source-of-truth` if the directory doesn't exist. Write freely — no enforced format. Group by category where it helps readability.

## Step 4: Confirm

Tell the user what was written and where. One sentence.
