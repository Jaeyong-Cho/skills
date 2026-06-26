---
name: to-todo
description: Add, update, or list todos in source-of-truth/TODO.md — a single persistent todo file for the project. Use when user says "add todo", "mark done", "what are my todos", "to-todo", or invokes /to-todo.
---

# To Todo

Manage the project's single todo file at `source-of-truth/TODO.md`.

## Operations

**Add a todo** — user says "add todo: X" or just describes a task to track
**Mark done** — user says "done: X" or "mark X as done"
**List todos** — user says "show todos", "what's left"
**Remove** — user says "remove X" or "delete X from todos"

## File format

```markdown
# TODO

- [ ] Task description
- [ ] Another task
- [x] Completed task
```

Unchecked `[ ]` = open. Checked `[x]` = done. Keep completed items at the bottom.

## Steps

1. If `source-of-truth/TODO.md` doesn't exist, create it with the header `# TODO`.
2. Read the current file.
3. Apply the operation (add / check / uncheck / remove).
4. Write the file back — open items first, completed items last.
5. Confirm in one sentence what changed.
