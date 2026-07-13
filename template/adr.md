# ADR: {Title}

**Date:** {YYYY-MM-DD}

## Decision
> The problem being solved and the choice made to address it.

- Problem: {what the direction is and what problem it solves}
- Decision: {what was decided and the key architectural choices}

## Design
> Module structure, contracts, data flows, and how to observe it working mid-execution.

- {module / contract / data-flow bullets}
- Observability: {checkpoints, logs, assertions, debug data to judge it's working}

## Action Sequence
> Ordered atomic steps. Each step: one concern, describable without "and".

1. {First atomic step}
2. {Second atomic step}

## Closeout
> Fixed steps, always last, in order.

- [ ] Refactor — readable code, readable architecture, clear naming, simple over clever, remove unused files and dead code, flatten unnecessary abstractions.
- [ ] Test — run the test-loop to verify the refactor didn't break anything.
- [ ] Wiki — update `.context/wiki/` via `/to-wiki` if new truths found or stale (skip otherwise).
- [ ] Changelog — write an entry via `/to-changelog`.
- [ ] TODO — remove the originating `.context/TODO.md` item via `/to-todo`, if one exists.

## Verification
> What proves the plan worked, and how to check it.

- Run: {what it resets/initializes, executes, writes — results, metadata}
- Verify: {what it reads and checks per scenario}

|Scenario|Expected Result|How Checked|
|--|--|--|
|{scenario name}|{expected result}|{binary pass/fail, numeric range, or rubric}|
