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

1. Read `today.md` to understand what work has happened so far.
2. Read `goals/YYYY/goal-MM-DD.md` (today's goal file).
3. Read the weekly goal `goals/YYYY/goal-MM-WNN.md` for broader context.

---

## Step 2: Understand the adjustment

The user's message should explain what to change. If it's unclear, ask:
- What task(s) are being added, removed, or re-prioritized?
- Why is this adjustment necessary?

Good reasons: a blocker appeared, an urgent request came in, a task turned out to be larger than expected, a dependency was resolved, context changed.

Do not accept vague reasoning like "I just feel like it" — ask the user to be specific. The adjustment log is a record for future reflection.

---

## Step 3: Apply the changes to the goal file

Update `goals/YYYY/goal-MM-DD.md`:

- **Re-prioritize**: move tasks within their topic section (high → medium → low order must be maintained)
- **Add a task**: place it in the correct topic section at the correct priority position; create the topic section if it doesn't exist
- **Remove a task**: delete or mark `*(dropped)*` with a note
- **Change priority**: move the task to the new position within its topic

Topic sections within `## Tasks` are organized by subject (e.g., `### Rust`, `### ML Research`). Within each section, tasks run high → medium → low, top to bottom.

---

## Step 4: Append to the Adjustment Log

Add an entry at the bottom of `## Adjustment Log` in the goal file:

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
