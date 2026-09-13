---
name: verify-loop
description: Drive a requested change to evidence-backed acceptance by preparing first, then running ordered UT → IT → E2E verification with independent Style and Architecture gates, analyzing failures, and retrying failed resolver attempts with a safer strategy.
disable-model-invocation: true
license: MIT
---

# Verify Loop

This is the implementation-and-verification loop. Read [`../references/verification-structure.md`](../references/verification-structure.md) and [`../references/deterministic-evaluation.md`](../references/deterministic-evaluation.md) before running checks.

Use `verify-design` first when the project lacks the `verify/` interface or when a new feature, bug, or other non-current expected state needs a focused red check. `verify-loop` runs checks, analyzes gaps, dispatches scoped implementation attempts, and judges acceptance; it does not invent requirements.

## Establish shared intent

Before running checks, dispatching a scout, or changing code, **MUST RUN** a session of `@skills/grill-me` in the current conversation. Give it the requested goal, project, requested state, evidence, level, maximum cycles, and [`../references/intent-checklist.md`](../references/intent-checklist.md). It must establish the observable outcome, scope, constraints, and assumptions, follow its calibration, impact, uncertainty, and round rules, and finish with a teach-back and explicit confirmation of shared understanding. Do not begin the loop until the human confirms. Use that confirmed outcome and acceptance condition as the target; do not invent requirements.

After confirmation, reject an unknown level or non-positive cycle count. If the target or acceptance condition is not judgeable, stop and ask for clarification.

## Verification execution

For each verification run, use preparation, the selected functional chain, and two independent gates:

```text
prepare ──pass──> ut ──pass──> it ──pass──> e2e (only through the selected level)
                    │            │            │
                    └────────────┴────────────┴── style + archi run independently and in parallel
```

1. Start `verify/prepare/run.sh` and wait for it to pass. Do not start any other runner before it completes successfully.
2. After preparation passes, start `verify/style/run.sh`, `verify/archi/run.sh`, and `verify/ut/run.sh` independently.
3. Start IT only after UT passes and only for `it` or `e2e`.
4. Start E2E only after IT passes and only for `e2e`.
5. Stop starting later functional levels after any known failure. Let already-running independent checks finish so their evidence is retained.
6. Capture each command's output and exit status separately. A runner passes only with exit status zero.

Every item is independently invokable with one command (`./verify/<item>/run.sh`). When using the project root runner, use `./verify/run.sh <item>` where `<item>` is `prepare`, `ut`, `it`, `e2e`, `style`, or `archi`; it must perform preparation before any selected item other than `prepare`. For parallel gates, invoke their domain runners only after the single preparation run has passed.

Style and Architecture do not wait for UT, IT, E2E, or each other. Run them concurrently after preparation using the host's native process mechanism. Do not hide a failure behind a combined pipeline status. If preparation fails, report the preparation failure and do not start the other runners.

Before reporting a failure, read the nearest `index.md` and print:

```text
FAIL: verify/<domain>
Intent: <why this verification exists, from index.md>
Violated: <rule, expected behavior, stable test name, or runner assertion>
Command: ./verify/<domain>/run.sh
Evidence:
<captured output>
```

Use the failing check's own rule identifier, assertion, test name, or runner message for `Violated`. Never invent a rule. If none is available, use `Violated: <domain> verification failed` and retain the raw output. For a requested state, also print `Expected` and `Observed`.

## Cycle

Repeat until accepted, blocked, or the maximum is reached.

### 1. Inspect current state — dispatch a read-only scout

Give a scout the target, acceptance condition, project, current diff, requested level, and available evidence. Require it to:

- inspect the implementation and relevant callers;
- run `verify/prepare/run.sh` first and only start the requested verification runners after it passes;
- run the verification interface at the requested level;
- compare observed behavior with the acceptance condition;
- report changed files, exact failures, each failure's intent and violated rule, risks, and evidence;
- make no edits and delegate no further work.

If `verify/`, `verify/prepare/`, or a required runner is missing, report **BLOCKED** and recommend `verify-design`; do not silently run unrelated commands as a substitute.

### 2. Analyze the gap — main orchestrator

Classify the current state as:

- **Accepted candidate:** the acceptance condition is met and current verification evidence is sufficient;
- **Gap:** a concrete mismatch remains;
- **Blocked:** evidence is missing, the requirement is ambiguous, a runner cannot execute, or a human-owned decision is required.

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
- run the smallest relevant verification after editing;
- report changed files, commands, results, residual risks, and unresolved gaps;
- stop rather than guess if the strategy is insufficient or requirements conflict.

The worker may edit; `verify-loop` itself does not directly implement the gap. Do not accept the worker's claim without reviewing its diff and evidence.

### 4. Verify and judge the attempt

Run the verification interface again at the requested level. Inspect the current diff and compare current evidence with the acceptance condition.

Judge one of:

- **ACCEPT:** acceptance is met, all selected verification gates pass, and no blocking regression or unresolved risk contradicts the target;
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
- The resolver depends on inspection and root-cause analysis.
- Preparation is mandatory and completes before any other runner; functional verification is ordered `ut → it → e2e`; Style and Architecture are independent parallel gates.
- Do not dispatch a resolver for an accepted candidate or unsupported root cause.
- Failed resolver attempts are rolled back before retry; do not silently keep partial fixes.
- Stop for ambiguity, contradictory requirements, unsafe rollback, destructive/security-sensitive changes without authority, unavailable credentials, or a human-owned decision.
- Never claim success when the loop stops at its maximum or a blocker.

## Output

Return all progress in the current session; do not create a report file unless requested.

```markdown
# Verify Loop

- Target: [requested outcome]
- Acceptance: [observable condition]
- Project: [path]
- Maximum functional level: [ut | it | e2e]
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
