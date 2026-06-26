---
name: small-impl
description: Implement a change in the smallest possible atomic unit. Blocks if the plan is too large and requires it to be broken down first. Use when user invokes /small-impl.
---

# Small Impl

If `source-of-truth/` exists in the project root, read files relevant to implementation style, workflow, or coding constraints.

Implement one small, focused change. Large plans are not allowed — they must be broken down before any code is written.

## Step 1: Evaluate scope

Before writing any code, assess whether the change is small enough.

**A change is small if ALL of these are true:**
- Single concern — one reason to change, one thing being done
- Describable in one sentence without "and"
- Touches one logical unit (one function, one module, one config)
- Does not mix concerns: no refactor + feature, no interface + implementation change in one shot
- Reviewable diff — a human can understand it in under 2 minutes

**A change is large if ANY of these are true:**
- Requires changes across multiple unrelated files
- Mixes refactoring with new behavior
- Changes both a contract (interface/API/schema) and its callers in one go
- Can only be described with "and" or "also"
- Would produce a diff that takes more than 2 minutes to review

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
