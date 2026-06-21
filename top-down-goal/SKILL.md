---
name: top-down-goal
description: Top-down decomposition of a user goal into sub-needs, then writes a timestamped summary with suggested APIs. Use when user describes a feature goal and wants to break it down, mentions "top-down-goal", "break down this feature", "what do I need to implement", or "decompose this goal".
---

# Top-Down Goal

Decompose a high-level goal into sub-needs, grounded in the existing codebase and API docs.

Read [deep-modules](../references/deep-modules.md) and [archi](../references/archi.md) before starting.

## Step 1: Understand the goal

Restate the goal in one sentence to confirm understanding.

## Step 2: Explore the codebase

Read existing source files and all API docs in `src/api/` relevant to the goal. Map what exists vs. what is missing.

## Step 3: Decompose top-down

Break the goal into sub-needs. At each level ask: "What must be true for this to work?" Keep going until each leaf is concrete and implementable.

```
Goal
├── Sub-need A
│   ├── Leaf 1
│   └── Leaf 2
└── Sub-need B
    └── Leaf 3
```

## Step 4: Grill — narrow the decision space

Ask one question at a time. Ask only the high-impact ambiguous ones in order of impact. Skip anything the codebase already answers.

When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)". For open-ended questions, ask in plain text and state your recommendation.

User can say "wrap up" to stop early.

## Step 5: Write the summary

Write to `~/.claude/skills/top-down-goal/{timestamp}_{slug}.md` where:
- `timestamp` = `YYYYMMDD_HHMMSS`
- `slug` = kebab-case of the goal (e.g. `space-input-handler`)

```md
# {Goal}

## Decomposition

{top-down tree}

## Key Decisions

- {decision}: {choice and reason}

## Suggested APIs

### Existing
- `api/objects/<name>.md` — {why}

### New (to create)
- `api/objects/<name>.md` — {why}
```

## Rules

- Decompose before asking — have the full tree mapped before grilling.
- Do not invent APIs — only reference existing ones or flag new ones as "new".
- If an existing API doc is incomplete or wrong for what the goal clearly needs, fix it — but surface the change to the user first.
