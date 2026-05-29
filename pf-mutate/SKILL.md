---
name: pf-mutate
description: |
  Propose and apply a focused mutation to evolve code toward a goal, driven by a user-supplied reason (evaluation result, goal shift, new insight). Grills the user on the intent before forming a hypothesis, then applies the change and records it as mutation_N.md.
  Use when the user wants to take a step toward an evolutionary goal, act on an evaluation result, or change direction. Triggers: "pf-mutate", "mutate toward goal", "next mutation", "try a variant", "evolve the code", "take a step toward the goal", "apply evaluation result".
---

# Evolutionary Mutation

One mutation = one focused change toward a goal — hill-climbing, one candidate at a time. Scope is **mutate only** — propose, apply, record. Scoring the result (functional → performance → taste) is the evaluation step's job.

For VAO layer definitions read `../pf/references/layers.md`.

## Step 1: Select goal

```bash
ls evolve/ 2>/dev/null
```

Display as a numbered list so the user can reference by number or slug. If the user already named one, confirm it. Read `evolve/<slug>/goal.md`.

## Step 2: Read relevant history

```bash
ls evolve/<slug>/mutation_*.md evolve/<slug>/evaluation_*.md 2>/dev/null | sort -V
```

Start from the latest pair (most recent `mutation_N.md` + its `evaluation_N.md`). Read more only if needed — e.g., user references a past attempt or the latest state is ambiguous. **Do not read the full history by default.**

## Step 3: Read the codebase

Read the source files relevant to the goal. Use the goal's description and input/output to locate the right entry points — just enough to have a concrete mental model before asking questions.

## Step 4: Grill the intent

Run `grill-me` skill. Starting context: the user's reason for mutating (evaluation result, shifted goal, new insight) — if no reason was given, open with that. Cover at minimum:
- **Why now** — what triggered this mutation request?
- **What must change** — which behavior, structure, or property is wrong or suboptimal?
- **Constraints** — what must not regress?

No maximum questions. User can say **"wrap up"** to move on.

## Step 5: Propose the mutation

Form a hypothesis. State:
- **Change** — what is being changed
- **Why** — why this should move toward the goal
- **Expected effect + how to measure** per tier:
  - functional — what must still hold / expected output
  - performance — what to measure
  - taste — the subjective question for the human

Show this, then ask via `AskUserQuestion`: **"Apply this mutation?"** — allow redirect. Do not edit until confirmed.

## Step 6: Apply

Make the real edits — minimal, only what the hypothesis requires. If behavior is added or altered, run `pf-impl`'s RED→GREEN for just that behavior; otherwise edit directly. Sanity-check that it builds/parses.

## Step 7: Record mutation_N.md

`N` = count of existing `mutation_*.md` + 1. Write `evolve/<slug>/mutation_N.md`:

```markdown
# Mutation N — <short title>

## Goal
<slug> — <one-line restatement>

## Hypothesis
<the change and why it should move toward the goal>

## Change
- files: <list>
- summary: <what changed, one paragraph>

## How to evaluate
- functional: <what must still hold / expected output>
- performance: <what to measure, which script/benchmark>
- taste: <subjective question for the human>

## Status
applied — awaiting evaluation

## History
- YYYY-MM-DD: applied
```

## Step 8: Hand off

Report the path to `mutation_N.md` and the next step: **evaluate** (functional → performance → taste).
