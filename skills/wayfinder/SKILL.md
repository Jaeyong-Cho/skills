---
name: wayfinder
description: Decompose one goal into a concise tree of high-level work-package ways, recursing only where useful; show uncertainty, requirements, design, implementation, and testing for atomic work. Invoke as /wayfinder.
disable-model-invocation: true
---

# Wayfinder

Make a high-level plan tree for one goal. The tree answers:

> What major work is needed, what does each major work package contain, and what must happen before an atomic work package can ship?

This is a planning artifact only. Do not write code, tests, detailed designs, or skill handoffs.

## Ways are work packages

A way is a child work package that contributes to its parent. Sibling ways are usually all required, not competing alternatives.

```text
Build Tetris
├── Setup project build system
├── Make TUI
├── Make main menu
├── Make Tetris game
└── Make settings
```

A way may have its own ways:

```text
Make Tetris game
├── Make tetrimino shape
├── Make tetrimino rotate
├── Make tetrimino drop logic
├── Make clear line logic
└── Make score logic
```

When `Make score logic` is atomic, show its concise delivery sequence:

```text
Make score logic
├── Experiment score algorithm
├── Define requirements and edge cases
├── Design architecture
├── Implement
└── Test
```

Use the user's domain language. Do not expand this into commands, classes, individual functions, or every test case.

## Decomposition rules

- Handle one root goal per invocation.
- Give every node a short stable ID and exactly one parent.
- Start with the major capabilities or work packages, not lifecycle phases.
- Recursively split a node only when it contains multiple meaningful sub-goals or decisions.
- Stop at a work package that is small enough to plan as one unit but still meaningful to the user.
- Do not split merely to make the tree deeper. High-level coverage is more important than exhaustive detail.
- Keep sibling ways distinct and collectively complete for their parent. Order them by dependency or delivery sequence when useful.
- Add the uncertainty → requirements → design → implement → test sequence only under an atomic work package.
- Do not add graph edges, cross-links, implementation details, or skill handoffs.

## Uncertainty

Place an uncertainty at the smallest node it affects.

- If it changes how a parent must be decomposed, make `[?] Understand ...` the first child and stop dependent decomposition until it is resolved.
- If it affects only an atomic work package, make `Experiment ...` its first child.
- Resolve it with the cheapest reliable action: inspect existing code/docs, explore behavior, run a small reversible experiment, or ask the owner for a product decision.
- For an experiment, name only the question, method, and pass/fail signal.
- For a human decision, state the consequence of each answer and use the `❓` / `➡️` format.
- Record unresolved blockers as `[BLOCKED]`; never fill the tree with guesses.

Do not add an uncertainty node for a detail that can wait until requirements or design.

## Atomic work-package sequence

For an atomic node, use these high-level children in order:

1. **Experiment** — only when a meaningful uncertainty needs evidence; otherwise omit it.
2. **Define requirements** — define observable behavior, important edge cases, scope, and acceptance signals.
3. **Design architecture** — explore the existing codebase, then select what to reuse, modify, create, or delete and describe the solution boundaries.
4. **Implement** — make the smallest change that satisfies the approved requirements and design.
5. **Test** — verify the behavior, regressions, build, and relevant integration flow.

These are plan stages, not detailed task lists. The downstream planning or implementation work can expand them later.

## Planning process

1. Capture the single goal and its success signal.
2. Inspect enough repository context to avoid planning work that already exists.
3. List the goal's major work packages.
4. Recurse only into work packages that contain meaningful sub-goals.
5. Mark uncertainties where they change decomposition or execution.
6. Add the five-stage sequence to each atomic work package.
7. Check that the tree covers the goal without unnecessary depth.

If the goal or success signal is missing, ask one focused question and wait. If a blocker remains unanswered, return the partial tree with the blocker marked.

## Output format

Return only the concise tree. Add a short note below it only for a blocker, an uncertainty, or a non-obvious ordering decision.

```markdown
## Plan tree
G [Build Tetris]
├── A [Setup project build system]
├── B [Make TUI]
├── C [Make main menu]
├── D [Make Tetris game]
│   ├── D1 [Make tetrimino shape]
│   ├── D2 [Make tetrimino rotate]
│   ├── D3 [Make tetrimino drop logic]
│   ├── D4 [Make clear line logic]
│   └── D5 [Make score logic]
│       ├── D5.1 [Experiment score algorithm]
│       ├── D5.2 [Define requirements and edge cases]
│       ├── D5.3 [Design architecture]
│       ├── D5.4 [Implement]
│       └── D5.5 [Test]
└── E [Make settings]
```

Use the actual goal. Keep node titles short. Do not add a separate node for every acceptance criterion, file, command, object, or test case.

## Completion criterion

The tree is complete when one goal is the root, its major work packages are visible, meaningful sub-goals are decomposed where needed, uncertainties are marked at the correct level, atomic work packages show the concise delivery sequence, and no unnecessary low-level detail or skill handoff appears.
