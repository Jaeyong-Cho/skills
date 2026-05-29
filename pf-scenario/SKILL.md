---
name: pf-scenario
description: |
  Set up an end-to-end scenario against the real system — grills the user, prepares all inputs (config, CLI args, env vars, files), and creates a reusable runner under scenarios/. Does not run it.
  Use when the user wants to set up a scenario, prepare inputs for a feature, or create a reusable scenario runner. Triggers: "pf-scenario", "set up scenario", "create scenario", "prepare this scenario", "scenario for this feature".
---

# Scenario Setup

A scenario = a named, reproducible setup for the real system. Not tied to evolutionary goals — any input combination, any feature, any configuration. Running is left to the user.

## Step 1: Grill the scenario

Run `grill-me` skill. Purpose: understand what to run, what inputs it needs, and what behavior to expect. No maximum questions. User can say **"wrap up"** to move on.

## Step 2: Check existing scenarios

```bash
ls scenarios/ 2>/dev/null
```

If a matching scenario exists, offer to reuse or update it. Otherwise create new.

## Step 3: Create the scenario runner

Assign slug from the scenario name (lowercase, hyphens, max 30 chars).

```bash
mkdir -p scenarios/<slug>/run
```

Write `scenarios/<slug>/scenario.md`:

```markdown
# <Scenario name>

## What it runs
<feature or entry point>

## Input
<all inputs: CLI args, config, env vars, files — concrete and reproducible>

## Expected behavior
<what should happen>

## How to run
<the single CLI command to invoke>

## History
- YYYY-MM-DD: created
```

Create `scenarios/<slug>/run/` — the single CLI entry point:
- Accepts inputs as parameters (args, env vars, or config file) — not hardcoded
- Language and internal structure: unconstrained
- Entry point must be one invocable command

`scenario.md` documents the specific inputs to use; the runner itself stays general.

## Step 4: Verify

Run the entry point once. Confirm it invokes without crashing — correct output is not the goal here, just that the runner works. If it errors, fix the runner before handing off.

Hand off: tell the user the command to run.
