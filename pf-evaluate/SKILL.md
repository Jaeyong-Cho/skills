---
name: pf-evaluate
description: |
  Evaluate a mutation end-to-end using a per-goal CLI eval script, reporting from the whole-goal perspective first, then recording the result as N_evaluation.md. Creates the eval script once per goal; reuses it on every subsequent evaluation.
  Use when the user wants to evaluate a mutation, check if a change works, score a result, or decide whether to keep or discard. Triggers: "pf-evaluate", "evaluate mutation", "evaluate goal", "check the output", "does it work", "score this mutation", "keep or discard".
---

# Evolutionary Evaluation

Evaluation is end-to-end: a single CLI script runs the real system with the goal's input, captures actual output, and compares to expected. No mocks, no internal checks.

## Step 1: Select goal

```bash
ls evolve/ 2>/dev/null
```

Display as a numbered list. Read `evolve/<id>-<slug>/goal.md` — note **Input** and **Expected output**.

## Step 2: Show what changed

```bash
ls evolve/<id>-<slug>/*_mutation.md 2>/dev/null | sort -V | tail -1
```

Read the latest `N_mutation.md`. Confirm `Status: applied — awaiting evaluation`. Show the user the **Change** section — what files, what summary — so it's clear what this evaluation is testing.

## Step 3: Ensure eval runner exists

Check for `evolve/<id>-<slug>/eval.*` (any language — shell, Python, Go, etc.). If missing, create one in whatever language best fits the project:
- Read the codebase to understand how to invoke the system
- Wire the goal's **Input** as the fixed argument(s)
- Capture full stdout/stderr
- Make it executable if needed

The runner is the single canonical way to run this goal's evaluation. It must be deterministic: same input every time.

## Step 4: Run

```bash
evolve/<id>-<slug>/eval.<ext>
```

Capture the full output.

## Step 5: Report — goal perspective first

Lead with the big picture before mutation-level details:

| | |
|---|---|
| **Goal** | `<slug>` — one-line description |
| **Expected output** | `<from goal.md>` |
| **Actual output** | `<from Step 4>` |
| **Functional** | pass / fail — differences noted |

Then state which mutation this belongs to and what it changed.

## Step 6: Ask for taste

Ask via `AskUserQuestion` using the taste question from `N_mutation.md`'s `## How to evaluate`. Wait for verdict.

## Step 7: Record N_evaluation.md

`N` matches the mutation number. Write `evolve/<id>-<slug>/N_evaluation.md`:

```markdown
# Evaluation N — <mutation title>

## Mutation
N_mutation.md

## Actual output
<verbatim output from eval.sh>

## Functional
pass / fail — <notes>

## Performance
<measurement, if applicable>

## Taste
<user's verdict>

## Verdict
kept / discarded

## History
- YYYY-MM-DD: evaluated
```

## Step 8: Update mutation status

Edit `evolve/<id>-<slug>/N_mutation.md` — set `## Status` to `kept` or `discarded`.
