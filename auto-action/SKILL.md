---
name: auto-action
description: Auto-action skill. Reads the ADR and executes the full action sequence autonomously without confirmation between steps. Use when invoked as /auto-action.
disable-model-invocation: true
---

# Auto-Action

Read the ADR to execute from `.context/adr/`. If multiple ADRs exist, list them and ask the user which to use. If one exists, use it.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`.

Execute the entire Action Sequence straight through — no confirmation between steps. If a step fails or is blocked, stop immediately, report what failed and why, and do not continue.

After all steps are done, report what changed for each step in order. If truths or decisions worth persisting were discovered, or any existing wiki entries are now stale, update `.context/wiki/` via `/to-wiki` — skip it otherwise.

Completion criterion: every step executed and reported, or stopped on first failure with reason.

When done: "Auto-action complete. Run `/evaluate` to assess the result."
