---
name: pf-scenario
description: |
  Set up and run an end-to-end scenario against the real system — prepares all inputs (config, CLI args, env vars, files) and executes the project's functionality. Saves scenarios as reusable runners under scenarios/.
  Use when the user wants to run a specific scenario, test a feature end-to-end, verify behavior with specific inputs, or create a reusable scenario runner. Triggers: "pf-scenario", "run scenario", "run this end-to-end", "set up and run", "test this scenario", "run with this input".
---

# Scenario Runner

A scenario = a named, reproducible setup + execution of the real system. Not tied to evolutionary goals — any input combination, any feature, any configuration.

## Step 1: Grill the scenario

Run `grill-me` skill. Cover at minimum:
- **What to run** — which feature or entry point of the system?
- **Input** — CLI args, config files, env vars, stdin, request body — what does it need to run?
- **Expected behavior** — what should happen? (output, side effects, state change)
- **Purpose** — exploration, verification, regression check, or demo?

No maximum questions. User can say **"wrap up"** to move on.

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

## History
- YYYY-MM-DD: created
```

Create `scenarios/<slug>/run/` — the single CLI entry point:
- Wire all inputs from `scenario.md` as fixed arguments
- Capture full stdout/stderr
- Language and internal structure: unconstrained
- Entry point must be one invocable command

## Step 4: Run

```bash
<entry point from scenarios/<slug>/run/>
```

## Step 5: Report

Show:
- **Command run**
- **Full output** (stdout + stderr)
- **Behavior vs expected** — match, partial match, or unexpected
- **Anything notable** — errors, timing, side effects
