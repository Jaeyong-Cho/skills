---
name: pf-force
description: |
  Apply an external force — a new insight, detected issue, or better direction — to the goal landscape. Reads existing goals, grills the user to shared understanding, then judges whether to create, update, or delete goals. All changes preserve history.
  Use when the user has a thought, observation, or issue that might reshape one or more goals. Triggers: "pf-force", "apply force", "I noticed something", "new direction", "something better", "rethink goals", "new goal", "create goal", "update goal", "delete goal", "list goals", "what are my goals".
---

# Evolutionary Force

A force is an external pressure that acts on the goal landscape — a new insight, a detected problem, a better approach. It may create a new goal, redirect an existing one, or make one obsolete.

Goals live in `evolve/<id>-<slug>/goal.md`. Mutations and evaluations accumulate as `N_mutation.md` / `N_evaluation.md` in the same directory.

When writing markdown: using Mermaid diagrams is recommended.

## Step 1: Read existing goals

```bash
ls evolve/ 2>/dev/null
```

For each goal show: id-slug, mutation count, evaluation count, last history entry.

## Step 2: Grill the force

Run `grill-me` skill using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: understand what the force is and how it reshapes the goal landscape. Starting context: the user's force — their idea, observation, or issue. Ask one question at a time using `AskUserQuestion`. No maximum questions. User can say **"wrap up"** to move on.

## Step 3: Judge

| Action | When |
|--------|------|
| **Create** | Force reveals a new end-to-end goal not yet tracked |
| **Update** | Force sharpens, redirects, or narrows an existing goal |
| **Delete** | Force makes a goal obsolete or wrong |
| **No change** | Force is context only — goals are already correct |

State the judgment and confirm with the user before acting.

## Step 4: Execute

### Create

Goals must be end-to-end and appropriately scoped:
- Too broad: "make the system better" — no clear convergence
- Too narrow: "fix one line" — not worth an evolutionary loop
- Right: iterable, evaluatable, converges toward a clear output

If the user defines a goal in terms of internal structure ("refactor", "clean up") — push back. Ask: what input changes, and how does the output differ?

Assign `id` = count of existing `evolve/` directories + 1 (zero-padded to 4 digits: `0001`, `0002`, …). Derive slug from description (lowercase, hyphens, max 30 chars).

```bash
mkdir -p evolve/<id>-<slug>
```

Write `evolve/<id>-<slug>/goal.md`:

```markdown
# <Goal name>

## Description
<what we're trying to achieve>

## Input
<concrete, reproducible input>

## Expected output
<what should come out>

## History
- YYYY-MM-DD: created
```

Then create the eval command for this goal under `evolve/<id>-<slug>/eval/`:
- Read the codebase to understand how to invoke the system
- Wire the goal's **Input** as fixed argument(s)
- Capture full stdout/stderr
- Entry point must be a single CLI command (e.g. `./eval/run.sh`, `python eval/main.py`, `go run ./eval`)
- Internal structure (single file or multi-file project) is unconstrained — use whatever fits

The command must be deterministic: same input every time.

### Update

Edit the relevant fields in `goal.md`. Append to History:
```markdown
- YYYY-MM-DD: updated — <force summary>
```

### Delete

Two options:
- **Archive** — append to History and keep files:
```markdown
- YYYY-MM-DD: abandoned — <force summary>
```
- **Remove** — delete `evolve/<id>-<slug>/` entirely (confirm first)
