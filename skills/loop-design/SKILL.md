---
name: loop-design
description: Discuss and select the smallest executable feedback element for a development goal, then hand it to to-loop to write one cycle without speculating about future cycles.
disable-model-invocation: true
---

# Loop Design

This skill starts the discussion about building or setting up the work system. It selects the next loop element; `@skills/to-loop` writes the cycle files afterward. One invocation MUST select **at most one cycle**. Prefer completing the current cycle over creating a future cycle.

## Design Loop Mode

Invoking this skill enters **Design Loop Mode**: think about the smallest executable cycle for building or setting up a work system. This mode designs the feedback loop, not the product work itself. **MUST ASK** to user to run `@skills/grill-me` or not; use the available goal, intent, repository state, and run evidence to define the cycle.

Think in this shape:

```text
goal and intent → setup → execute → verify → evidence → pass/fail
```

```text
minimum scope                         maximum scope
one script / setup script  ────────>  one cycle
```

For the first cycle of a new goal, use the available goal and intent. Later cycles reuse that goal and immediate run/review evidence; do not plan future cycles without a new unresolved decision.

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

## Discuss the current loop
Before discuss, see thie references `./references/verification-design.md` and `./references/verification-tools.md`

1. Read the user's request and discussion, the current repository state, existing cycle READMEs, and immediate run/review evidence. Preserve the human's **GOAL** and **INTENT**.
2. Discuss the work-system topic with the human. State the target code or work-system files, the one question the next element must answer, its scope, and its observable pass/fail result. Ask only for decisions needed to select this element; do not invoke `@skills/grill-me`.
3. Select the smallest scope that can answer it: a setup, execution, verification, experiment, or one cycle change. Do not create speculative later cycles.
4. Define only the verification stages needed for the current question, ordered by cost:

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
5. When the discussion is settled and writing is needed, hand the selected element to `@skills/to-loop`. Do not write cycle files in this skill.

## Handoff to to-loop

```text
GOAL: <human's desired outcome>
INTENT: <why the human wants it>
CURRENT STATE: <observed state and evidence>
TARGET CODE: <code or work-system files allowed to change; never verification scripts>
NEXT ELEMENT: <one setup, execution, verification, experiment, or cycle change>
QUESTION: <one thing this element must answer>
SCOPE: <what is included and excluded>
EXPECTED EVIDENCE: <what will be observed>
PASS/FAIL: <observable result>
CHEAPEST METHOD: <why this is the smallest sufficient check>
HANDOFF: @skills/to-loop
```

## Verification cost

Do not choose verification by a time budget. Choose the cheapest method that can falsify the current assumption: prefer a focused subsystem, smaller representative data, reused setup/build artifacts, a test seam, or decomposition. Stop once confidence is sufficient; use E2E or full testing only when cheaper evidence cannot answer the current question.

## Completion

The discussion produces one settled loop-design brief with the human's goal, intent, scope, question, evidence, pass/fail result, and cheapest method. Hand it to `@skills/to-loop`; do not write or run the cycle here.
