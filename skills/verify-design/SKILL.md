---
name: verify-design
description: Design and validate a project's verify/ interface by reusing native tests, linters, builds, and architecture checks; use when a project needs discoverable verification or a new feature/bug check must expose a current gap.
disable-model-invocation: true
license: MIT
---

# Verify Design

Make a project's proof of correctness discoverable, executable, and honest. Read [`../references/verification-structure.md`](../references/verification-structure.md) before changing anything.

Do not impose a testing framework. Reuse existing mechanisms, then reference them, wrap them, extend them, and create new verification only when necessary.

## Inputs

Accept:

- **Project:** repository or component to inspect and change.
- **Requested behavior:** optional new feature, bug, or other expected state that is not true in the current state.
- **Level:** optional maximum functional level: `ut`, `it`, or `e2e`; default `ut`.
- **Evidence:** existing commands, failures, logs, or acceptance criteria.

If the requested behavior is absent or ambiguous, inspect the project first. Do not invent an expected state.

## Procedure

### 1. Inspect and classify

Find the project's native tests, linters, static analysis, build commands, continuous-integration commands, architecture checks, and existing verification. Classify each as UT, IT, E2E, Style, or Architecture. Record the native command and its source location.

Completion criterion: every discovered relevant mechanism is classified, or explicitly recorded as unavailable; no test is moved or duplicated merely for this interface.

### 2. Build the interface

Create or adapt this project-level shape:

```text
verify/
├── index.md
├── run.sh
├── ut/{index.md,run.sh}
├── it/{index.md,run.sh}
├── e2e/{index.md,run.sh}
├── style/{index.md,run.sh}
└── archi/{index.md,run.sh}
```

For each runner, invoke the existing native mechanism. Keep adapters small. If a domain has no applicable check, document that fact in its index and make its runner return success; do not pretend a missing check proves behavior. Make every runner executable.

Every directory added below `verify/` gets a local `index.md`. Each index describes its purpose, every direct child directory, and every relevant direct child file with a short description. Keep indexes local; do not copy the whole subtree into ancestors.

Completion criterion: the required directories, runners, and indexes exist; runners execute native checks or explicitly document no applicable check; every index entry points to an existing direct child and has a description.

### 3. Add a red check for a requested new state

When the human requests a new feature, bug fix, regression check, or any expected state that is not the current state, add the smallest native check that expresses the expected behavior. Prefer a focused test or deterministic style/architecture check over a new framework.

Run the relevant verification level. A failure is expected evidence, not an implementation failure:

```text
GAP
Intent: why this check exists
Expected: requested behavior or invariant
Observed: current behavior and failure output
Violated: stable test/rule name, or the relevant domain rule
Next: implementation must make the check pass
```

Do not implement the requested feature in this skill. If the new check passes immediately, report that no current gap was observed. If the project cannot express the check with its native mechanisms, stop and report the blocker instead of creating speculative infrastructure.

### 4. Lint the structure

Run the bundled deterministic linter from the skill directory:

```bash
./tools/lint-verify-structure [project]
```

It checks required directories and runners, indexes, local links, descriptions, stale/out-of-scope references, and unexplained depth. Fix structural failures and rerun it. A depth warning may remain only with a documented reason.

Completion criterion: the linter passes with no structural errors and its output is retained as evidence.

### 5. Run the verification loop

Invoke `@skills/verify-loop` at the requested maximum level. Pass it the project, requested behavior, the new check (if any), the linter result, and all native command evidence. `verify-loop` owns ordered functional execution, independent Style/Architecture gates, intent output, and the final pass/fail judgment.

## Output

Return the result in the current session; do not create a report unless requested:

```markdown
# Verify Design

- Project: [path]
- Requested state: [behavior, or `existing state only`]

## Existing mechanisms
- [domain] — [native command and source]

## Interface
- [created, adapted, or already present paths]

## Gap
- Intent: [why the check exists]
- Expected: [requested behavior]
- Observed: [current result]
- Violated: [rule/check]
- Evidence: [command and output]

## Validation
- Structure linter: [pass/fail]
- Verify loop: [pass/fail/stopped]

## Residual risks
- [risk, or `None`]
```

The skill is complete only when the interface is locally indexed, native mechanisms are reused or explicitly unavailable, the structure linter passes, and `verify-loop` returns current evidence. For a new requested state, completion also requires a focused check and an explicit GAP when the current state fails it.
