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

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: understand the intent behind the mutation and what the change should achieve. Starting context: the user's reason for mutating (evaluation result, shifted goal, new insight).

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

## Step 5: Update goal and eval if needed

If the grill revealed that the goal's scope, expected output, or input has shifted — update `evolve/<id>-<slug>/goal.md` and append to its History before proceeding. If the eval script no longer reflects the updated input or expected output — update it too. Confirm changes with the user before proceeding.

If nothing changed, skip.

## Step 6: Propose the mutation

Form a hypothesis. State:
- **Change** — what is being changed
- **Why** — why this should move toward the goal
- **Expected effect + how to measure** per tier:
  - functional — what must still hold / expected output
  - performance — what to measure

Show this, then ask via `AskUserQuestion`: **"Apply this mutation?"** — allow redirect. Do not edit until confirmed.

## Step 7: Apply

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

## Step 8: Refactor

Read `../pf-impl/references/tdd-refactoring.md`. Run all tests after each refactor step. Never refactor while RED.

- [ ] Interface narrowable?
- [ ] Complexity hidden or exposed?
- [ ] Duplication to extract?

**Observability** (see `../pf-observe/REFERENCE.md`):
- [ ] Logs key inputs, outputs, and state changes?
- [ ] Errors include enough context to diagnose without a debugger?
- [ ] Existing `observe/` scripts still compatible with changed paths/interfaces?

## Step 9: Record N_mutation.md

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

## Step 10: Hand off

Report the path to `N_mutation.md` and the next step: **evaluate** (functional → performance).
