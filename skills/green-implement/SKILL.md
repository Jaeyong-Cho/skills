---
name: green-implement
description: Implement the smallest production change that makes one verified red test pass, while preserving the defined contract and requirement boundary. Use after red-test.
disable-model-invocation: true
---

# Green Implement

Make one failing requirement test pass with the smallest correct implementation.

## Input

- One requirement and its contract
- One verified failing test from `/skill:red-test`
- The repository's existing implementation and test conventions

## Output

The smallest production implementation that makes the focused test pass, plus passing focused and relevant regression tests. It is input to `/skill:refactor-green`.

## Rules

- Require an existing requirement, contract, and focused failing test.
- Read the failing test and failure output before editing production code.
- Implement only the behavior required by the test and contract.
- Do not edit the test to hide a failure.
- Do not add speculative abstractions, configuration, retries, or features.
- Preserve input validation, error handling, and data-safety requirements.
- Keep one abstraction level per function: L1 orchestrates, L2 expresses domain rules, and L3 performs technical mechanisms.
- Keep each responsibility with its cohesive owner; accept dependencies instead of constructing them inside the rule under test.

## OOD check

Read `../references/abstraction-levels.md` before editing. Do not let an L1 function issue raw infrastructure calls or an L2 function embed database, HTTP, SDK, or filesystem details. Use a narrow capability contract when a mechanism must be substituted.

## Workflow

1. Re-run the focused red test and capture the failure.
2. Trace the smallest production path from the contract to the missing behavior.
3. Implement the minimal change.
4. Run the focused test until it passes.
5. Run the relevant existing test subset to catch regressions.
6. Report changed files, tests run, and any explicitly deferred behavior.

## Completion criterion

The focused test passes, relevant regression tests pass, the implementation stays within one requirement, and no test was weakened or bypassed. Next skill: `/skill:refactor-green`.
