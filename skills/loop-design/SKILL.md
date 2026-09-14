---
name: loop-design
description: Select and design the smallest executable feedback element for a development goal: one script, setup, verification, experiment, or at most one cycle. Use with to-loop to prepare the current cycle without speculating about future cycles.
---

# Loop Design

`to-loop` identifies the next needed element; this skill designs it. One invocation MUST design or modify **at most one cycle**. Prefer completing or modifying the current cycle over creating a future cycle.

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
3. Write or update that cycle's `README.md` with its question, scope, ordered scripts, expected evidence, execution budget, and whether it is a final-confidence cycle.
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

## Three-minute budget

A normal cycle MUST finish within three minutes. Before accepting a longer design, try a focused subsystem, smaller representative data, reused setup/build artifacts, a test seam, or decomposition.

A cycle exceeding three minutes is allowed only when its `README.md` contains:

```text
Execution Budget: <duration>

Justification:
<why this runtime is necessary>

Why a cheaper representative verification is insufficient:
<evidence>
```

An E2E or full test does not justify a longer budget by itself. It must also document why final verification is necessary now and why cheaper checks already performed are insufficient.

## Completion

The cycle README and only its needed reusable scripts exist, are ordered by cost, and specify a three-minute-or-justified budget. Hand the selected cycle to `@skills/loop-run`; do not run or design another cycle here.
