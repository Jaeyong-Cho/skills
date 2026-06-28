---
name: to-e2et
description: Write an end-to-end test that drives the full application flow with an unexpected input or sequence. Use when user says "write e2e test", "to-e2et", or invokes /to-e2et. Works well with findings from /attack.
---

# To E2E Test

If `source-of-truth/` exists in the project root, read relevant files on testing and coding constraints.
Read `../references/tdd.md` and `../references/tdd-tests.md` before writing.

Before writing any test, present the plan to the human and wait for explicit approval. Do not proceed until they confirm they are satisfied.

Write an e2e test that drives the full application flow from entry point to final output, verifying the system handles the unexpected case end-to-end.

## What to test

An e2e test treats the system as a black box. Drive it through its real interface (CLI, HTTP, UI). Mock only what cannot run locally (third-party payment APIs, SMS gateways, hardware).

## Steps

1. **Identify the flow** — what is the full user journey or request path this case triggers?
2. **Define the case** — what unexpected input or sequence enters the system, and what should the final observable output be?
3. **Mock only external third parties** — everything internal runs for real.
4. **Write the test** — start from the real entry point, inject the unexpected input, assert the final output or side effect.
5. **Name it** after the full-flow failure: `test_checkout_fails_gracefully_on_invalid_card`, not `test_checkout`.

All files go in `tests/`. Follow existing naming conventions. Update `tests/run.sh` if it exists to include the new test.
