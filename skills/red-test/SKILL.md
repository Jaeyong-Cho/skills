---
name: red-test
description: Write the smallest failing test for one approved requirement and its defined contract, then run it to prove the missing behavior is actually uncovered. Use after define-contract and before implementation.
disable-model-invocation: true
---

# Red Test

Turn one requirement's acceptance criterion into evidence that the behavior is missing.

## Input

- One selected requirement and its acceptance criterion
- The defined contract
- Existing test conventions and the current codebase

## Output

A deterministic test at the appropriate abstraction level that fails specifically because the required behavior is missing. It is input to `/skill:green-implement`.

## Rules

- Require one requirement and one defined contract before starting.
- Derive the test from an acceptance criterion, not from the planned implementation.
- Prefer the cheapest test that cannot lie: unit test for pure logic, integration test for a real boundary, end-to-end test for a user-visible flow.
- Use deterministic fixtures and isolated state.
- Do not implement production behavior and do not weaken the assertion just to get green.
- Test through the contract's public behavior, not private helpers or implementation details.
- For L1 orchestration, prefer an integration test; for L2 domain behavior, isolate only the L3 contract; for L3 mechanisms, test the real test instance or vendor contract.

## Human interview

MUST RUN `/skill:grill-me` using `../references/human-checkpoint.md`, scoped only to selecting the acceptance scenario and verification level for this test. Before writing the test, present the scenario in plain language:

> “Given [starting state], when [action], should [observable result] happen?”

Ask the human to confirm the scenario or correct it. If the acceptance criterion is already explicit, state the chosen criterion and ask only for confirmation before creating the test.

## OOD check

Use `../references/abstraction-levels.md` to choose the test level and `../references/deep-modules.md` to avoid coupling the test to a wide interface.

## Workflow

1. Select the smallest normal acceptance criterion. Add one relevant exception or boundary criterion only when it protects the same requirement.
2. Locate the repository's existing test convention and create the test beside similar tests.
3. Arrange the smallest concrete input and precondition.
4. Act through the defined contract.
5. Assert one observable result, state change, or failure.
6. Run the focused test.
7. If it passes before implementation, stop and determine whether the behavior already exists or the test is ineffective. If it fails for setup or contract errors, fix the test setup—not the production behavior—and rerun.

## Completion criterion

The test exists, asserts the requirement's observable behavior, runs deterministically, and fails specifically because the required behavior is not implemented. Report the test path and failure output summary. Next skill: `/skill:green-implement`.
