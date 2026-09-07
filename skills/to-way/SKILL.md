---
name: to-way
description: Record a complete Wayfinder plan tree as ordered Markdown group files with numbered paths. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Turn one complete Wayfinder plan tree into reusable Markdown group files. Preserve the tree, its recommended order, uncertainty notes, and concise execution stages. Do not redesign, deepen, rank, or execute the plan.

## Numbered layout

The tree order is the recommended work order. File numbers preserve that order:

- the root is `0-goal.md`;
- a child at depth `D`, in sibling position `N`, is `{D}-{N}-{slug}.md`;
- each node's child files live in a directory named after that node's ID;
- use the source tree's order, not alphabetical order;
- keep the numeric prefix short as shown (`1-1`, `1-2`, `2-1`).

Example:

```text
ways/01-build-tetris/
├── 0-goal.md
└── 0-goal/
    ├── 1-1-setup-project-build.md
    ├── 1-2-tui.md
    ├── 1-3-main-menu.md
    ├── 1-4-tetris-game.md
    ├── 1-5-settings.md
    └── 1-4/
        ├── 2-1-tetrimino-shape.md
        ├── 2-2-tetrimino-rotate.md
        ├── 2-3-tetrimino-drop-logic.md
        ├── 2-4-clear-line-logic.md
        └── 2-5-score-logic.md
```

If `2-5-score-logic` is atomic, its children continue at the next depth:

```text
ways/01-build-tetris/0-goal/1-4/2-5/
├── 3-1-experiment-score-algorithm.md
├── 3-2-define-requirements.md
├── 3-3-design-architecture.md
├── 3-4-implement.md
└── 3-5-test.md
```

This directory structure allows every parent to use `2-1`, `2-2`, and so on without filename collisions.

## Workflow

1. **Gather the tree.** Use the complete Wayfinder result from this session or a supplied source. Preserve the goal, node titles, node IDs, order, conditions, uncertainty status, and concise stage names. If no tree is available, stop and ask for one; do not invent it.
2. **Confirm the destination.** If this session has not confirmed a destination, ask one `❓` / `➡️` question using `../references/question-format.md`. Recommend `./ways/` in the current directory. Once confirmed, create `./ways/{nn}-{slug}/`; update an existing same-goal directory instead of creating a duplicate.
3. **Validate the tree.** Confirm that:
   - one root is present and it is the goal;
   - every node has one parent and a unique ID;
   - sibling order is explicit and preserved;
   - every non-atomic node contains domain work packages, not generic lifecycle detail;
   - every atomic node contains the applicable experiment, requirements, design, implementation, and test stages;
   - blockers and conditions are retained;
   - every node has exactly one output file at the correct numbered path.
4. **Write the groups.** Write one Markdown file per node. The parent file lists its direct children in recommended order with their numbered relative paths. A leaf file contains only its node and any uncertainty or completion note.
5. **Report paths.** Tell the user the output directory and every group file path.

Do not generate JSON, production code, tests, design documents, or downstream skill handoffs. Do not change the tree while recording it. If the tree is incomplete, preserve the blocker rather than filling it from assumptions.

## Group file format

Write each node to its numbered path under `./ways/{nn}-{slug}/`:

```markdown
---
type: Way Group
title: <node title>
description: <one-line explanation>
tags: [wayfinder, plan-tree]
timestamp: <ISO 8601 datetime>
---

# <node title>

## Node
- ID: <node ID>
- Depth/order: <D-N; `0` for the root>
- Kind: <goal | work package | uncertainty | experiment | requirements | design | implementation | test | checkpoint>
- Description: <concise description>

## Children
### <child ID> — <child title>
- Order: <D-N>
- Kind: <kind>
- Description: <concise description>
- Group: `<relative numbered path>`

<Repeat in the original recommended order.>

## Notes
- Condition: <when this node applies, or `None`>
- Evidence/status: <uncertainty finding, blocker, or completion signal>
```

Use `0-goal.md` for the root. For each child, use the next depth number and its 1-based sibling position. Slugs are lowercase kebab-case and do not replace the numeric prefix. Keep the same node ID in the file content even when the filename is numbered.

## Completion criterion

The output is complete when the confirmed Wayfinder tree is preserved exactly, file numbering reflects its recommended order, every node has one numbered group file, every parent links its direct children, no path collides, and no design or implementation work was added.
