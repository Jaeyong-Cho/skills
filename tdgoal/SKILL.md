---
name: tdgoal
description: Top-down decomposition of a user goal into sub-goals, grounded in architecture layers, then writes a timestamped summary. Use when user describes a feature goal and wants to break it down, mentions "tdgoal", "break down this feature", "what do I need to implement", or "decompose this goal".
---

# TDGoal (Top-Down Goal)

Decompose a high-level goal into sub-goals, grounded in the existing codebase and architecture layers.

Read [deep-modules](../references/deep-modules.md) and [archi](../references/archi.md) before starting.

## Step 1: Understand the goal

Restate the goal in one sentence to confirm understanding.

## Step 2: Explore the codebase

Read existing source files and docs relevant to the goal. Map what exists vs. what is missing.

## Step 3: Decompose top-down

Break the goal into sub-goals. At each level ask: "What must be true for this to work?" Keep going until each leaf is concrete and implementable.

Assign each leaf to a layer from [archi](../references/archi.md) (Objects / Logics / Usecase / External) and an operation (create / update / remove). Flag any leaf that would violate the dependency rule (inner depending on outer) as a design error before continuing.

```
Goal
├── Sub-goal A                [Usecase]   create
│   ├── Leaf 1               [Objects]   update
│   └── Leaf 2               [Logics]    create
└── Sub-goal B               [External]  update
    └── Leaf 3               [Usecase]   remove
```

## Step 4: Grill — depth-first

Ask questions depth-first through the decomposition tree: fully resolve one sub-goal and its leaves before moving to the next sibling. Within each sub-goal, go one level deeper before moving sideways.

Before asking at each node, identify the most consequential ambiguity at that node. Ask only if the answer genuinely changes the shape of that branch. Skip what is obvious or derivable from the codebase.

Ask one question at a time. When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)". For open-ended questions, ask in plain text and state your recommendation explicitly.

User can say "wrap up" to stop early.

## Step 5: Write the ADR

Write to `docs/src/adr/{timestamp}_{slug}.md` where:
- `timestamp` = `YYYYMMDD_HHMMSS`
- `slug` = kebab-case of the goal (e.g. `space-input-handler`)

Add the entry to `docs/src/SUMMARY.md` under an `# ADR` section (create it if absent), in chronological order:

```md
# ADR

- [ADR](adr.md)
  - [{Goal}](adr/{timestamp}_{slug}.md)
```

If `docs/src/adr.md` doesn't exist, create it as a one-line index page.

Write one single concrete execution path as the scenario — the most representative path through the system for this goal. Trace it from External down through Usecase → Logics → Objects.

```md
# {Goal}

## Scenario

Given {precondition}. When {trigger}. Then {expected outcome}.

### External
- {trigger} — [External] create/update/remove — {what arrives and from where}

### Usecase
- {usecase name} — [Usecase] create/update/remove — {what user goal this fulfills}
  1. call {LogicA} — {why}
  2. call {LogicB} — {why}

### Logics
- {LogicA} — [Logics] create/update/remove — {what it computes or enforces}
  - uses {ObjectX}, {ObjectY}
- {LogicB} — [Logics] create/update/remove — {one sentence}
  - uses {ObjectZ}

### Objects
- {ObjectX} — [Objects] create/update/remove — {what state changes}
- {ObjectY} — [Objects] create/update/remove — {one sentence}

## Key Decisions

- {decision}: {choice and reason}
```
