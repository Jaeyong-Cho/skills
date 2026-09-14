---
name: loop-run
description: Execute one selected NN-slug loop cycle, capture all runtime evidence, review its cost and sufficiency, and commit an accepted scoped change. Use after loop-design prepares a cycle; it never runs multiple cycles.
---

# Loop Run

Execute exactly one selected `loop/cycles/NN-slug/` cycle. Do not design, broaden, or start another cycle while running it.

## Single-subagent boundary

Sub-agent dispatch is optional. If a sub-agent is used, it owns the selected cycle end to end: it runs the scripts, captures evidence, diagnoses failures, applies only the scoped fix, reruns the cycle when needed, reviews the result, and returns the verdict. Never split this work between a verify runner and a fix agent, and never use a second sub-agent for the same cycle. A scoped retry is still part of this one cycle; it is not a new cycle.

## Preconditions

1. Read the cycle `README.md`, validate its `NN-slug` name, script order, and expected evidence.
2. Create one run directory before execution:

   ```text
   loop/runs/cycle-NN-{timestamp}/
   ├── logs/
   ├── outputs/
   └── results/
   ```

   Record cycle path, Git state, commands, start time, and environment metadata. Export the run path to scripts so their artifacts go under `outputs/` or `results/`.

## Execute cheaply and in order

Run `NN-{step}.sh` scripts numerically. Capture each script's stdout and stderr under `logs/`, its exit status and duration under `results/`, and all required outputs, test results, measurements, benchmarks, and other artifacts under `outputs/` or `results/`.

Before rerunning a passing step, reuse its immediate prior result only when its command, environment, and observed inputs are unchanged. Otherwise execute it. Reuse is never allowed for a cycle's final E2E or full-test stage: that stage MUST execute when the cycle reaches it.

Run verification from narrowest/cheapest to broadest/most expensive. Do not execute E2E or a full test until every required cheaper stage in this cycle has passed. Stop at the first unexpected failure or missing expected evidence; preserve the evidence and do not run later expensive stages.

The single sub-agent owns any diagnosis or scoped source change. It makes only the small change explicitly scoped by this cycle and does not add unrelated work.

## Review the cycle

Review the cycle README, captured evidence, elapsed time, Git diff, and reused results. Determine whether:

- the intended question was answered;
- verification went from cheap/targeted to broad/expensive;
- the representative evidence was sufficient;
- E2E/full testing, if used, was final verification only;
- another cycle is actually necessary.

Return exactly one verdict:

- **DONE:** evidence is sufficient at justified cost. If the cycle made a scoped source or reusable-cycle-definition change, inspect Git status and diff, then create one focused commit. Do not include unrelated changes or generated run artifacts unless required deliverables.
- **NEXT-CYCLE:** this cycle is sufficient but reveals one next necessary question. Hand only that question to `@skills/to-loop`; do not design it here.
- **RETRY:** the result is inconclusive or failed for a correctable issue within this scope. State the smallest correction and rerun only this cycle.
- **ESCALATE:** requirements conflict, evidence is ambiguous, the cycle is unnecessarily broad, or E2E/full testing was ordinary feedback. Alert the human with exact evidence; do not broaden, commit, or start another cycle.

## Result

```text
Cycle: NN-slug
Run: loop/runs/cycle-NN-{timestamp}/
Steps: executed and validly reused results
First failure: script, expected, actual, evidence (or none)
Final stage: not reached | passed | failed
Review: cost order, evidence sufficiency, and verdict
Commit: hash | not applicable | blocked
Next: none | to-loop | retry | human escalation
```
