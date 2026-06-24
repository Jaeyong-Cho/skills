---
name: impl
description: Implement a feature using TDD, grounded in the meta-pattern coordinate system — knows where the code sits (Abstractness / Subdomain axis), respects layer dependency rules, and follows RED → GREEN → REFACTOR. Can work from an IF spec, ADR, or direct user description. Use when user wants to implement something, mentions "impl", "implement this", "build this feature", "write the code".
---

# Impl

Implement faithfully, one unit at a time, via TDD. Structure follows the meta-pattern coordinate.

Read [deep-modules](../references/deep-modules.md), [tdd](../references/tdd.md), [tdd-tests](../references/tdd-tests.md), [tdd-mocking](../references/tdd-mocking.md), [tdd-refactoring](../references/tdd-refactoring.md), and [meta-pattern REFERENCE](../meta-pattern/REFERENCE.md) before starting.

## Step 1: Locate on the coordinate

Before writing any code, place the target on the meta-pattern axes:
- **Abstractness** — which layer? (External / Usecase / Logics / Objects)
- **Subdomain** — which domain does this belong to?
- **Pattern** — which meta-pattern does the surrounding structure follow?

This determines: dependency direction, what can be imported, and what must be injected.

## Step 2: Read the spec

Read whatever spec exists — IF doc (`src/if/`), ADR (`docs/src/adr/`), or user description. Extract the list of entry points to implement. If spec is missing or ambiguous, ask before guessing.

## Step 3: Implement — one entry point at a time

Follow RED → GREEN → REFACTOR for each entry point:

### RED
Write a failing test that calls only the public interface and asserts specified behavior. Must fail before any implementation.

### GREEN
Write minimal code to pass:
1. Match the signature exactly
2. Inject dependencies — never instantiate them inside
3. Follow the layer rule: never import from an outer layer
4. Run tests — confirm GREEN before moving on

### REFACTOR
With all tests green:
- Narrow any interface that's wider than needed
- Extract duplication into private helpers
- Check that complexity is hidden, not leaking

Run tests after each refactor step. Never refactor while RED.

## Rules

- No new public interface beyond what the spec defines
- If code placement would violate the dependency rule (inner → outer), stop and surface it
- If the meta-pattern of surrounding code conflicts with what you're adding, flag it before continuing
