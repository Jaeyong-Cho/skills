---
name: req-ood-tdd
description: Orchestrate the full prototype → requirements → OOD → TDD-plan → implementation → review → commit → merge → release workflow, with one requirement document, one design document, and one plan per vertical slice.
disable-model-invocation: true
---

# Prototype → Requirements → OOD → TDD → Ship

Run one product goal through the complete development workflow. This skill is a coordinator: it calls the existing skills and preserves their rules. It does not replace `/skill:req`, `/skill:ood`, `/skill:tdd`, `/skill:to-plan`, or `/skill:do-plan` with a second process.

The workflow may produce several vertical slices, but every slice is specified, designed, planned, implemented, reviewed, and shipped independently. Never turn a vertical slice into a horizontal layer plan.

## References

Load these at the stage where they apply:

- Prototype discovery: `../references/prototype.md` and, for unresolved questions, `../references/top-down-decompose.md`.
- Requirement documents: `../references/requirement-engineering.md`, `../references/spec-convention.md`, `../references/document-style.md`, `../references/document-style/frontmatter.md`.
- Object-oriented design: `../references/abstraction-levels.md`, `../references/deep-modules.md`, and `../references/meta-pattern.md`.
- TDD and validation: `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`, `../references/tdd-refactoring.md`, `../references/deterministic-evaluation.md`, and `../references/test-loop.md`.
- Human checkpoints: `../references/question-format.md`.

## Artifact map

Reuse the target repository's existing convention first. If it has none, use this layout:

| Artifact | Default location | Rule |
|---|---|---|
| Prototype | Beside the relevant module/page, clearly disposable | Happy path only; no production dependency on it. Keep it on a throwaway branch. |
| Requirement inventory | `spec/index.md` and `spec/<epic>/index.md` | Lists every discovered slice and links each written Story. Keep not-yet-specified candidates visible. |
| Requirement | `spec/<epic>/<slice>.md` | One vertical slice: happy path plus its concrete, directly relevant edge, boundary, and failure cases. Follow `template/spec.md`. |
| OOD design | `design/<epic>/<slice>.md` | One approved design-and-contract brief per requirement. |
| TDD implementation plan | `plans/<nn>-<slice>.md` | One independently executable plan per vertical slice. |
| Execution report | `plans/<nn>-<slice>.report.md` | Written by `/skill:do-plan`; records evidence and any blocked work. |

Use the target's existing names when they differ. Do not create parallel copies of an existing spec, design, or plan system. Every document must have an exact path, stable slice slug, and links to its upstream and downstream artifacts.

## State and gates

Keep these fields as workflow state throughout the run:

- prototype branch and verdict;
- approved candidate slice list and order;
- requirement, design, plan, report, test, commit, merge, and release paths for every slice;
- confirmed scope, exclusions, deferred topics, assumptions, and unresolved risks.

Silence is not approval. Stop at every human-owned gate. Use `../references/question-format.md` for any question this coordinator asks directly; the delegated skills keep their own checkpoints.

## Pipeline

### 0. Establish the target

1. Read repository instructions, the existing spec/index chain, relevant source and tests, branch policy, build command, unit-test command, integration/e2e command, and release convention.
2. Check for unrelated uncommitted changes. Do not overwrite or include them.
3. Name the product goal, target epic, slice slug convention, and the prototype question. Inspect only context needed for that goal.

**Completion criterion:** the target repository, artifact convention, baseline commands, branch policy, and one product goal are known; unrelated changes are protected.

### 1. Prototype the happy path

1. Follow `../references/prototype.md`. Choose the logic/state or UI branch and build the smallest runnable, throwaway prototype for the happy path.
2. Make it trivial to run, keep state visible, and avoid persistence, production abstractions, and tests unless the question itself requires them.
3. Run the prototype. Use trial and error to expose confusing states, missing inputs, and observable outcomes. Record the verdict, evidence, open questions, and discarded ideas in the workflow context. Use `/skill:experiment` when an unresolved question needs a separate executable experiment.
4. Commit the prototype only to a clearly named throwaway branch and record that branch in the context. Do not merge prototype code into the production branch.
5. Ask the human whether the prototype verdict is sufficient to discover requirements. If not, revise only the prototype and repeat this stage.

**Completion criterion:** the happy path runs, its relevant state/output is visible, the prototype verdict is recorded with evidence, and no prototype code is treated as production code.

### 2. Discover the vertical-slice list

1. From the prototype, context, trial results, and repository evidence, use `../references/top-down-decompose.md` to build a mutually exclusive, collectively exhaustive candidate list.
2. Each candidate must name one actor, trigger, user-visible outcome, execution boundary, and dependency. Split by behavior/outcome, not by UI/backend/database layer.
3. For each candidate, list only concrete edge, boundary, alternate, and failure cases that belong to the same outcome. Mark each case `in scope`, `out of scope`, or `deferred with a condition`.
4. Order the candidates by dependency and user value. Keep unknowns as explicit understand-nodes or experiments; do not guess around a blocking unknown.
5. Present the list for human approval before writing detailed requirement documents. Once approved, create or update the target's requirement inventory and its indexes.

**Completion criterion:** every candidate has one coherent outcome and boundary, candidates do not overlap, the list has no unexplained gap, every listed edge case has a concrete trigger and disposition, and the human approved the order and scope.

### 3. Specify and write one requirement per slice

Run `/skill:req` once with the complete approved candidate inventory, prototype verdict, context, and repository evidence. It processes slices in dependency order, validates their boundaries as a batch, and writes one requirement document for every approved slice. Do not invoke `/skill:req` once per candidate.

The requirement stage must:

1. Keep every slice to one happy path plus its directly relevant edge, boundary, alternate, and failure cases.
2. Require Given–When–Then acceptance criteria with a category and deterministic Verification Method for every in-scope case, per `../references/requirement-engineering.md`.
3. Stop at the batch approval gate before writing any requirement document.
4. Write each approved card as `spec/<epic>/<slice>.md` or the repository's equivalent. Follow `template/spec.md`, add required metadata, preserve accepted edge-case decisions, and update `spec/<epic>/index.md` and `spec/index.md` in the same change.
5. If one slice changes, update the inventory and dependency order, then reapprove the affected batch. Do not silently absorb a sibling feature.

**Completion criterion:** `/skill:req` returns one approved requirement inventory and exactly one requirement document per approved slice; each document contains its actor, trigger, outcome, scope, exclusions, preconditions, happy path, concrete relevant edge/failure cases, Given–When–Then acceptance criteria, and a deterministic verification path; both indexes link to every document.

### 4. Design one OOD solution per requirement

Run `/skill:ood` once with the complete requirement inventory and all approved requirement documents. It designs slices in dependency order, checks shared boundaries across the batch, and writes one design document for every requirement. Do not invoke `/skill:ood` once per requirement.

The OOD stage must:

1. Follow its full sequence for every slice: Requirements → Domain Model → Responsibilities → Data Model → APIs → Workflow → Edge Cases → Failure Modes → Trade-offs.
2. Design the smallest coherent vertical slice, identifying the user-facing boundary and every applicable internal boundary. Apply `../references/abstraction-levels.md` and `../references/deep-modules.md`; do not invent layers or abstractions without a real boundary.
3. Trace every acceptance criterion and in-scope edge case to an Object, Interface, observable behavior, and verification. Preserve exclusions and deferred topics.
4. Stop at the batch design approval gate. After approval, write one design brief to `design/<epic>/<slice>.md` or the repository's equivalent for every slice. Do not write production code or feature tests in this stage.

**Completion criterion:** `/skill:ood` returns one approved design inventory and exactly one design document per requirement; each document reaches the real external boundary, owns every in-scope rule, defines interfaces and failures, traces every acceptance criterion, and contains no unapproved implementation.

### 5. Write one TDD plan per vertical slice

For each requirement/design pair:

1. Run `/skill:to-plan` with the exact requirement document, design document, context, and repository evidence. Do not combine slices.
2. Write exactly one independently executable plan file at `plans/<nn>-<slice>.md` or the repository's equivalent. The plan must include the acceptance-criteria table, real Verification Method paths, QA Procedure, deferred items, uncertainty assertions, branch/worktree, build command, unit and integration/e2e commands, dogfood test, commit message, and human merge/release gates. Record merge/release as gates, not per-slice implementation action items; the coordinator handles aggregate merge/release after all slices.
3. Tag changed functions with `[L1]`, `[L2]`, or `[L3]` and list their TDD work in dependency order. Follow the Testing by level rules in `../references/abstraction-levels.md`.
4. Include a code-review gate after implementation and validation but before commit. The default reviewer is `/skill:thermo-nuclear-code-quality-review`; use a repository-specific review skill when one exists.
5. Confirm the plan path and contents through `/skill:to-plan` before execution.

**Completion criterion:** every requirement/design pair has one plan, no plan contains a second slice, each acceptance criterion names a real deterministic check, and every implementation/review/commit/merge/release action is executable without guessing.

### 6. Execute each plan

Run `/skill:do-plan` once per plan, in dependency order.

- Let `/skill:do-plan` create and use the plan's worktree before implementation.
- Execute every unchecked item in order. For each behavior, use `/skill:tdd` with one approved acceptance criterion, or follow that skill's exact RED → GREEN → REFACTOR rules inside the plan item; never bulk-write tests before implementation. The plan's deterministic test must pass before its item is checked off.
- Write production code and tests only in the plan worktree. Validate focused tests, relevant regression tests, build, integration/e2e checks, and the plan's QA Procedure.
- Stop for ambiguous scope, missing verification, failed prerequisites, or changed requirements. Return to the affected requirement/design/plan stage instead of patching around the problem.
- `/skill:do-plan` must run the code-review gate before committing. Do not accept a review that only says the tests pass.

**Completion criterion:** every plan action is checked or explicitly blocked, every acceptance criterion has pass/fail evidence, the build and required test commands pass, the dogfood check is recorded, and no code is committed before review.

### 7. Review and commit

`/skill:do-plan` owns the per-slice review-before-commit gate. For each plan:

1. Require its report to include the review result, `git diff --check`, blocking/non-blocking findings, residual risks, staged-file list, and test evidence.
2. If a blocker remains, return to the affected requirement, design, or TDD step. A behavior change reopens the relevant human approval gate; a structure-only change stays in TDD REFACTOR.
3. Let `/skill:do-plan` ask for human commit confirmation and record the resulting hash. Do not commit a slice outside that gate.

**Completion criterion:** every slice has a clean or explicitly accepted review, green checks after fixes, a staged diff containing only that slice, a human-confirmed commit, and a recorded hash.

### 8. Merge and release

1. After all slice commits are reviewed, run the aggregate build, unit, integration/e2e, and release-readiness checks on the integration branch. Re-run the code review against the combined change when slices interact.
2. Follow the repository's branch policy. If it uses the `project-setup` convention, work branches merge into `develop` and releases merge `develop` into `main`; otherwise use the existing policy. Never invent merge or release commands.
3. Show the merge target, commits, validation evidence, and release notes/tag/version change. Ask the human to confirm before merging.
4. Ask separately for release confirmation. Only then run the repository's documented release action. Record the release identifier and evidence. Remove merged worktrees and run `git worktree prune` after the human confirms the merge.

**Completion criterion:** the intended integration branch contains all reviewed slice commits, aggregate validation passes, the human confirmed merge and release separately, and the release identifier/evidence is recorded. A blocked confirmation leaves the corresponding item open; it is not reported as done.

## Change-control rules

- A prototype is disposable evidence, not a production shortcut.
- A requirement, behavior, or scope change after design returns to `/skill:req` first, then `/skill:ood`; a design-only change returns to `/skill:ood`.
- A design change after approval requires design approval again before code changes.
- A review finding that changes observable behavior reopens the requirement/design gate; a structure-only fix stays in TDD REFACTOR.
- Keep deferred topics deferred unless the human starts a new slice.
- Never merge, release, or claim completion without the required human confirmation and command evidence.

## Final report

Report one row per slice:

| Slice | Requirement | Design | Plan/report | Tests/build | Review | Commit | Merge/release |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

Also report prototype verdict/branch, deferred topics, residual risks, blocked gates, and the next safe action. Use the report produced by `/skill:do-plan` as execution evidence rather than paraphrasing test results.

## Completion criterion

The workflow is complete only when the happy-path prototype verdict is recorded, the approved vertical-slice inventory is complete, every slice has a requirement document with concrete edge cases, an approved OOD document, and one TDD plan, every plan has executed with code/tests/validation and review evidence, commits were human-confirmed, and merge/release were separately human-confirmed with recorded evidence. No unapproved scope or untracked slice remains.
