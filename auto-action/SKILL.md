---
name: auto-action
description: Auto-action skill. Reads a plan and its ADR and executes the full action sequence — fully autonomous for a regular plan, or with recorded holes left as TODOs for a self-plan. Use when invoked as /auto-action.
disable-model-invocation: true
---

# Auto-Action

Read the plan to execute from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture, design, observability, test-loop, and verification context behind the plan's Action Sequence.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`.

Check the plan's `**Type:**` line. If it reads `Self-Plan`, follow **Self-Plan Execution**. Otherwise (no Type line, or any other value) follow **Full Execution**.

## Full Execution

Execute the plan's entire Action Sequence straight through — no confirmation between steps. If a step fails or is blocked, stop immediately, report what failed and why, and do not continue.

After all steps are done, report what changed for each step in order, checked against the ADR's Observability and Verification Criteria. Read `.context/req/` for the spec context behind what was decided and why.

Completion criterion: every step executed and reported, or stopped on first failure with reason.

## Self-Plan Execution

For each implementation step, write exactly what the step's **Working** and **Hole** annotations specify — this was already decided in `/self-planning`, so do not re-derive or re-apply the five rules here. Write working parts complete and runnable. For each hole, write its recorded TODO text verbatim, following `../references/todo-hole.md`.

Test steps are always written complete, per the plan.

Do not run tests to green — holes are intentionally incomplete, so failing tests are expected. If a step's Working/Hole annotation is missing or unclear, stop and send the user back to `/self-planning` rather than guessing.

Completion criterion: every step written (tests complete, working parts complete, holes marked with explanatory TODOs), or stopped on first missing/unclear annotation with reason.

## When Done

**Full Execution:** "Auto-action complete." followed by the per-step summary. If a draft RDR (`{timestamp}-{slug}.md`, no `.merged.md` suffix) exists in `.context/rdr/` for this slug, add: next step `/merge-req` to commit it into the spec. If a draft ADR (`{timestamp}-{slug}.md`, no `.merged.md` suffix) exists in `.context/adr/` for this slug, add: next step `/merge-archi` to commit it and derive the architecture doc. If any step failed, mention neither — leave both drafts in place so nothing is committed for unfinished work.

**Self-Plan Execution:** "Auto-action complete (self-plan)." followed by which files were modified, which were created, and which functions/blocks contain holes for the user to implement. Do not mention `/merge-req` or `/merge-archi` — holes mean implementation isn't finished yet.
