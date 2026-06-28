---
name: to-ut
description: Write unit tests for a specific function or module, targeting a weakness or unexpected input. Use when user says "write unit test", "to-ut", or invokes /to-ut. Works well with findings from /attack.
---

# To Unit Test

If `source-of-truth/` exists in the project root, read relevant files on testing and coding constraints.
Read `../references/tdd.md` and `../references/tdd-tests.md` and `../references/tdd-mocking.md` before writing.

Before writing any test, present the plan to the human and wait for explicit approval. Do not proceed until they confirm they are satisfied.

Write a unit test that isolates and pins one specific behavior — especially failure paths and edge cases.

## What to test

A unit test targets the smallest unit that owns the behavior: one function, one method, one class. No real DB, no real network — mock all external dependencies.

## Steps

1. **Identify the target** — which function/module owns this behavior?
2. **Define the case** — what is the input and what is the exact expected output or error?
3. **Mock externals** — replace DB, API, filesystem calls with mocks that return controlled values. Derive mock data from the actual input — same shape, same edge characteristics.
4. **Write the test** — one test, one assertion of the exact failure mode.
5. **Name it** after what it's breaking: `test_returns_null_on_empty_input`, not `test_process`.

All files go in `tests/`. Follow existing naming conventions.
