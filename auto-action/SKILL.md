---
name: auto-action
description: Auto-action skill. Reads a plan and its ADR and executes the full action sequence autonomously without confirmation between steps. Use when invoked as /auto-action.
disable-model-invocation: true
---

# Auto-Action

Read the plan to execute from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture, design, observability, test-loop, and verification context behind the plan's Action Sequence.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`.

Execute the plan's entire Action Sequence straight through — no confirmation between steps. If a step fails or is blocked, stop immediately, report what failed and why, and do not continue.

After all steps are done, report what changed for each step in order, checked against the ADR's Observability and Verification Criteria. Read `.context/req/` for the spec context behind what was decided and why.

Completion criterion: every step executed and reported, or stopped on first failure with reason.

When done: "Auto-action complete." followed by the per-step summary. If a draft RDR (`{timestamp}-{slug}.md`, no `.merged.md` suffix) exists in `.context/req/rdr/` for this slug, add: next step `/merge-req` to commit it into the spec. If a draft ADR (`{timestamp}-{slug}.md`, no `.merged.md` suffix) exists in `.context/adr/` for this slug, add: next step `/merge-archi` to commit it into the architecture doc. If any step failed, mention neither — leave both drafts in place so nothing is committed for unfinished work.
