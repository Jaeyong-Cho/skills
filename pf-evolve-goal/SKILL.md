---
name: pf-evolve-goal
description: |
  Manage evolutionary development goals — create, read, update, and delete goals in the evolve/ directory. Each goal has a description, input, expected output, and success criteria. Mutations and evaluations are tracked as numbered files inside the goal directory.
  Use when the user wants to define a new goal, review existing goals, update a goal's direction, or remove a goal. Triggers: "pf-evolve-goal", "new goal", "create goal", "set goal", "update goal", "change goal", "list goals", "delete goal", "what are my goals", "evolve goal".
---

# Evolutionary Goal Management

Goals live in `evolve/<slug>/goal.md`. Mutations and evaluations accumulate as `mutation_N.md` / `evaluation_N.md` in the same directory.

## Create

Run `grill-me` skill. Starting context: goal definition. Cover at minimum:
- **Description** — what are we trying to achieve?
- **Input** — what goes in?
- **Expected output** — what should come out?
- **Success criteria** — what does good look like at each layer (functional → performance → human taste)?

No maximum questions — keep going until the goal is unambiguous. User can say **"wrap up"** to move on.

Derive slug from description (lowercase, hyphens, max 30 chars).

```bash
mkdir -p evolve/<slug>
```

Write `evolve/<slug>/goal.md`:

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
- mutation count: `ls evolve/<slug>/mutation_*.md 2>/dev/null | wc -l`
- evaluation count: `ls evolve/<slug>/evaluation_*.md 2>/dev/null | wc -l`

## Update

User names a goal → read its `goal.md` → run `grill-me` skill with the current goal as context, focused on what changed and why → update the relevant fields → append to History:

```markdown
- YYYY-MM-DD: updated — <reason>
```

## Delete

Ask for confirmation. Two options:
- **Archive** — set status to `abandoned`, append reason to History, keep files
- **Remove** — delete `evolve/<slug>/` entirely
