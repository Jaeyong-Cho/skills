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

## Step 4: Grill — narrow the decision space

Before asking anything, map the decision space: identify every ambiguous or consequential decision the decomposition revealed. Rank by impact — which ones, if decided wrong, reshape the whole goal tree?

Then ask only the high-impact ambiguous ones in order of importance. Skip anything obvious or already answered by the codebase.

Ask one question at a time. When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)". For open-ended questions, ask in plain text and state your recommendation explicitly.

User can say "wrap up" to stop early.

## Step 5: Write the summary

Write to the current directory `./{timestamp}_{slug}.md` where:
- `timestamp` = `YYYYMMDD_HHMMSS`
- `slug` = kebab-case of the goal (e.g. `space-input-handler`)

Order the decomposition as a logical top-down sequence a reader can follow straight through — from the goal down to leaves, in the order things must be understood or built. Each sub-goal is a section; its leaves are listed under it in implementation order.

```md
# {Goal}

## {Sub-goal A}

- {Leaf 1} — [Objects] create
- {Leaf 2} — [Logics] create

## {Sub-goal B}

- {Leaf 3} — [Usecase] update
- {Leaf 4} — [External] update

## Key Decisions

- {decision}: {choice and reason}
```
