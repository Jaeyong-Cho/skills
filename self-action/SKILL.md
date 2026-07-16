---
name: self-action
description: Read a plan and scaffold implementation with TODO hints in source files
disable-model-invocation: true
---

# Self-Action

Read the plan to scaffold from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture and design context. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md` for testing patterns.

For each step in the plan's Action Sequence:

- **If the step involves tests:** Generate complete test code following the plan's test specifications. Tests should be ready to run immediately and cover all cases the plan lists.
- **Function signatures and interfaces — scaffold with TODOs:** Create function declarations, method signatures, and interface/type definitions. Add TODO hints explaining the contract: what it takes, what it returns, what it should do. Do not implement the bodies.
- **Implementation logic — write complete:** Write all implementation logic inside function bodies. Handle edge cases, assertions, validation, and error handling. Production-ready, no TODOs.

Completion criterion: all tests written, all function signatures and interfaces defined with TODO explanations (human's ~30%), and all implementation logic fully written (AI's ~70%).

When done: report which files were modified, which were created, which tests were added, and which function signatures are ready for human review. Do not report anything beyond the changes made.
