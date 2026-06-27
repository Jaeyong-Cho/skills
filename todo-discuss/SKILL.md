---
name: todo-discuss
description: Discuss what to do next, decompose complex tasks, and structure todos — then optionally write the result back to source-of-truth/TODO.md. Use when user says "what should I do next", "help me plan", "decompose this task", "todo-discuss", "how do I break this down", or invokes /todo-discuss.
---

# Todo Discuss

If `source-of-truth/` exists in the project root, read all files in it first — especially `TODO.md`.

Help the user figure out what to do next and how to break it down into actionable todos.

## What this covers

- **Prioritization** — what to tackle next given the current state
- **Decomposition** — breaking a large task into concrete, small steps
- **Structure** — organizing todos into a logical order with dependencies clear

## How to run it

Ask one question at a time. Drive toward clarity on three things:

**1. What's the goal?**
- "What are you trying to accomplish?"
- If `TODO.md` exists, read it and ask: "Which of these is most important right now? What's blocking progress?"

**2. What's blocking or unclear?**
- "What's the hardest part to figure out?"
- "Is anything blocked on something else?"
- Surface dependencies — if B can't start until A is done, make that explicit.

**3. How to decompose?**
- For any task that's vague or large, ask: "What's the first concrete action?"
- Keep decomposing until each step is small enough to complete in one sitting.
- Each final step should be: specific, actionable, and independently completable.

## Output

When the discussion reaches clarity, offer to write the structured todos back to `source-of-truth/TODO.md` via `/to-todo`.

Present the proposed todo list first — let the user confirm before writing.
