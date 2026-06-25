---
name: small-impl
description: Implement a change in the smallest possible atomic unit. Blocks if the plan is too large and requires it to be broken down first. Use when user invokes /small-impl.
---

# Small Impl

Implement one small, focused change. Large plans are not allowed — they must be broken down before any code is written.

## Step 1: Evaluate scope

Before writing any code, assess whether the change is small enough.

**A change is small if it fits one of these patterns:**
- **One function** — add, modify, or delete a single function (~20–30 lines diff)
- **Uniform change** — the same mechanical edit applied everywhere (rename a variable, update an import, change a constant) — multiple files are fine if the change is identical in nature

**A change is large if ANY of these are true:**
- Modifies multiple functions for different reasons
- Mixes different types of change (e.g. rename + logic fix + refactor)
- Diff exceeds ~30 lines of meaningful change (not counting renames/moves)
- Can only be described with "and" or "also"

## Step 2: Block if large

If the plan is large, **do not write any code**. Instead:

1. State clearly: "This plan is too large to implement as one change."
2. List what makes it large (which of the above rules it violates).
3. Break it into a numbered sequence of small changes, each independently implementable and safe to commit.
4. Ask the user: "Which step should I implement first?"

Do not proceed until the user picks one step.

## Step 3: Implement the small change

Once the scope is confirmed small:
- Implement only that one change. Nothing else, even if you notice nearby improvements.
- Do not refactor surrounding code unless it is the explicit task.
- After implementing, state in one sentence what changed and why it is complete.
