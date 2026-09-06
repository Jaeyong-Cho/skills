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

Launch exactly one fresh, read-only `stage-reviewer` sub-agent with this task:

- Stage: TDD implementation.
- Personas: TDD Practitioner, Clean Code Reviewer, Tester, Maintainer, and Simplifier as primary; Domain Expert as supporting; Security Reviewer or Performance/SRE only when materially relevant.
- Artifacts: requirement and OOD paths/content, the complete relevant `git diff --` output, changed paths, and test commands/results. Capture the diff before launching the child and include it in the task; the read-only reviewer has no shell or edit tools.
- Scope: verify observable behavior, meaningful edge/failure coverage, refactoring safety, clarity, maintainability, and feedback to OOD/requirements. Report only concrete findings in the current implementation.
- Output: use the shared finding format and end with Must fix, Should improve, Deliberately deferred, and `Verdict: BLOCK | PROCEED`.

Use the `subagent` tool through a `workflowScript`, with `agent: "stage-reviewer"`, `context: "fresh"`, and no write tools or edits. The workflow body must await the child (`const result = await runs.run("stage-review", {...}); return result.output;`). Launch the workflow asynchronously, then wait for its completion result before declaring the TDD cycle complete; do not continue while it is still detached. If `stage-reviewer` is unavailable, stop and report that `./install.sh` must install `npm:pi-subagents` and the custom agent.

## Parent disposition

Merge duplicate findings. Classify the result as:

1. **Must fix before proceeding** — behavior defects, broken contracts, unsafe failure handling, misleading tests, or material maintainability damage.
2. **Should improve without blocking** — worthwhile cleanup that does not invalidate the slice.
3. **Deliberately deferred** — product/design questions for `/skill:req` or `/skill:ood`, and risk concerns outside the current behavior.

Apply blocking fixes in the parent, then rerun the focused and relevant regression tests. Do not let the reviewer add speculative behavior or rewrite a sound test merely to satisfy a preference.

## Completion criterion

Red was observed for the intended missing behavior, Green and regression tests pass, refactoring preserves the contract, tests exercise observable behavior and meaningful risks, the diff is in scope, and every blocking review finding is resolved or explicitly accepted.
