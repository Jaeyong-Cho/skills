---
name: loop-design
description: Select and design the smallest executable feedback element for a development goal; one script, setup, verification, experiment, or at most one cycle. Use with to-loop to prepare the current cycle without speculating about future cycles.
---

# Loop Design

`to-loop` identifies the next needed element; this skill designs it. One invocation MUST design or modify **at most one cycle**. Prefer completing or modifying the current cycle over creating a future cycle.

## Shared-understanding gate

Every invocation MUST first run or continue `@skills/grill-me`. Use it to establish shared understanding with the human about the goal, the current cycle question, and the observable pass/fail result. Do not design, write, or modify a cycle until `grill-me` reaches an empty frontier and the human explicitly confirms the shared understanding. For later cycles, an existing confirmed context may make this a short confirmation, but `grill-me` still MUST run; re-interview whenever a new decision or ambiguity appears.

```text
minimum scope                         maximum scope
one script / setup script  ────────>  one cycle
```

For the first cycle of a new goal, use its confirmed `grill-me` context. Later cycles reuse that confirmed goal and immediate run/review evidence; do not re-interview or plan future cycles without a new unresolved decision.

## Cycle layout

Every new cycle directory is `NN-slug/`, with a two-digit numeric prefix. Cycle directories contain reusable definitions only:

```text
loop/
├── cycles/
│   └── NN-slug/
│       ├── README.md
│       ├── 00-setup.sh
│       ├── 01-execute.sh
│       └── 02-verify.sh
└── runs/
    └── cycle-NN-{timestamp}/
        ├── logs/
        ├── outputs/
        └── results/
```

Create only needed scripts, named `NN-{step}.sh` in execution order. Never store runtime output in a cycle directory; all runtime artifacts belong in `loop/runs/cycle-NN-{timestamp}/`.

## Design the current element

1. Read the goal, current repository state, existing cycle READMEs, and immediate run/review evidence. State the one question this element must answer and its observable pass/fail result.
2. Select the smallest scope that can answer it: add or change one script in the current cycle when sufficient; otherwise create one new cycle. Do not create speculative later cycles.
3. Write or update that cycle's `README.md` with the human's **GOAL** and **INTENT** as the purpose of the cycle, followed by its question, scope, ordered scripts, expected evidence, and whether it is a final-confidence cycle. Preserve the human's meaning; do not replace it with implementation language.
4. Put setup, execution, test, experiment, or verification commands in the numbered scripts. Each script has clear inputs, outputs, and meaningful exit status. Reuse existing project commands before adding helpers. Read [verification-design.md](references/verification-design.md) for non-trivial behavior, API, structure, or architecture checks; read [verification-tools.md](references/verification-tools.md) only when an existing command cannot express a required check.
5. Define only the verification stages needed for the current question, ordered by cost:

   ```text
   static/deterministic
   → targeted unit
   → targeted component
   → targeted integration
   → representative path
   → broader regression
   → E2E/full test
   ```

   Stop once confidence is sufficient. E2E and full tests are confidence gates: they MUST be the last stage and never the first development feedback. Use the narrowest verification that can falsify the current assumption; challenge any proposal that starts broad.

## Verification cost

Do not choose verification by a time budget. Choose the cheapest method that can falsify the current assumption: prefer a focused subsystem, smaller representative data, reused setup/build artifacts, a test seam, or decomposition. Stop once confidence is sufficient; use E2E or full testing only when cheaper evidence cannot answer the current question.

## Completion

The cycle README and only its needed reusable scripts exist and are ordered by cost. Hand the selected cycle to `@skills/loop-run`; do not run or design another cycle here.
