---
name: req-write
description: Top-down decomposition of a user goal into MECE requirements, then write to src/req/{category}/{req}.md with suggested API list. Use when user describes a feature goal and wants to break it into requirements, mentions "req-write", "write requirements", "break down this feature", "what do I need to implement".
---

# Req Write (Goal → Requirements)

Decompose a high-level goal top-down into MECE requirements, grounded in the existing codebase and API docs.

## Step 1: Understand the goal

User states a goal (e.g., "handle space key input in Tetris"). Restate it in one sentence to confirm understanding.

## Step 2: Explore the codebase

Before asking anything:
- Read existing source files relevant to the goal
- Read all API docs in `src/api/` (objects, aspects, values)
- Map what already exists vs. what is missing

## Step 3: Decompose top-down

Break the goal into sub-needs using top-down thinking. At each level ask: "What must be true for this to work?" Keep going until each leaf is concrete and implementable.

Example for "space key → block drop":
```
Space input handled
├── Input event detected (space key)
├── Block drops to bottom
│   ├── Collision detected at lowest valid row
│   └── Block position updated to that row
├── Block settled (no longer moving)
│   └── Block state transitions to settled
├── Board evaluated for complete lines
│   ├── Complete lines identified
│   ├── Lines removed and board compacted
│   └── Score updated
└── Next block spawned
```

Each leaf = one requirement. Requirements must be **MECE**: no overlap, no gaps.

## Step 4: Grill — narrow the decision space

Map every ambiguous or consequential decision the decomposition revealed. Rank by impact.

Ask one question at a time. Ask only the high-impact ambiguous ones in order of impact. Skip anything the codebase already answers.

When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)" to its label. For open-ended questions, ask in plain text and state your recommendation explicitly.

User can say "wrap up" to stop early.

## Step 5: Write the requirements

For each leaf requirement, confirm the filename and category with the user, then write to `src/req/<category>/<name>.md` using [REQ_TEMPLATE.md](REQ_TEMPLATE.md).

Add each new file to `src/SUMMARY.md`. Follow this structure (paths relative to `src/`):

```md
# Requirements

## <Category>

- [Requirement Name](req/category/name.md)
```

If the `# Requirements` section or the `##` category doesn't exist yet, create it. Insert new entries in alphabetical order within the category.

## Step 6: Summarize

After writing all requirements, output:
- List of req files written
- Suggested API docs to create or update (grouped by layer: objects / aspects / values)
- Any dependencies between requirements (which must be done first)

## Rules

- Decompose before asking — have the full tree mapped before grilling.
- MECE: each requirement covers exactly one concern. If two reqs overlap, merge them. If there's a gap, add a req.
- "Out of Scope" is required in every req — it's what enforces MECE.
- Do not invent APIs — only reference existing ones or flag new ones as "suggested (new)".
- If an existing API doc is incomplete, wrong, or missing a method the requirement clearly needs, fix it — but only when the change is unambiguously correct given the requirement. Surface the change to the user before writing.
- Req files are for WHAT and WHY, not HOW. Implementation details belong in api-write docs.
