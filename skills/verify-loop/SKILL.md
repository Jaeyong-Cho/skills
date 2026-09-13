---
name: verify-loop
description: Drive a requested change through one specified target test: prepare first, run the test, identify an evidence-backed Gap, and resolve it with safe retries.
disable-model-invocation: true
license: MIT
---

# Verify Loop

This is the implementation-and-verification loop. Read [`../references/verification-structure.md`](../references/verification-structure.md) and [`../references/deterministic-evaluation.md`](../references/deterministic-evaluation.md) before running checks.

Use `verify-design` first when the project lacks the `verify/` interface or when a new feature, bug, or other non-current expected state needs a focused red check. `verify-loop` runs checks, analyzes gaps, dispatches scoped implementation attempts, and judges acceptance; it does not invent requirements.

## Establish shared intent

Before running checks, dispatching a scout, or changing code, **MUST RUN** a session of `@skills/grill-me` in the current conversation. Give it the requested goal, project, requested state, evidence, maximum cycles, and [`../references/intent-checklist.md`](../references/intent-checklist.md). It must establish the observable outcome, scope, constraints, and assumptions, then discuss the cheapest sufficient evidence method for reaching the user's intended goal:

- compare only the relevant target-test options and their verification domains;
- prefer the lowest sufficient domain and an existing native test or focused runner;
- define the exact single command, check path, expected result, deterministic pass signal, and what evidence would be insufficient;
- identify the cost and coverage trade-off without expanding into a broad verification suite.

`grill-me` must finish with the recommended target test and domain, a teach-back, and explicit human confirmation. Do not begin the loop until the human confirms. Use that confirmed outcome, cheapest-method decision, and acceptance condition as the target; do not invent requirements.

After confirmation, require exactly one **Target test**: the exact single command to run, its check path, expected result, and deterministic pass signal. The target may specify one verification domain (`ut`, `it`, `e2e`, `style`, or `archi`); record that domain and run only its target test. Reject a non-positive cycle count. If the target test, expected result, or acceptance condition is not judgeable, stop and ask for clarification. Do not substitute a broad UT/IT/E2E suite or unrelated Style/Architecture checks.

The main agent MUST compare the target test's intent, assertion, pass signal, observed result, and confirmed acceptance condition before resolving a Gap. If any tests or requirements contradict each other, or the target test cannot consistently express the requested outcome, stop as **BLOCKED**, report **CONTRADICTION**, and request that `verify-design` be fixed. Do not edit implementation code or dispatch a resolver for a contradictory test design.

## Target-test loop

`verify-loop` runs only the specified target test through this loop:

```text
prepare ──pass──> target test ──pass──> ACCEPT
                       │
                       └──fail──> GAP ──resolve──> repeat
```

1. Start `verify/prepare/run.sh` and wait for it to pass. Do not start the target test before preparation completes successfully.
2. Run exactly the specified target test command and capture its output and exit status separately. A test passes only with its stated deterministic pass signal and zero exit status.
3. If the target test passes, accept only when it observes the requested outcome; do not run additional checks.
4. If the target test fails, record a **GAP**, analyze its evidence, and resolve only that gap.
5. After a resolver edit, repeat preparation and the same target test. Never replace it with another test or silently expand the scope.

The target test may be a project runner such as `./verify/ut/run.sh` or a native test command. Every command must remain independently invokable. A domain target does not authorize running the domain's other tests or any other domain. If preparation fails, report the preparation failure as **BLOCKED** and do not start the target test.

Before reporting a failure, read the nearest `index.md` when the target is under `verify/` and print:

```text
FAIL: target test
Intent: <why this test exists, from its index.md or test definition>
Violated: <rule, expected behavior, stable test name, or assertion>
Command: <exact target test command>
Evidence:
<captured output>
```

Use the target test's own rule identifier, assertion, test name, or runner message for `Violated`. Never invent a rule. If none is available, use `Violated: target test failed` and retain the raw output. For a requested state, also print `Expected` and `Observed`.

## Cycle

Repeat until accepted, blocked, or the maximum is reached.

### 1. Inspect current state — dispatch a read-only scout

Give a scout the target, acceptance condition, project, current diff, target domain, exact target test command, and available evidence. Require it to:

- inspect the implementation and relevant callers;
- run `verify/prepare/run.sh` first and only start the target test after it passes;
- run exactly the specified target test, not a broader verification suite;
- compare observed behavior with the acceptance condition;
- report changed files, the exact target-test failure, its intent and violated rule, risks, and evidence;
- make no edits and delegate no further work.

If `verify/`, `verify/prepare/`, or a required runner is missing, report **BLOCKED** and recommend `verify-design`; do not silently run unrelated commands as a substitute.

### 2. Analyze the gap — main orchestrator

The main orchestrator must first reconcile the target domain, test intent, assertion, pass signal, observed result, and confirmed acceptance condition. Classify the current state as:

- **Accepted candidate:** the target test passes and the acceptance condition is met;
- **Gap:** the target test has a concrete failure that contradicts the acceptance condition;
- **Blocked:** evidence is missing, the requirement is ambiguous, a runner cannot execute, or a human-owned decision is required;
- **Contradiction:** tests, test definitions, domain intent, or requirements demand incompatible outcomes. Treat this as **BLOCKED**.

For **Contradiction**, stop immediately. Do not infer a preferred rule, edit implementation code, or dispatch a resolver. Report the conflicting commands/assertions and request that `verify-design` correct the verification design before restarting `verify-loop`.

For a Gap, analyze the root cause rather than repeating the failed symptom. State exactly:

```text
Gap: <current result differs from expected>
Intent: <why the failing verification exists>
Violated: <rule or expected behavior>
Root cause: <supported cause, or `cannot determine`>
Improved strategy: <one smallest safe change>
Proof: <verification command and expected evidence>
```

Do not dispatch a resolver for a guessed root cause. If the root cause cannot be determined from the code and evidence, stop as **BLOCKED** or run the smallest targeted investigation before editing.

### 3. Snapshot and resolve — dispatch one scoped worker

Before editing, record the current diff and the resolver scope. Dispatch at most one worker with the target, acceptance condition, inspected evidence, and exactly the improved strategy.

Require it to:

- change only the scoped implementation, test, configuration, or documentation;
- preserve unrelated behavior and avoid speculative refactors;
- run preparation and the exact target test after editing;
- report changed files, commands, results, residual risks, and unresolved gaps;
- stop rather than guess if the strategy is insufficient or requirements conflict.

The worker may edit; `verify-loop` itself does not directly implement the gap. Do not accept the worker's claim without reviewing its diff and evidence.

### 4. Verify and judge the attempt

Run preparation and the same target test again. Inspect the current diff and compare current evidence with the acceptance condition. Do not run unrelated verification.

Judge one of:

- **ACCEPT:** the target test passes with its deterministic signal, observes the requested outcome, and no blocking regression or unresolved risk contradicts the target;
- **CONTINUE:** the attempt failed, a concrete root cause and improved strategy are available, and another cycle remains;
- **STOP:** maximum reached, evidence is missing, rollback is unsafe, the change is destructive, or human judgment is required.

A passing command is not acceptance unless it observes the target. A clean diff is not acceptance. Invalidate all pre-attempt evidence after editing.

### 5. Roll back a failed attempt before retrying

When a resolver attempt does not satisfy the target:

1. Confirm the failure with current verification evidence.
2. Compare the post-attempt scope with the pre-attempt snapshot.
3. Automatically remove only the resolver's scoped changes, restoring the exact pre-attempt state.
4. Preserve unrelated pre-existing changes and untracked files.
5. If the attempt overlaps unrelated work or cannot be restored safely, stop as **STOP** and ask for human handling.
6. Use the analyzed root cause and improved strategy as the next cycle's input; do not repeat the same attempt.

A rollback is complete only when the pre-attempt diff and file contents are restored and verified. Never leave a known failed attempt in place while dispatching a retry.

After **ACCEPT**, stop immediately. Do not spend remaining cycles on optional cleanup.

## Controls

- Default maximum: `3` cycles; honor a user-supplied positive integer exactly.
- One read-only scout and at most one resolver per cycle.
- The resolver depends on target-test inspection and root-cause analysis.
- Preparation is mandatory and completes before the target test.
- Do not dispatch a resolver for a passing target test or unsupported root cause.
- Failed resolver attempts are rolled back before retry; do not silently keep partial fixes.
- Stop for contradictory tests, test definitions, domain intents, or requirements; report **CONTRADICTION** and request a `verify-design` fix before continuing.
- Also stop for ambiguity, unsafe rollback, destructive/security-sensitive changes without authority, unavailable credentials, or a human-owned decision.
- Never claim success when the loop stops at its maximum or a blocker.

## Output

Return all progress in the current session; do not create a report file unless requested.

```markdown
# Verify Loop

- Target: [requested outcome]
- Acceptance: [observable condition]
- Project: [path]
- Target domain: [ut | it | e2e | style | archi | native]
- Target test: [exact command and check path]
- Cheapest sufficient method: [confirmed rationale and rejected broader alternatives]
- Maximum cycles: [number]

## Cycle [n]

### State evidence
- [commands and observed results]
- [gap, or `None`]

### Root-cause analysis
- **Intent:** [why the verification exists]
- **Violated:** [rule or expected behavior]
- **Root cause:** [supported cause]
- **Improved strategy:** [one change]
- **Proof:** [verification command]

### Resolution
- **Worker:** [subagent]
- **Changed files:** [paths]
- **Verification:** [results]
- **Rollback:** [not needed | restored before retry | unsafe]

### Judgment
- **[ACCEPT | CONTINUE | STOP]** — [current evidence and reason]

## Final status
[Accepted | Stopped at maximum | Blocked | Needs human decision]

## Residual risks
- [risk, or `None`]
```

The loop is complete only when the final judgment is supported by current evidence, every child result and resolver diff was reviewed, every failed attempt was safely removed before retry, and the status distinguishes acceptance from maximum-cycle or blocker termination.
