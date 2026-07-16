---
name: self-action
description: Read a plan and scaffold implementation with TODO hints in source files
disable-model-invocation: true
---

# Self-Action

Read the plan to scaffold from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture and design context. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md` for testing patterns.

For each step in the plan's Action Sequence:

- **If the step involves tests:** Generate complete test code following the plan's test specifications. Tests should be ready to run immediately and cover all cases the plan lists.
- **Identify business logic:** Isolate the core feature logic that a human should understand and write (~30%). This is the conceptual heart of the feature. Everything else (infrastructure, setup, plumbing, error handling) is AI's responsibility.
- **Business logic only — scaffold with TODOs:** For business logic functions/blocks, create skeleton code (signatures only) with TODO hints explaining the business goal, inputs, outputs, and edge cases. Do not scaffold infrastructure or implementation details.
- **Everything else — write complete:** For non-business-logic code, write complete, production-ready implementations. No TODOs.

Completion criterion: all tests written, business logic scaffolded with clear TODOs (human's 30%), and all infrastructure/plumbing fully implemented (AI's 70%).

When done: report which files were modified, which were created, which tests were added, and which functions are scaffolded for human implementation. Do not report anything beyond the changes made.
