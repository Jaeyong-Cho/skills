---
name: to-loop
description: Write one selected loop-design brief as a cycle README and only its needed numbered scripts. Use after loop-design discusses the work-system cycle and the user is ready to record it.
---

# To Loop

Write the cycle selected by `@skills/loop-design`. This skill records the agreed loop; it does not start a new discussion, invoke `@skills/grill-me`, run the cycle, or design a later cycle.

## Workflow

1. Read the complete `@skills/loop-design` handoff, current repository state, existing `loop/cycles/` READMEs, and immediate `loop/runs/` evidence.
2. Use the handoff's **GOAL**, **INTENT**, question, scope, expected evidence, pass/fail result, and cheapest method. Do not invent missing decisions or replace the human's intent with implementation language.
3. Update the current cycle when the selected element belongs there; otherwise create exactly one new `loop/cycles/NN-slug/` directory. Do not create speculative later cycles.
4. Write one or more reusable cycle files inside that directory:
   - required `README.md`;
   - only the needed numbered scripts, such as `00-setup.sh`, `01-execute.sh`, and `02-verify.sh`.
5. The cycle `README.md` MUST record:
   - the human's **GOAL** and **INTENT** as the cycle purpose;
   - the one question and observable pass/fail result;
   - scope and exclusions;
   - ordered scripts and their expected evidence;
   - the cheapest verification method and why it is sufficient; and
   - whether this is a final-confidence cycle.
   - also each step script's brief description.
6. Put setup, execution, experiment, test, or verification commands in the numbered scripts. Each script has clear inputs, outputs, and meaningful exit status. Reuse existing project commands before adding helpers.
7. Keep runtime output out of the cycle directory. Outputs belong under `loop/runs/cycle-NN-{timestamp}/` when `@skills/loop-run` executes the cycle.
8. Stop after writing the cycle definition. Hand it to `@skills/loop-run`; do not run it here.
9. For about reuseable data (previous run's cacheable data) for next run then locate the output here:

   ```text
   loop/cycles/NN-slug/data/
   ```
## Verification order

Write only the stages needed for the current question and order them from cheapest to most expensive:

```text
static/deterministic
→ targeted unit
→ targeted component
→ targeted integration
→ representative path
→ broader regression
→ E2E/full test
```

Use the narrowest check that can falsify the current assumption. E2E and full tests are final-confidence stages, never the first feedback.

## Completion criterion

The selected cycle directory contains its required README and only its needed reusable scripts; the README preserves the human's goal and intent, has an observable question and pass/fail result, and records the cheapest sufficient verification. The cycle is ready for `@skills/loop-run` and has not been executed.
