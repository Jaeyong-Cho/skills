---
name: tdd
description: "Run one complete RED → GREEN → REFACTOR cycle for an approved requirement and defined contract: prove the behavior is missing, implement the smallest fix, then improve structure without changing behavior."
disable-model-invocation: true
---

# TDD

Complete one vertical behavior slice in a single invocation:

```text
acceptance criterion
        ↓
RED: test fails for the missing behavior
        ↓
GREEN: smallest implementation passes
        ↓
REFACTOR: improve structure while tests stay green
```

Do not stop between phases for a separate skill handoff.

## Input

- One approved requirement and acceptance criterion
- One defined contract from `/skill:define-contract`
- The repository's existing code and test conventions

## Output

One deterministic behavior test, the smallest production change that makes it pass, and any justified behavior-preserving cleanup. Report changed paths, the verified RED failure, and the final focused and regression test results.

## Rules

- Work on one behavior at a time; do not write several tests before implementing them.
- Test observable behavior through the public contract, not private helpers or implementation details.
- Prefer the cheapest test that cannot lie: unit for pure domain logic, integration for a real boundary, end-to-end for a user-visible flow.
- Use deterministic fixtures and isolated state. Mock only external system boundaries.
- Do not write production behavior during RED.
- Do not weaken or rewrite the test merely to make GREEN pass.
- Implement only what the requirement, contract, and current test require.
- Refactor only while all relevant tests are green, and never add behavior or speculative abstractions during REFACTOR.
- Preserve validation, errors, side effects, responsibility ownership, and dependency direction.

Read `../references/tdd.md`, `../references/tdd-tests.md`, and the Testing by level section of `../references/abstraction-levels.md`. Read `../references/tdd-mocking.md` when the behavior crosses an external boundary. Before REFACTOR, read `../references/tdd-refactoring.md` and `../references/deep-modules.md`.

## Human checkpoint

Do not run a full `/skill:grill-me`; the approved requirement and contract bound the work. Before editing, state the scenario as:

> Given [starting state], when [action], then [observable result].

Show the exact planned test and production paths and ask for confirmation once. Ask another focused question only if the acceptance criterion conflicts with the contract or multiple behaviorally different implementations remain possible.

## Workflow

### 1. RED — prove the gap

1. Find the repository's test convention and choose the appropriate abstraction level.
2. Add the smallest test for the selected acceptance criterion.
3. Run the focused test.
4. Confirm it fails specifically because the required behavior is missing.
   - If it already passes, stop and determine whether the behavior exists or the test is ineffective.
   - If setup or contract errors cause the failure, repair the test setup without adding production behavior and rerun it.

Do not continue until RED is verified.

### 2. GREEN — make it pass

1. Re-run the focused test and inspect its failure.
2. Trace the smallest production path from the public contract to the missing behavior.
3. Implement the minimal correct change without anticipating future tests.
4. Run the focused test until it passes.
5. Run the relevant existing test subset for regressions.

Do not continue until the focused and relevant regression tests are green.

### 3. REFACTOR — improve safely

1. Identify one concrete smell in the changed code: unclear naming, duplicated logic, mixed responsibility, or unnecessary complexity.
2. If there is no concrete improvement, skip refactoring; green code does not require churn.
3. Otherwise make one smallest structural improvement at a time and rerun the focused test after each meaningful change.
4. Run the relevant regression tests again.
5. Stop when the code is clear enough.

## Completion criterion

The cycle is complete only when:

- the test was observed failing for the intended missing behavior;
- the same test passes without being weakened;
- relevant regression tests pass;
- any refactor preserved the contract and observable behavior;
- the diff contains no unrelated scope or speculative design.
