---
name: to-tdgoal
description: Translate a proto prototype into a tdgoal ADR — reads the implemented source, observe reports, and output, then writes a top-down architectural decomposition grounded in what the prototype actually proved. Use when user wants to graduate a prototype into a design, says "to-tdgoal", "make a tdgoal from this proto", "turn proto into design", or "write ADR from prototype".
---

# To-TDGoal

Elevate a throwaway prototype into a proper architectural design. Grounded in empirical findings, not hypotheses.

Read [archi](../references/archi.md) and [deep-modules](../references/deep-modules.md) before starting.

## Inputs

Read all of these before writing anything:

1. Source files in `proto/<slug>/` — what was implemented and how
2. `proto/<slug>/observe/*.md` — what was observed, what worked, what was surprising
3. `proto/<slug>/output/` — any data produced (if relevant)
4. `proto/<slug>/run.sh` — what use cases were exercised

## Workflow

1. **Restate the goal** — one sentence: what production problem does this prototype answer?
2. **Extract findings** — from observe reports: what did the prototype prove or rule out?
3. **Decompose top-down** — break the production goal into sub-goals, assigned to layers (Objects / Logics / Usecase / External), grounded in what the prototype showed actually works
4. **Grill** — before writing, map the decision space: identify every ambiguous or consequential decision the decomposition revealed. Rank by impact — which ones, if decided wrong, reshape the whole goal tree? Ask only the high-impact ambiguous ones in order of importance. Skip anything obvious or already answered by the prototype. Ask one question at a time. Use `AskUserQuestion` for discrete options (recommended first). User can say "wrap up" to move on.
5. **Write the ADR** — same format as tdgoal (see below)

## ADR output

Write to `docs/src/adr/<timestamp>_<slug>.md`. Add entry to `docs/src/SUMMARY.md` under `# ADR`.

```md
# {Goal}

## Proto findings
- What the prototype proved: {key finding}
- What was ruled out: {if any}
- Approach carried forward: {what from the prototype source shapes the design}

## Scenario: {name}

Given {precondition}. When {trigger}. Then {expected outcome}.

### External
### Usecase
### Logics
### Objects

## Key Decisions

- {decision}: {choice and reason — cite the proto finding that drove it}
```

## Rules

- Every Key Decision must cite a proto finding
- If the prototype didn't test something, flag it as an open question, not a decision
- Follow the dependency rule: inner layers never depend on outer
