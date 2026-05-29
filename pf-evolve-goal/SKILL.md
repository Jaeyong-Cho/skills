---
name: pf-evolve-goal
description: |
  Manage evolutionary development goals — create, read, update, and delete goals in the evolve/ directory. Each goal has a description, input, expected output, and success criteria. Mutations and evaluations are tracked as numbered files inside the goal directory.
  Use when the user wants to define a new goal, review existing goals, update a goal's direction, or remove a goal. Triggers: "pf-evolve-goal", "new goal", "create goal", "set goal", "update goal", "change goal", "list goals", "delete goal", "what are my goals", "evolve goal".
---

# Evolutionary Goal Management

Goals live in `evolve/<id>-<slug>/goal.md`. Mutations and evaluations accumulate as `N_mutation.md` / `N_evaluation.md` in the same directory.

## Create

Goals must be **end-to-end**: a concrete input fed to the real system produces an observable output. Not "improve X internally" — but "given this input, the system should produce this output."

Run `grill-me` skill. Starting context: goal definition. Cover at minimum:
- **Input** — what exactly goes into the system? (file, string, request, stdin — must be concrete and reproducible)
- **Expected output** — what does the system emit? (stdout, file, response body — must be observable and comparable)
- **Why** — what's wrong or missing with the current output?
- **Success criteria** — what does good look like (functional correctness, performance, human taste)?

If the user defines a goal in terms of internal code structure ("refactor", "clean up", "improve coverage") — push back. Ask: what input changes, and how does the output differ?

No maximum questions. User can say **"wrap up"** to move on.

Derive slug from description (lowercase, hyphens, max 30 chars). Assign `id` = count of existing `evolve/` directories + 1 (zero-padded to 2 digits: `01`, `02`, …).

```bash
mkdir -p evolve/<id>-<slug>
```

Write `evolve/<id>-<slug>/goal.md`:

```markdown
# <Goal name>

## Description
<what we're trying to achieve>

## Input
<what goes in>

## Expected output
<what should come out>

## History
- YYYY-MM-DD: created
```

## Read

List all goals and their current state:

```bash
ls evolve/ 2>/dev/null
```

For each goal directory, show:
- slug and status (from `goal.md`)
- mutation count: `ls evolve/<id>-<slug>/*_mutation.md 2>/dev/null | wc -l`
- evaluation count: `ls evolve/<id>-<slug>/*_evaluation.md 2>/dev/null | wc -l`

## Update

User names a goal → read its `goal.md` → run `grill-me` skill with the current goal as context, focused on what changed and why → update the relevant fields → append to History:

```markdown
- YYYY-MM-DD: updated — <reason>
```

## Delete

Ask for confirmation. Two options:
- **Archive** — set status to `abandoned`, append reason to History, keep files
- **Remove** — delete `evolve/<id>-<slug>/` entirely
