---
name: to-todo
description: Manage .sot/TODO.md — a global checklist of checkbox items with inline sub-header descriptions. Use when the user says "add a todo", "add to my todo list", "check off", "mark done", "mark complete", "remove a todo", "delete a todo", "show my todos", "what's on my todo list", or when a task worth tracking surfaces during other work.
---

# To Todo

Manage `.sot/TODO.md` — one global checklist for the project.

Format: each task is a checkbox line, followed by an indented `####` sub-header repeating the same title, followed by its description.

```markdown
# TODO

- [ ] Task title
  #### Task title
  Description — context, acceptance criteria, or notes.
```

Title text must be identical between the checkbox and its `####` line — that's how they're paired. Titles must be unique in the file; if a new task's title collides with an existing one, ask the user to disambiguate rather than duplicating it.

## Add
1. Read `.sot/TODO.md` (create it with just a `# TODO` header if missing — `mkdir -p .sot` first).
2. Append a blank line, then the checkbox line, `####` line, and description, matching the format above.

## Check / Uncheck
Flip `- [ ]` to `- [x]` (or back) for the matching title. Leave the description in place — completed tasks keep their context.

## Remove
Delete the entire block (checkbox line, `####` line, description, and surrounding blank line) for the matching title.

## List
Read `.sot/TODO.md` and report the checklist titles and their checked state. If the file doesn't exist, say the todo list is empty.

Completion criterion: every checkbox line has exactly one matching `####` sub-header directly beneath it — no orphaned checkboxes, headers, or duplicate titles.
