---
name: tdd-review
description: Incrementally review one TDD implementation checkpoint as tests, behavior, production code, and refactoring.
disable-model-invocation: true
---

# TDD Implementation Review

Review one meaningful TDD checkpoint after Red → Green → Refactor. Read `../references/stage-review.md` first.

## Input

- The approved requirement and OOD contract.
- The current working-tree diff, captured with `git diff --`, and changed tests/production files.
- Test results and the checkpoint that triggered review.

Inspect the supplied diff and changed files directly. Review tests and production code together; do not turn this into a test-count or coverage exercise.

## Review step

Launch one workflowScript that fans out **one fresh, read-only `stage-reviewer` child per applicable persona**:

- Stage: TDD implementation; Persona: TDD Practitioner (primary).
- Stage: TDD implementation; Persona: Clean Code Reviewer (primary).
- Stage: TDD implementation; Persona: Tester (primary).
- Stage: TDD implementation; Persona: Maintainer (primary).
- Stage: TDD implementation; Persona: Simplifier (primary).
- Stage: TDD implementation; Persona: Domain Expert (supporting).
- Stage: TDD implementation; Persona: Security Reviewer only when materially relevant.
- Stage: TDD implementation; Persona: Performance/SRE only when materially relevant.

Each child receives the requirement and OOD paths/content, the complete relevant `git diff --` output, changed paths, and test commands/results. Capture the diff before launching the children. Each child inspects only its assigned persona and reports only concrete findings in the current implementation. Do not send all personas to one reviewer; the independent contexts are the point of this review.

Use the `subagent` tool through one `workflowScript` with `runs.all([...])`; every child uses `agent: "stage-reviewer"`, `context: "fresh"`, and no write tools or edits. The workflow must await all children and return clearly labelled persona reports. The parent is the aggregator: merge duplicate findings, preserve the responsible persona, and classify the combined result. Launch the workflow asynchronously, then wait for its completion result before declaring the TDD cycle complete; do not continue while it is still detached. If `stage-reviewer` is unavailable, stop and report that `./install.sh` must install `npm:pi-subagents` and the custom agent.

## Parent disposition

Merge duplicate findings. Classify the result as:

1. **Must fix before proceeding** — behavior defects, broken contracts, unsafe failure handling, misleading tests, or material maintainability damage.
2. **Should improve without blocking** — worthwhile cleanup that does not invalidate the slice.
3. **Deliberately deferred** — product/design questions for `/skill:req` or `/skill:ood`, and risk concerns outside the current behavior.

Apply blocking fixes in the parent, then rerun the focused and relevant regression tests. Do not let the reviewer add speculative behavior or rewrite a sound test merely to satisfy a preference.

## Completion criterion

Red was observed for the intended missing behavior, Green and regression tests pass, refactoring preserves the contract, tests exercise observable behavior and meaningful risks, the diff is in scope, and every blocking review finding is resolved or explicitly accepted.
