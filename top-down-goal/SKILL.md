---
name: top-down-goal
description: Top-down decomposition of a user goal into sub-goals, then writes a timestamped summary. Use when user describes a feature goal and wants to break it down, mentions "top-down-goal", "break down this feature", "what do I need to implement", or "decompose this goal".
---

# Top-Down Goal

Decompose a high-level goal into sub-goals, grounded in the existing codebase.

Read [archi](../references/archi.md) before starting.

## Step 1: Understand the goal

Restate the goal in one sentence to confirm understanding.

## Step 2: Explore the codebase

Read existing source files and docs relevant to the goal. Map what exists vs. what is missing.

## Step 3: Decompose top-down

Break the goal into sub-goals. At each level ask: "What must be true for this to work?" Keep going until each leaf is concrete and implementable.

```
Goal
├── Sub-goal A
│   ├── Leaf 1
│   └── Leaf 2
└── Sub-goal B
    └── Leaf 3
```

## Step 4: Grill — narrow the decision space

Ask one question at a time. Ask only the high-impact ambiguous ones in order of impact. Skip anything the codebase already answers.

When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)". For open-ended questions, ask in plain text and state your recommendation.

User can say "wrap up" to stop early.

## Step 5: Write the summary

Write to `./{timestamp}_{slug}.md` where:
- `timestamp` = `YYYYMMDD_HHMMSS`
- `slug` = kebab-case of the goal (e.g. `space-input-handler`)

```md
# {Goal}

## Decomposition

{top-down tree}

## Key Decisions

- {decision}: {choice and reason}
```
