---
name: wayfinder
description: Recursively decompose one goal into work-package ways, then plan uncertainty removal, requirements, design, implementation, and tests for each atomic goal. Invoke as /wayfinder.
disable-model-invocation: true
---

# Wayfinder

Make a hierarchical plan tree for one goal. Start with the major work packages needed to reach the goal. Decompose each work package into smaller work packages until the work is atomic. At an atomic goal, add the execution sequence:

```text
remove uncertainty → specify requirements → design → implement → test
```

This is a planning artifact only. Do not write production code or tests. Do not invoke another skill or add skill handoffs.

## What a “way” means

A way is a child work package that contributes to its parent goal. Ways are not necessarily alternatives. For example, building Tetris can require all of these sibling ways:

```text
Build Tetris
├── Setup project build system
├── Make TUI
├── Make main menu
├── Make Tetris game
└── Make settings
```

`Make Tetris game` is then decomposed independently:

```text
Make Tetris game
├── Make tetrimino shape
├── Make tetrimino rotate
├── Make tetrimino drop logic
├── Make clear line logic
└── Make score logic
```

`Make score logic` is an atomic goal only when its next work is clear. Its execution tree is:

```text
Make score logic
├── Experiment score algorithm
├── Define requirements and edge cases
├── Design architecture
├── Implement
└── Test
```

Use the real goal and repository context instead of copying this example.

## Decomposition rules

- Handle one root goal per invocation.
- Give every node a stable unique ID and exactly one parent.
- Decompose a goal into the complete set of sibling work packages needed for that goal. They should be mutually exclusive and collectively exhaustive at that level.
- Do not force the uncertainty/requirements/design/implementation/test sequence onto a non-atomic goal. First split that goal into its ways.
- Continue splitting until a junior developer can execute the node without making a new product or architecture decision.
- A node is atomic based on decision scope, not size. “Make Tetris game” is not atomic; “Make score logic” may be.
- Do not choose, rank, or collapse sibling ways. They are the plan tree, not a menu of alternatives.
- Order siblings in a useful dependency or delivery order. State the reason when order is not obvious.
- Every leaf must name a concrete action and an observable completion signal.
- Do not add cross-links or graph edges. If two branches need the same work, move that work to their nearest common parent or record the dependency in the node detail without breaking the tree.

## Remove uncertainty

At every goal, ask whether an unknown could change its decomposition or execution. Put that unknown at the smallest node it affects.

- If the unknown changes how a goal must be split, make `[?] Understand ...` the first child of that goal. Do not invent dependent children until it is resolved.
- If the unknown only affects an atomic goal's solution, make `Experiment ...` the first execution child.
- If repository evidence can answer it, inspect the relevant files, tests, commands, and conventions and record the evidence.
- If execution is required, create an experiment with a question, hypothesis, smallest reversible method, pass/fail signal, and result.
- If it is a product policy or priority, create a human decision with the exact consequence of each answer. Use the `❓` / `➡️` format when asking.
- If it is a low-risk assumption, record the assumption, its uncertainty level (`[H]` or `[L]`), and the signal that will validate it.
- Never hide an unresolved uncertainty in a requirement or design. An unresolved blocker remains `[BLOCKED]`, and dependent work is not fabricated.

An uncertainty node is atomic: resolving it may reveal a new uncertainty, but that becomes a new sibling under the affected parent, not a child hidden inside the old node.

## Atomic-goal execution sequence

For every atomic work package, use these children in order. Omit a child only when repository evidence shows that work is already complete; record that evidence.

### 1. Remove uncertainty

Identify and resolve unknowns about feasibility, behavior, constraints, or the solution. Use repository inspection, exploration, an experiment, or a human decision. If no uncertainty remains, record that check as complete rather than inventing an experiment.

For an experiment, include:

- question;
- hypothesis;
- smallest reversible method;
- supporting and rejecting signals;
- result, decision, or blocked status.

### 2. Specify requirements

Define what must be true, without choosing implementation:

- actor, trigger, purpose, and observable outcome;
- normal, boundary, alternate, and failure cases;
- invariants and constraints;
- in scope, out of scope, and deferred behavior;
- Given–When–Then acceptance criteria;
- a deterministic verification method and test path for every criterion.

The requirements child is complete only when behavior is testable and no product decision is silently assumed.

### 3. Design architecture

Define how the approved behavior fits the repository:

- existing code and boundaries to reuse;
- responsibilities and owned state;
- data and invariants;
- interfaces/contracts and failure handling;
- normal workflow;
- requirement-to-design-to-test traceability;
- smallest design and its explicit trade-offs.

The design child is complete only when each requirement and relevant edge case has an owner and a verification path.

### 4. Implement

Break the design into the smallest ordered implementation tasks. For each task, name the production path, dependency, and expected result. Keep implementation inside the approved requirement and design; a new behavior or architectural decision returns to the relevant earlier child.

### 5. Test

Plan the checks that prove the atomic goal:

- focused tests for each acceptance criterion;
- regression tests;
- build checks;
- integration or end-to-end checks where the behavior crosses a boundary;
- acceptance review against the requirement;
- diff and residual-risk review;
- human approval before commit, merge, or release.

Name the real test files and commands. “Test it” is not an actionable leaf.

## Inspect before planning

Before building the tree:

1. Read the user's goal and success signal.
2. Inspect relevant repository instructions, source files, tests, build configuration, and existing requirements/design documents.
3. Identify existing work that already satisfies a node; do not plan it again.
4. Record facts, assumptions, constraints, and uncertainties.
5. Ask only for missing information that cannot be found by inspection and that changes the tree.

If the root goal or success signal is missing, ask one focused question and wait. If a blocker remains unanswered, return the partial tree with the blocker clearly marked.

## Output format

Return only a plan tree and concise node details. Do not return a route graph, edge list, skill list, or implementation.

```markdown
## Plan tree
G [Goal: build Tetris]
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

## Node details
### [ID] — [title]
- Kind: [goal | uncertainty | experiment | requirements | design | implementation | test | checkpoint]
- Action: [the concrete work to perform]
- Evidence/done when: [finding, artifact, test, command, or approval]
- Condition: [why this child applies, or `None`]

[Repeat for every node in tree order.]
```

For each non-atomic node, its children must be the actual domain work packages, not generic lifecycle phases. For each atomic node, its children must cover uncertainty removal, requirements, design, implementation, and testing in that order. Use the user's terminology where possible.

## Completion criterion

The tree is complete when the root is one goal; every non-atomic goal is decomposed into complete sibling ways; every uncertainty that can change the plan is resolved, recorded, or blocked at the correct node; every atomic goal has the five execution stages; every leaf has an action and observable evidence; and the final test nodes name the checks and human gates needed to prove the goal. No downstream skill handoff appears.
