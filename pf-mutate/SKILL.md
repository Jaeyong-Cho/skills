---
name: pf-mutate
description: |
  Propose and apply a focused mutation to evolve code toward a goal, driven by a user-supplied reason (evaluation result, goal shift, new insight). Grills the user on the intent before forming a hypothesis, then applies the change and records it as N_mutation.md.
  Use when the user wants to take a step toward an evolutionary goal, act on an evaluation result, or change direction. Triggers: "pf-mutate", "mutate toward goal", "next mutation", "try a variant", "evolve the code", "take a step toward the goal", "apply evaluation result".
---

# Evolutionary Mutation

One mutation = one focused change toward a goal — hill-climbing, one candidate at a time. Scope is **mutate only** — propose, apply, record. Scoring the result (functional → performance) is the evaluation step's job.

When writing markdown: using Mermaid diagrams is recommended.

For VAO layer definitions read `../pf/references/layers.md`, `../pf/references/deep-modules.md`, `../pf/references/views.md`.

## Step 1: Select goal

```bash
ls evolve/ 2>/dev/null
```

Display as a numbered list so the user can reference by number or slug. If the user already named one, confirm it. Read `evolve/<id>-<slug>/goal.md`.

## Step 2: Read relevant history

```bash
ls evolve/<id>-<slug>/*_mutation.md evolve/<id>-<slug>/*_evaluation.md 2>/dev/null | sort -V
```

Start from the latest pair (most recent `N_mutation.md` + its `evaluation_N.md`). Read more only if needed — e.g., user references a past attempt or the latest state is ambiguous. **Do not read the full history by default.**

## Step 3: Read the codebase

Read the source files relevant to the goal. Use the goal's description and input/output to locate the right entry points — just enough to have a concrete mental model before asking questions.

## Step 4: Grill the intent

Run `grill-me` skill. Purpose: understand the intent behind the mutation and what the change should achieve. Starting context: the user's reason for mutating (evaluation result, shifted goal, new insight). No maximum questions. User can say **"wrap up"** to move on.

## Step 5: Propose the mutation

Form a hypothesis. State:
- **Change** — what is being changed
- **Why** — why this should move toward the goal
- **Expected effect + how to measure** per tier:
  - functional — what must still hold / expected output
  - performance — what to measure

Show this, then ask via `AskUserQuestion`: **"Apply this mutation?"** — allow redirect. Do not edit until confirmed.

## Step 6: Apply

Extract behaviors from the hypothesis — each discrete change that needs code:

```
1. <behavior>  [value/aspect/object]
2. ...
```

Implement one behavior at a time:
```
RED:   Write test via public interface → confirm fails
GREEN: Write minimal code → confirm passes
```
Do not write the next test until current is green.

Read `../pf-impl/references/tdd-tests.md` for test examples, `../pf-impl/references/tdd-mocking.md` for mocking.

## Step 7: Refactor

Read `../pf-impl/references/tdd-refactoring.md`. Run all tests after each refactor step. Never refactor while RED.

- [ ] Interface narrowable?
- [ ] Complexity hidden or exposed?
- [ ] Duplication to extract?

**Observability** (see `../pf-observe/REFERENCE.md`):
- [ ] Logs key inputs, outputs, and state changes?
- [ ] Errors include enough context to diagnose without a debugger?
- [ ] Existing `observe/` scripts still compatible with changed paths/interfaces?

## Step 8: Record N_mutation.md

`N` = count of existing `*_mutation.md` + 1. Write `evolve/<id>-<slug>/N_mutation.md`:

```markdown
# Mutation N — <short title>

## Goal
<id>-<slug> — <one-line restatement>

## Hypothesis
<the change and why it should move toward the goal>

## Change
- files: <list>
- summary: <what changed, one paragraph>

## How to evaluate
- functional: <what must still hold / expected output>
- performance: <what to measure, which script/benchmark>

## Status
applied — awaiting evaluation

## History
- YYYY-MM-DD: applied
```

## Step 9: Hand off

Report the path to `N_mutation.md` and the next step: **evaluate** (functional → performance).
