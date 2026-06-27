---
name: to-todo
description: Add or remove tasks in TODO.md — a plain list of human-accepted tasks for the project. Use when user says "add todo", "remove todo", "what are my todos", "to-todo", or invokes /to-todo.
---

# To Todo

Manage the project's accepted task list at `TODO.md`.

Every item in `TODO.md` is human-accepted and ready to execute. No checkboxes — done tasks are removed, not marked.

## Operations

**Add** — user says "add todo: X" or describes a task to accept
**Remove** — user says "remove X" or "delete X" (use this when a task is done or cancelled)
**List** — user says "show todos", "what's left"

## File format

```markdown
# TODO

- Task description
- Another task
```

Plain list only. No checkboxes. No done items — remove them when complete.

## Steps

1. If `TODO.md` doesn't exist, create it with the header `# TODO`.
2. Read the current file.
3. Apply the operation (add / remove).
4. Write the file back.
5. Confirm in one sentence what changed.
