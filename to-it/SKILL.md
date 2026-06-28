---
name: to-it
description: Write an integration test that chains real components together with controlled mock data at system boundaries. Use when user says "write integration test", "to-it", or invokes /to-it. Works well with findings from /attack.
---

# To Integration Test

If `source-of-truth/` exists in the project root, read relevant files on testing and coding constraints.
Read `../references/tdd.md` and `../references/tdd-tests.md` and `../references/tdd-mocking.md` before writing.

Before writing any test, present the plan to the human and wait for explicit approval. Do not proceed until they confirm they are satisfied.

Write an integration test that proves two or more real components handle the unexpected case correctly when wired together.

## What to test

An integration test uses real implementations of the components under test. Mock only what lives outside the system boundary (third-party APIs, external DBs, hardware). Internal components run for real.

## Steps

1. **Identify the chain** — which components interact to handle this behavior?
2. **Define the case** — what unexpected input flows through the chain, and what should come out the other end?
3. **Mock system boundaries** — only external services. Derive mock responses from the actual input — same shape, same edge characteristics.
4. **Write the test** — wire the real components, inject the unexpected input, assert the exact outcome.
5. **Name it** after the cross-component failure: `test_auth_rejects_expired_token_from_cache`, not `test_auth`.

All files go in `tests/`. Follow existing naming conventions.
