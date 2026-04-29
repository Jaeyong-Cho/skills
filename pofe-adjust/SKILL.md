---
name: pofe-adjust
description: |
  Mid-day plan adjustment for the POFE knowledge base. Updates today's goal file based on new information, blockers, or changed priorities — and requires explicit reasoning for every change. Use when priorities shift during the day, a task gets blocked, or new urgent work appears.
  Triggers: "adjust today's plan", "update today's goals", "pofe adjust", "change today's priorities", "something came up", "I need to reprioritize", or any request to modify the current day's goal mid-day.
---

# pofe-adjust: Mid-Day Plan Adjustment

**Goal**: Update today's goal file to reflect the current reality, with an explicit record of what changed and why — so the end-of-day review has accurate context.

---

## Step 1: Load current state

1. Read `today.md` in full — the `## Goals` section at the top is today's goal; the journal below shows what has happened so far.
2. Read `goals/YYYY/goal-MM-WNN.md` (weekly goal) for broader context.

---

## Step 2: Derive the adjustment from today.md

**The journal is the source of truth.** The human's written notes are always correct. The goal files are AI inferences that may not match reality. When the journal and a goal file disagree, correct the goal file — never ignore the discrepancy.

The reason for the adjustment is already written in `today.md` — read it to understand what happened and why the plan needs to change. Look for:
- A blocker or unexpected problem encountered
- A new urgent task that came up
- A task that turned out larger or smaller than expected
- A completed dependency that unblocks something
- Any explicit note about needing to reprioritize
- Any description of work done that contradicts the current goal file

Infer from the journal what tasks should be added, removed, or re-prioritized, and what the reason is. Do not ask the user to re-explain what is already in the journal.

---

## Step 3: Apply the changes to the Goals section

Update the `## Goals` section at the top of `today.md`:

- **Re-prioritize**: move tasks within their topic section (high → medium → low order must be maintained)
- **Add a task**: place it in the correct topic section at the correct priority position; create the topic section if it doesn't exist
- **Remove a task**: delete or mark `*(dropped)*` with a note
- **Change priority**: move the task to the new position within its topic
- **Background tasks**: if a newly added or discovered task is long-running and independent (test suite, build, download, training run), mark it `*(bg)*` and add it to the `> Trigger first` block at the top of Goals. If a background task finishes, remove it from that block.

Topic sections within `## Goals` are organized by subject (e.g., `### Rust`, `### ML Research`). Within each section, tasks run high → medium → low, top to bottom. Background tasks `*(bg)*` appear first within their priority band.

---

## Step 4: Append to the Adjustment Log

Add an entry at the bottom of `## Adjustment Log` in `today.md`:

```markdown
- HH:MM — <what changed> — <why>
```

Example:
```markdown
- 14:23 — moved "refactor parser" from High to Low — blocked by missing upstream API; deprioritized until resolved
- 14:23 — added "investigate API timeout" to Rust/High — urgent: production issue reported
```

Use 24h time. Be specific — this log is the record for the end-of-day review and future reflection.

---

## Step 5: Confirm with the user

Show a brief summary of what changed:

```
Updated goals/YYYY/goal-MM-DD.md:
  + Rust / High: "investigate API timeout" (added — urgent prod issue)
  ~ Rust: "refactor parser" High → Low (blocked by upstream API)
```

No need to show the full file — just the delta.
