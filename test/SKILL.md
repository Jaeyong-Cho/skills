---
name: test
description: Run tests for a plan or discover and run all tests
disable-model-invocation: true
---

# Test

If a plan slug is provided as an argument (e.g., `/test my-plan-slug`), load that plan. If no slug is provided, list all plans in `.context/plan/` and ask the user which to run tests for. If the user declines to select a plan, discover and run all tests in the project.

Read the matching ADR from `.context/adr/` (same slug) and RDR from `.context/rdr/` (same slug) for test strategy, scope, and acceptance criteria. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`.

**If a plan exists:** Run tests specified in the plan. If the plan specifies a scope (unit only, integration only, or both), use that. Otherwise default to both.

**If no plan:** Discover the project's test method and run all tests. Default to both unit and integration tests unless the user specifies otherwise.

Completion criterion: all specified tests executed and results reported.

When done: show each test's pass/fail status. Report the total count (passed, failed, skipped). If any tests failed, list them explicitly.
