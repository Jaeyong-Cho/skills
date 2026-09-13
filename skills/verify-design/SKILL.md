---
name: verify-design
description: Design and validate a project's verify/ interface by reusing native tests, linters, builds, and architecture checks; use when a project needs discoverable verification or a new feature/bug check must expose a current gap.
disable-model-invocation: true
license: MIT
---

# Verify Design

Make a project's proof of correctness discoverable, executable, and honest. Read [`../references/verification-structure.md`](../references/verification-structure.md) and [`../references/deterministic-evaluation.md`](../references/deterministic-evaluation.md) before changing anything.

Do not impose a testing framework. Reuse existing mechanisms, then reference them, wrap them, extend them, and create new verification only when necessary.

## Procedure

### 1. Establish shared intent

Before inspecting or changing the project, **MUST RUN** a session of `@skills/grill-me` in the current conversation. Give it the request, project, level, evidence, and [`../references/intent-checklist.md`](../references/intent-checklist.md). It must cover every intent-checklist point, follow its calibration, impact, uncertainty, and round rules, and finish with a teach-back and explicit confirmation of shared understanding. Do not begin design work until the human confirms that understanding. Do not create an intent file unless the human separately asks for persistence.

### 2. Inspect and classify

Find the project's native tests, linters, static analysis, build commands, continuous-integration commands, architecture checks, and existing verification. Classify each as UT, IT, E2E, Style, or Architecture. Record the native command, source location, and deterministic pass signal.

Completion criterion: every discovered relevant mechanism is classified, or explicitly recorded as unavailable; no test is moved or duplicated merely for this interface.

### 3. Build the interface

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

### 4. Add a red check for a requested new state

When the human requests a new feature, bug fix, regression check, or any expected state that is not the current state, add the smallest native check that expresses the expected behavior. Prefer a focused test or deterministic style/architecture check over a new framework.

Before running each check, define a verification method for every relevant mechanism, requested state, or acceptance criterion:

- **Type:** the lowest sufficient UT, IT, E2E, Style, or Architecture check.
- **Location:** the existing or new test/check path.
- **Command:** the exact command to run it.
- **Pass signal:** the exact observable result, such as a named assertion, returned value, database row, HTTP status, or zero exit status for a structural check; never "looks right."

Run the relevant verification level and record that method with its current evidence. A failure is expected evidence, not an implementation failure:

```text
GAP
Intent: why this check exists
Expected: requested behavior or invariant
Observed: current behavior and failure output
Violated: stable test/rule name, or the relevant domain rule
Next: implementation must make the check pass
```

Do not implement the requested feature in this skill. If the new check passes immediately, report that no current gap was observed. If the project cannot express the check with its native mechanisms, stop and report the blocker instead of creating speculative infrastructure.

### 5. Lint the structure

Run the bundled deterministic linter from the skill directory:

```bash
./tools/lint-verify-structure [project]
```

It checks required directories and runners, indexes, local links, descriptions, stale/out-of-scope references, and unexplained depth. Fix structural failures and rerun it. A depth warning may remain only with a documented reason.

Completion criterion: the linter passes with no structural errors and its output is retained as evidence.

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

## Verification method
| State, mechanism, or acceptance criterion | Type | Check path | Command | Observable pass signal |
|---|---|---|---|---|
| [state] | [UT/IT/E2E/Style/Architecture] | [path] | `[command]` | [exact result] |

## Validation
- Structure linter: [pass/fail]
- Verification methods: [defined and run / blocked]

## Residual risks
- [risk, or `None`]
```

The skill is complete only when the interface is locally indexed, native mechanisms are reused or explicitly unavailable, every requested state has a deterministic verification method with current evidence, and the structure linter passes. For a new requested state, completion also requires a focused check and an explicit GAP when the current state fails it.
