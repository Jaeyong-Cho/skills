---
name: tdd
description: Execute approved requirement and OOD slices through deterministic RED → GREEN → REFACTOR cycles, one behavior at a time, and report the code/test evidence per slice. Use after OOD and its TDD plan.
disable-model-invocation: true
---

# TDD

Execute the complete approved vertical-slice batch without changing its scope. A batch may contain one slice. Work in dependency order and never replace vertical cycles with a horizontal "write all tests, then all code" pass.

```text
approved slice + acceptance criterion
              ↓
RED: test fails for the missing behavior
              ↓
GREEN: smallest implementation passes
              ↓
REFACTOR: structure improves while behavior stays green
              ↓
next criterion / next slice
```

`/skill:to-plan` writes the implementation plans. This skill executes their behavior cycles; `/skill:do-plan` coordinates the plan actions, validation, review, and commit gate.

## Input

- One or more approved requirement documents and their acceptance criteria
- The corresponding approved OOD design documents, including each primary public boundary and internal Interfaces
- One TDD implementation plan per slice, or the selected plan action when running as a single-slice substep
- Repository code, tests, commands, and conventions

## Output

For every processed slice:

- one deterministic behavior test per completed cycle;
- the smallest production change that makes each test pass;
- justified behavior-preserving refactors only;
- focused, regression, build, and integration/e2e results;
- changed paths, verified RED failures, final Green results, residual risks, and blocked criteria.

## Batch rules

- Process slices in the plan's dependency order. Do not implement a dependent slice when its prerequisite is blocked.
- Process one acceptance criterion at a time within a slice.
- Test observable behavior through the primary public contract from OOD, not private helpers or implementation details. Use internal tests only as support.
- Prefer the cheapest test that cannot lie: unit for pure domain logic, integration for a real component boundary, E2E for a user-visible flow.
- Use deterministic fixtures and isolated state. Mock only external system boundaries.
- Do not write production behavior during RED.
- Do not weaken or rewrite a test merely to make GREEN pass.
- Implement only what the requirement, design, and current test require. Do not implement deferred topics or future slices.
- Refactor only while all relevant tests are green. Never add behavior or speculative abstractions during REFACTOR.
- Preserve validation, errors, side effects, responsibility ownership, dependency direction, and the OOD contract.

Read `../references/tdd.md`, `../references/tdd-tests.md`, and the Testing by level section of `../references/abstraction-levels.md`. Read `../references/tdd-mocking.md` when a behavior crosses an external boundary. Before REFACTOR, read `../references/tdd-refactoring.md` and `../references/deep-modules.md`.

## Human checkpoint

Before the first edit, show one cycle matrix for the batch:

| Slice | Acceptance criterion | Public boundary | Test path | Production path |
|---|---|---|---|---|
| [slice] | [criterion] | [boundary] | [path] | [path] |

State each scenario as:

> Given [starting state], when [action], then [observable result].

Ask once for confirmation of the matrix. Do not start a later slice while the batch is awaiting approval. Ask another focused question only if a criterion conflicts with its requirement/design contract or two implementations would produce different observable behavior.

**Completion criterion:** the human confirmed the ordered cycle matrix, or the batch is explicitly blocked with the missing decision named.

## Workflow

### 1. Validate the batch

1. Confirm every slice has exactly one approved requirement, design, and plan path.
2. Confirm each acceptance criterion has a public boundary, test level, fixture, and expected observable result.
3. Confirm the repository's focused, regression, build, and integration/e2e commands.
4. Confirm no dependency is being implemented after a dependent slice.

If an input is missing or contradicts another artifact, stop before editing and return to `/skill:req`, `/skill:ood`, or `/skill:to-plan` as appropriate.

**Completion criterion:** all selected cycles have a coherent requirement/design/plan trace and executable verification commands.

### 2. RED → GREEN → REFACTOR for each criterion

For each slice, then each acceptance criterion:

#### RED — prove the gap

1. Find the repository test convention and choose the appropriate abstraction level.
2. Add the smallest test for this criterion through the public contract.
3. Run the focused test.
4. Confirm it fails specifically because the required behavior is missing.
   - If it already passes, stop and determine whether the behavior already exists or the test is ineffective.
   - If setup or contract errors cause the failure, repair test setup without adding production behavior and rerun it.

Do not continue until RED is verified or the criterion is explicitly recorded as already implemented and removed from the plan by an approved scope decision.

#### GREEN — make it pass

1. Re-run the focused test and inspect its failure.
2. Trace the smallest production path from the public contract to the missing behavior.
3. Implement the minimal correct change without anticipating future criteria.
4. Run the focused test until it passes.
5. Run the relevant existing regression subset.

Do not continue until the focused and relevant regression tests are green.

#### REFACTOR — improve safely

1. Identify one concrete smell in the changed code: unclear naming, duplicated logic, mixed responsibility, leaky boundary, or unnecessary complexity.
2. If there is no concrete improvement, skip refactoring; green code does not require churn.
3. Otherwise make one smallest structural improvement at a time and rerun the focused test after each meaningful change.
4. Run the relevant regression tests again.
5. Stop when the code is clear enough and the contract is unchanged.

**Completion criterion:** this criterion has observed RED, focused GREEN, regression GREEN, and either a recorded refactor or a reason to skip it before the next criterion begins.

### 3. Validate each slice and the batch

After each slice:

- run its focused and relevant regression tests;
- run its build and integration/e2e checks required by its plan;
- verify every acceptance criterion and its named Verification Method;
- record changed production/test paths, evidence, failures, and residual risks.

After all unblocked slices:

- run the aggregate build, unit, integration/e2e, and deterministic test commands;
- confirm no deferred topic or unrelated file entered the diff;
- hand the per-slice evidence to `/skill:do-plan` for its review-before-commit gate.

If a slice fails, stop dependent slices. Independent slices may continue only when the plan explicitly permits it and their tests cannot observe the blocked slice.

**Completion criterion:** every completed slice has criterion-level RED/GREEN/REFACTOR evidence, required regression/build/integration results, and an explicit pass or blocked status; the aggregate validation result is recorded.

## Change control

- If behavior or scope changes, stop and return to `/skill:req` before changing code.
- If a boundary, Object, responsibility, or Interface changes, return to `/skill:ood` and obtain design approval again.
- If only structure changes after GREEN, keep it inside REFACTOR and rerun tests.
- Never implement a deferred topic because it is convenient while the batch is open.

## Completion criterion

TDD is complete only when every unblocked selected slice has executed one RED → GREEN → REFACTOR cycle per approved criterion, no test was weakened, focused and regression tests are green, required build/integration/e2e checks pass, blocked dependencies are recorded, and the complete evidence set is ready for code review.
