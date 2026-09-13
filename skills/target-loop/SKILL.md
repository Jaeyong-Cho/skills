---
name: target-loop
description: Repeatedly inspect, resolve, and verify a user-specified target by dispatching subagents. Use when work should continue until its acceptance condition is met, with a default maximum of three cycles.
disable-model-invocation: true
license: MIT
---

# Target Loop

Drive one concrete target to an evidence-backed acceptance decision. The main orchestrator owns the target, gap analysis, strategy, and final judgment. Subagents inspect and implement; they do not decide whether the target is accepted.

Do not create a report file unless the user asks. Return progress in the current session.

## Rule-building prerequisite

If the user is defining, changing, or extending these loop rules, **MUST run `@skills/grill-me` first**. Do not choose rules, write skill instructions, or implement the loop until grill-me reaches shared understanding and the user confirms it.

## Inputs

Accept:

- **Target:** the requested outcome and its acceptance condition.
- **Workdir:** repository or component to inspect and change.
- **Evidence:** existing test results, linter output, logs, diff, issue, or current behavior.
- **Maximum cycles:** a user-supplied positive integer such as `max cycles: 5`; default `3`.

If the target or its acceptance condition is not concrete enough to judge, ask for clarification before dispatching work. Do not turn a vague request into an invented definition of done.

## Cycle

Repeat until accepted or the maximum is reached.

### 1. Inspect current state — dispatch a subagent

Dispatch a read-only scout subagent through the active host's native mechanism. Give it the exact target, acceptance condition, workdir, current diff, and available evidence.

Require it to:

- inspect the current implementation and relevant callers;
- run the relevant existing checks: tests, linter, type checker, build, or other target-specific checks;
- compare observed behavior with the acceptance condition;
- report exact gaps, failed commands, changed files, risks, and evidence;
- make no edits and delegate no further work.

Never treat dispatch or a child exit alone as evidence. Review the returned result before deciding the next action.

### 2. Find the gap and choose a strategy — main orchestrator

Classify the target as:

- **Accepted candidate:** the acceptance condition is already met and current evidence is sufficient;
- **Gap:** a concrete mismatch remains;
- **Blocked:** missing evidence, ambiguity, external dependency, unsafe change, or a human-owned decision prevents resolution.

For a Gap, choose exactly one smallest safe resolution strategy for this cycle. State the gap, cause, intended change, scope, and check that will prove it. Do not dispatch a resolver for a guessed or unsupported gap.

If the target is an Accepted candidate, proceed to the review/judgment step without changing files. If Blocked, stop and report what the human or environment must provide.

### 3. Resolve the gap — dispatch a subagent

Dispatch a worker subagent through the active host's native mechanism. Pass the target, acceptance condition, inspected evidence, and the single approved strategy.

Require it to:

- change only the scoped implementation, tests, configuration, or documentation needed for that strategy;
- preserve unrelated behavior and avoid speculative refactors;
- run the smallest relevant checks after editing;
- report changed files, commands, results, residual risks, and any unresolved gap;
- stop rather than guess if the strategy is insufficient or requirements conflict.

Do not accept a worker's claim of success without inspecting its evidence.

### 4. Review and judge — main orchestrator

Inspect the current diff and the resolver's evidence against the target. Run or rerun the decisive checks when the child evidence is incomplete, stale, or not directly observable.

Judge one of:

- **ACCEPT:** the acceptance condition is met, relevant checks pass, and no blocking regression or unresolved risk contradicts the target;
- **CONTINUE:** a concrete gap remains and another cycle is available;
- **STOP:** the maximum is reached, evidence is missing, the change is unsafe, or a human decision is required.

A passing test alone is not acceptance unless it observes the target. A clean diff alone is not acceptance. If the review finds a new or changed gap, use it as the next cycle's input and invalidate stale evidence.

After `ACCEPT`, stop immediately. Do not spend remaining cycles on optional cleanup.

## Controls

- Default maximum: **3 cycles**.
- Honor a user-specified maximum exactly; reject zero, negative, or non-integer values.
- One inspect subagent and at most one resolver subagent per cycle.
- The resolver depends on the inspect result; do not dispatch it in parallel with inspection.
- Do not dispatch a resolver when inspection finds no gap.
- Stop for ambiguity, contradictory requirements, destructive/security-sensitive changes without authority, unavailable required credentials, or a human-owned decision.
- Never claim success when the loop stops at its maximum or a blocker.

## Output

Use this structure:

```markdown
# Target Loop

- Target: [requested outcome]
- Acceptance: [observable condition]
- Maximum cycles: [number]

## Cycle [n]

### State evidence
- [commands and observed results]
- [current gap or `None`]

### Strategy
- [chosen resolution, or why no resolver was needed]

### Resolution
- [subagent, changed files, checks, results]

### Judgment
- **[ACCEPT | CONTINUE | STOP]** — [evidence and reason]

## Final status
[Accepted | Stopped at maximum | Blocked | Needs human decision]

## Residual risks
- [risk, or `None`]
```

The loop is complete only when the final judgment is supported by current evidence, every dispatched child result was reviewed, and the status clearly distinguishes acceptance from maximum-cycle or blocker termination.
