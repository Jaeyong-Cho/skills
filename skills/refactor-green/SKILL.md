---
name: refactor-green
description: Refactor an implementation after its requirement test is green without changing observable behavior or expanding scope. Use after green-implement.
disable-model-invocation: true
---

# Refactor Green

Improve the code only after the requirement is working and protected by a test.

## Input

- A passing implementation from `/skill:green-implement`
- The original requirement and contract
- Passing focused and relevant regression tests

## Output

A behavior-preserving, clearer implementation with all required tests still passing and no scope expansion. The workflow is complete for this slice.

## Rules

- Require a passing focused test and the original requirement.
- Preserve the contract, observable behavior, errors, and side effects.
- Make one structural improvement at a time.
- Do not add new behavior, abstractions, dependencies, or speculative flexibility.
- Rerun the focused test after every meaningful change.
- Preserve responsibility ownership and dependency direction; do not move business rules into mechanisms or infrastructure details into domain code.

## OOD check

Read `../references/abstraction-levels.md` and `../references/deep-modules.md`. Check the one-sentence test, cohesion, interface width, dependency direction, and whether any extraction names a real concept rather than merely shortening a long function.

## Workflow

1. Read the implementation and identify one concrete smell: unclear name, duplicated logic, mixed responsibility, or unnecessary complexity.
2. Make the smallest structural change that removes that smell.
3. Run the focused test.
4. Run the relevant regression tests.
5. Stop when the code is clear enough; do not refactor for its own sake.

## Completion criterion

The code is simpler or clearer, responsibilities and abstraction levels remain coherent, all behavior remains protected by passing tests, and the diff contains no scope expansion. Report the refactor and the tests run.
