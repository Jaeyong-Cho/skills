# Testing Guidelines

The goal of testing is not to maximize code coverage or the number of tests. The goal is to provide confidence in important behavior and prevent regressions with reasonable maintenance cost.

## General Principles

- Do not write a unit test for every function mechanically.
- Test observable behavior and contracts rather than implementation details.
- Identify the failure mode you want to prevent, then choose the appropriate test level.
- If a smaller and faster test can provide the same confidence, prefer it over a heavier test.
- Do not break production-code encapsulation solely to make implementation details testable.
- Do not create meaningless tests just to increase coverage.
- Tests SHOULD NOT be unnecessarily coupled to implementation details or internal refactoring.

## Unit Tests

Prefer unit tests for:

- Business rules
- Calculations and transformations
- Validation logic
- State transitions
- Logic with meaningful branches or conditions
- Important edge cases and boundary conditions
- Reusable core utilities with non-trivial behavior
- Logic that has caused bugs in the past

Generally, do not create dedicated unit tests for:

- Simple getters and setters
- Trivial constructors
- Simple delegation
- Thin wrappers with no meaningful logic
- Behavior already guaranteed by the framework or language
- Private implementation details that are sufficiently covered through public behavior

If a private function becomes complex enough that directly testing it seems necessary, do not expose it merely for testing.

Instead, consider whether the logic represents a meaningful domain abstraction that SHOULD be extracted into its own class, module, or component.

## Integration Tests

Use integration tests to verify integration boundaries such as:

- Database queries
- ORM mappings
- Repositories
- Filesystems
- Message brokers
- Caches
- Framework integrations
- Interactions between multiple components

Do not attempt to prove real integration behavior using only mocked unit tests.

If correctness depends on the actual behavior of a database, framework, serialization library, message broker, or another infrastructure component, test against an appropriate real or realistic integration environment.

## API / Contract Tests

Use API or contract tests to verify:

- HTTP status codes
- Request and response schemas
- Serialization and deserialization
- Input validation
- Authentication and authorization
- Contracts between services
- Backward compatibility of externally consumed interfaces

Do not repeat every internal business-logic edge case at the API level if those cases are already sufficiently covered by lower-level tests.

## End-to-End Tests

Use end-to-end tests for critical user workflows such as:

- Sign-up
- Login
- Checkout
- Payment
- Order creation

Do not attempt to cover every edge case with E2E tests.

E2E tests SHOULD focus on critical happy paths and important failure paths that can only be validated when the entire system is connected.

Keep the E2E suite relatively small, stable, and focused on high-value workflows.

## Regression Tests

A regression test is not necessarily a separate test level.

It describes the **purpose of a test: preventing a previously discovered bug from occurring again.**

A regression test can therefore be implemented as a:

- Unit test
- Integration test
- API test
- Contract test
- End-to-end test

Choose the lowest appropriate test level that can reliably reproduce the bug.

When fixing a bug, prefer the following workflow:

1. Reproduce the bug.
2. Add a test that demonstrates the incorrect behavior and fails before the fix.
3. Fix the production code.
4. Verify that the regression test now passes.
5. Keep the test in the test suite to prevent the same bug from returning.

Examples:

- Business-rule or calculation bug → Unit regression test
- Database query or ORM mapping bug → Integration regression test
- Serialization or API contract bug → API / Contract regression test
- Bug caused by interactions between multiple systems → Integration or E2E regression test

Do not create an expensive E2E regression test when a smaller unit or integration test can reliably reproduce and prevent the same problem.

A regression test SHOULD clearly communicate what previously broken behavior it protects.

Do not interpret "regression testing" only as rerunning existing tests after a change. When fixing a real bug, prefer adding a specific test case that reproduces that bug and permanently protects against its recurrence.

## Choosing the Appropriate Test

Before writing a test, ask:

1. What failure or regression are we trying to prevent?
2. Is this primarily business logic?
   → Prefer a Unit Test.
3. Does correctness depend on a database, framework, external component, or integration boundary?
   → Prefer an Integration Test.
4. Is this about an API or service contract?
   → Prefer an API / Contract Test.
5. Can this behavior only be validated through a complete user workflow?
   → Prefer an E2E Test.
6. Is this fixing a bug that actually occurred?
   → Strongly consider adding a Regression Test at the lowest appropriate level.
7. Can a smaller test provide the same confidence?
   → Prefer the smaller test.

## Mocking

Use mocks primarily at boundaries where isolation provides meaningful value.

Good candidates include:

- External APIs
- Network calls
- Time / clocks
- Randomness
- Expensive or unavailable external dependencies

Avoid excessive mocking of internal collaborators.

In particular, avoid tests that primarily verify implementation call sequences such as:

"Method A calls Method B exactly once."

Prefer testing observable outcomes such as:

"Given input X, the system produces result Y."

Interaction verification is appropriate when the interaction itself is part of the contract or behavior, but it SHOULD NOT be the default testing strategy.

## Test Quality

Good tests SHOULD generally be:

- Deterministic
- Fast enough for their test level
- Independent
- Readable
- Clear when they fail
- Resistant to unrelated implementation refactoring

Test names SHOULD describe behavior rather than implementation whenever possible.

For example, prefer:

`should_reject_expired_coupon`

over:

`should_call_validate_coupon_method`

## When Modifying Code

Before adding or modifying tests, inspect the existing testing strategy and conventions of the codebase.

Do not mechanically add tests for every function that was changed.

Instead, determine:

- Was new behavior introduced?
- Was existing behavior changed?
- Was a new edge case introduced?
- Did an integration boundary change?
- Did an external or internal contract change?
- Is the change fixing an actual bug?

For bug fixes, whenever practical, add a regression test that reproduces the bug **before modifying the production code**.

Then implement the fix and verify that the regression test passes.

Avoid duplicating coverage at multiple test levels unless each level protects against a meaningfully different failure mode.

## Final Principle

Do not optimize for the number of tests or code coverage alone.

**Optimize for maximum confidence in important behavior with the lowest reasonable maintenance cost.**

Test important behavior for new features.

For bug fixes, leave behind a regression test whenever practical so that the same failure cannot silently return.
