---
name: auto-action
description: Auto-action skill. Reads a plan and its ADR and executes the full action sequence — fully autonomous for a regular plan; for a self-plan, writes working code with recorded holes left as TODOs, then on a later run (once the human has filled every hole) reviews the implementation against those holes' recorded intent and runs the tests. Use when invoked as /auto-action.
disable-model-invocation: true
---

# Auto-Action

Read the plan to execute from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture, design, observability, test-loop, and verification context behind the plan's Action Sequence.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`.

Check the plan's `**Type:**` line. If it reads `Self-Plan`, check whether its recorded holes are still open: for each implementation step with a **Hole** annotation, open the file and check whether the hole's blanked placeholder(s) (e.g. `/* */`) are still there — the TODO comment above them isn't the signal, since it stays until a hole passes review. If any hole's blank is still present, follow **Self-Plan Execution — Write**. If every hole's blank has been replaced with real code, follow **Self-Plan Execution — Review & Test** instead. If the plan's Type line is anything other than `Self-Plan` (including absent), follow **Full Execution**.

## Full Execution

Execute the plan's entire Action Sequence straight through — no confirmation between steps. If a step fails or is blocked, stop immediately, report what failed and why, and do not continue.

After all steps are done, report what changed for each step in order, checked against the ADR's Observability and Verification Criteria. Read `.context/req/` for the spec context behind what was decided and why.

Completion criterion: every step executed and reported, or stopped on first failure with reason.

## Self-Plan Execution — Write

For each implementation step, write exactly what the step's **Working** and **Hole** annotations specify — this was already decided in `/co-plan`, so do not re-derive or re-apply the rules here. Write working parts complete and runnable. For each hole, write its recorded TODO comment and blanked code skeleton verbatim, following `../references/todo-hole.md` — the surrounding statement structure is real code; only the recorded blank(s) are left for the human.

Each file gets one Write or Edit call that lands its final state directly — holes as TODOs, working parts complete, in the same pass. Never write a full working implementation for a hole's line(s) and then edit it down to a TODO afterward; that's two passes of work for one outcome the self-plan already decided.

Test steps are always written complete, per the plan.

Do not run tests to green — holes are intentionally incomplete, so failing tests are expected. If a step's Working/Hole annotation is missing or unclear, stop and send the user back to `/co-plan` rather than guessing.

Completion criterion: every step written (tests complete, working parts complete, holes marked with explanatory TODOs), or stopped on first missing/unclear annotation with reason. This is a stopping point, not a failure — the plan now waits on the human to fill in every hole before `/auto-action` can move past it.

## Self-Plan Execution — Review & Test

Do not rewrite any file — the human has already replaced every hole's TODO with their own implementation. Instead:

1. **Review.** For each hole, compare what's now in place against that hole's recorded TODO intent (the technique/approach it named) and against the flow the ADR describes. Note, per hole, whether it matches the intent, and flag anything that looks incomplete, mismatched, or that reintroduces working code the plan already wrote elsewhere. Once a hole passes review, remove its TODO comment from the file — the code now there replaces it, and leaving it behind is stale clutter, not documentation worth keeping. Leave the TODO comment in place for any hole that doesn't pass review, alongside the flagged concern, so the human still has it to work from.
2. **Test.** Run the same test scope `/test` would use: read the plan and ADR/RDR for test strategy and scope (default to both unit and integration unless the plan says otherwise), then run those tests and record pass/fail per test.

Completion criterion: every hole reviewed against its recorded intent with a verdict, and the plan's test scope run with results recorded — or stopped with a reason if a hole's recorded intent is missing (send the user back to `/co-plan`) or the project's tests can't be run.

## When Done

**Full Execution:** "Auto-action complete." followed by the per-step summary. If a draft RDR (`{timestamp}-{slug}.md`, no `.merged.md` suffix) exists in `.context/rdr/` for this slug, add: next step `/merge-req` to commit it into the spec. If a draft ADR (`{timestamp}-{slug}.md`, no `.merged.md` suffix) exists in `.context/adr/` for this slug, add: next step `/merge-archi` to commit it and derive the architecture doc. If any step failed, mention neither — leave both drafts in place so nothing is committed for unfinished work.

**Self-Plan Execution — Write:** "Auto-action complete (self-plan)." followed by which files were modified, which were created, and which functions/blocks contain holes for the user to implement. Do not mention `/merge-req` or `/merge-archi` — holes mean implementation isn't finished yet. Tell the user: fill in every hole, then re-run `/auto-action` on this plan — it will detect the holes are filled and switch to reviewing and testing the implementation instead of writing it.

**Self-Plan Execution — Review & Test:** "Auto-action review complete (self-plan)." followed by, per hole, whether it matched its recorded intent (and what looked off if not), then the test results (pass/fail counts, failures listed explicitly). If every hole matched and all tests pass, tell the user the plan's Closeout Review + Test item is satisfied and only Refactor remains. If anything didn't match or tests failed, say so plainly and do not claim Closeout is satisfied.
