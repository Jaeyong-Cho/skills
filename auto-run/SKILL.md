---
name: auto-run
description: Autonomously execute all tasks in TODO.md without asking the human for decisions. Removes each task from TODO.md when done. Only stops to ask when credentials are missing or a requirement is genuinely ambiguous. Use when user says "run tasks", "do the todos", "auto-run", "execute tasks", or invokes /auto-run.
---

# Auto Run

Run `sot search-cmd "project context constraints preferences" --k 5` for relevant context.
Read `TODO.md` in the current project root. Everything in this file is already human-accepted — execute all of it.

## Execution rules

**Act, don't ask.** Make decisions independently. Use `sot search-cmd` and the codebase to resolve ambiguity whenever possible. The human has already approved these tasks — don't re-seek approval.

**Only stop and ask when:**
1. Credentials, secrets, or access are missing and cannot be inferred
2. A requirement is genuinely ambiguous and cannot be resolved from any available context — state exactly what is unclear and what you need

**After completing each task:**
- Remove it from `TODO.md` immediately
- State in one line what was done

**If a task fails:**
- State what failed and why
- Skip it and continue with the next task
- List all failures in the final report

## Steps

1. Read `TODO.md` — if empty or missing, report "No tasks to run."
2. Pick the first task.
3. Execute it fully and autonomously.
4. Remove it from `TODO.md`.
5. Repeat until `TODO.md` is empty.
6. Report: tasks completed, tasks failed (with reasons).
