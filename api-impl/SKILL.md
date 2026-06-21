---
name: api-impl
description: Implement existing API specs faithfully using TDD — public API is the only test target. Reads user-provided API docs and implements each entry point one at a time: write test → implement → refactor. Use when user has a designed API spec and wants it filled in, mentions "implement this API", "implement from docs", "implement existing API", "implement based on spec", or "api-impl".
---

# API Impl (From Docs — TDD)

Design is already done. Your job: implement it faithfully via TDD.

Read [deep-modules](../references/deep-modules.md), [archi](../references/archi.md), [tdd](../references/tdd.md), [tdd-tests](../references/tdd-tests.md), [tdd-mocking](../references/tdd-mocking.md), and [tdd-refactoring](../references/tdd-refactoring.md) before starting.

**Layer dependency rule**: inner layers never depend on outer (`Objects → Logics → Usecase → Interfaces`). If any wired dependency violates this, stop and surface the conflict before continuing.

**Test target rule**: tests call only public methods defined in the spec. Never test private helpers or internal state directly.

## Step 1: Read the API doc

User provides one or more API names to implement. For each, determine its layer and read `src/api/<layer>s/<name>.md` (e.g. `src/api/objects/user.md`, `src/api/logics/transfer.md`, `src/api/usecases/signup.md`).

Extract the list of public entry points to implement.

## Step 2: Implement — one entry point at a time

For each public method / CLI command / UI handler, follow RED → GREEN → REFACTOR:

### RED
Write a test that calls the public method and asserts its specified behavior. The test must fail before any implementation exists.
- Test calls only the public signature from the spec
- Test describes behavior ("user can cancel a pending order"), not implementation
- Test must survive an internal refactor without changing

### GREEN
Write the minimal code to make the test pass:
1. **Match the signature exactly** — name, params, return type, errors
2. **Follow the algorithm** — implement the described logic; don't invent
3. **Wire dependencies correctly** — accept them as injected params, don't instantiate inside (per [deep-modules](../references/deep-modules.md))
4. Run tests — confirm GREEN before moving on

### REFACTOR
With all tests green, check for improvements:
- Can any interface be narrowed?
- Any duplication to extract into private helpers?
- Is complexity hidden or leaking?

Run tests after each refactor step. Never refactor while RED.

Do not move to the next entry point until current one is GREEN and refactored.

## Step 3: Done

List implemented entry points vs spec. Flag any deviations with reason.

## Rules

- **No new public API.** Match the spec exactly — no additions.
- Private helpers are fine; just never test them directly.
- If spec is ambiguous, ask before guessing.
- If spec conflicts with testability principles, surface the conflict; don't silently deviate.
