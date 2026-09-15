---
name: loop-run
description: Run one selected NN-slug cycle as a single feedback loop; capture the expected/current gap, change the target code, and rerun to verify the change. Use after to-loop prepares a cycle; it never starts a second cycle.
disable-model-invocation: true
---

# Loop Run

Run exactly one selected `loop/cycles/NN-slug/` cycle as one feedback loop. Do not design or start another cycle here.

## Preconditions

1. Read the cycle `README.md` and validate its `NN-slug` name, script order, target code, expected evidence, and pass/fail result.
2. Create one run directory before execution:

   ```text
   loop/runs/cycle-NN-{timestamp}/
   ├── logs/
   ├── outputs/
   └── results/
   ```

   Record the cycle path, Git state, commands, start time, and environment metadata. Export the run path to scripts so their artifacts go under `outputs/` or `results/`.

## One feedback loop

1. Run the selected cycle's numbered scripts in order. Capture stdout and stderr under `logs/`, exit statuses under `results/`, and required outputs under `outputs/` or `results/`.
2. Compare the expected result with the current result. Record the **GAP**—what should happen, what happened, and the evidence showing the difference.
3. If a GAP exists, make the smallest scoped change to the **target code** that reduces it. Do not change verification scripts, weaken assertions, alter expected results, or add unrelated work to make the cycle pass.
4. Rerun the same selected cycle to verify the target-code change. Capture the new evidence and whether the GAP closed, narrowed, or remains.
5. Stop after this feedback loop. Do not start another cycle or perform another fix-and-rerun iteration here. A remaining GAP returns to a later `@skills/loop-design` discussion.

Run verification from narrowest/cheapest to broadest/most expensive. Do not execute E2E or a full test until every required cheaper stage in this cycle has passed. Preserve all initial and rerun evidence.

## Result

Return exactly one run result:

```text
Cycle: NN-slug
Run: loop/runs/cycle-NN-{timestamp}/
Expected: <intended result>
Initial current: <observed result>
Initial GAP: <difference and evidence>
Target change: <scoped target-code change, or none>
Rerun current: <observed result>
Final GAP: closed | narrowed | remains | none
Evidence: <paths to initial and rerun evidence>
Status: passed | failed | incomplete
Next: none | loop-design | human review
```

## Completion criterion

One selected cycle completed one feedback loop: it captured the expected/current GAP with evidence, made at most one scoped target-code change without modifying verification scripts, reran the same cycle, and reported whether the GAP closed. No second cycle or additional fix iteration was started.
