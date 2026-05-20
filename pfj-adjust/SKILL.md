---
name: pfj-adjust
description: |
  Mid-day plan adjustment for the POFE knowledge base. Updates today's goal file based on new information, blockers, or changed priorities — and requires explicit reasoning for every change. Use when priorities shift during the day, a task gets blocked, or new urgent work appears.
  Triggers: "adjust today's plan", "update today's goals", "pfj adjust", "change today's priorities", "something came up", "I need to reprioritize", or any request to modify the current day's goal mid-day.
---

# pfj-adjust: Mid-Day Plan Adjustment

**Goal**: Update today's goal file to reflect current reality, with explicit record of what changed and why — so end-of-day review has accurate context.

---

## Step 1: Load current state

1. Read `today.md` in full — `## Goals` section at top is today's goal; journal below shows what has happened so far.
2. Read `goals/YYYY/goal-MM-WNN.md` (weekly goal) for broader context.

---

## Step 2: Derive adjustment from today.md

**Journal is source of truth.** Human's written notes always correct. Goal files are AI inferences that may not match reality. When journal and goal file disagree, correct goal file — never ignore discrepancy.

Reason for adjustment already written in `today.md` — read it to understand what happened and why plan needs to change. Look for:
- Blocker or unexpected problem encountered
- New urgent task that came up
- Task that turned out larger or smaller than expected
- Completed dependency that unblocks something
- Explicit note about needing to reprioritize
- Description of work done that contradicts current goal file

Infer from journal what tasks should be added, removed, or re-prioritized, and what reason is. Do not ask user to re-explain what is already in journal.

---

## Step 3: Apply changes to Goals section

Update `## Goals` section at top of `today.md`:

- **Re-prioritize**: move tasks within their topic section (high → medium → low order must be maintained)
- **Add a task**: place in correct topic section at correct priority position; create topic section if it doesn't exist
- **Remove a task**: delete or mark `*(dropped)*` with note
- **Change priority**: move task to new position within its topic
- **Background tasks**: if newly added or discovered task is long-running and independent (test suite, build, download, training run), mark it `*(bg)*` and add to `> Trigger first` block at top of Goals. If background task finishes, remove it from that block.

Topic sections within `## Goals` organized by subject (e.g., `### Rust`, `### ML Research`). Within each section, tasks run high → medium → low, top to bottom. Background tasks `*(bg)*` appear first within their priority band.

---

## Step 4: Append to Adjustment Log

Add entry at bottom of `## Adjustment Log` in `today.md`:

```markdown
- HH:MM — <what changed> — <why>
```

Example:
```markdown
- 14:23 — moved "refactor parser" from High to Low — blocked by missing upstream API; deprioritized until resolved
- 14:23 — added "investigate API timeout" to Rust/High — urgent: production issue reported
```

Use 24h time. Be specific — this log is record for end-of-day review and future reflection.

---

## Step 5: Confirm with user

Show brief summary of what changed:

```
Updated goals/YYYY/goal-MM-DD.md:
  + Rust / High: "investigate API timeout" (added — urgent prod issue)
  ~ Rust: "refactor parser" High → Low (blocked by upstream API)
```

No need to show full file — just the delta.
