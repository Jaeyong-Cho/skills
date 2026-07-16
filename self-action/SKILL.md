---
name: self-action
description: Read a plan and scaffold implementation with TODO hints in source files
disable-model-invocation: true
---

# Self-Action

Read the plan to scaffold from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture and design context. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md` for testing patterns.

For each step in the plan's Action Sequence:

- **If the step involves tests:** Generate complete test code following the plan's test specifications. Tests should be ready to run immediately and cover all cases the plan lists.
- **Top-level architecture and flow — scaffold with TODOs:** Create the orchestration layer: main functions, call sequences, interface definitions, and component interactions. Add TODO hints explaining the big picture: what calls what, in what order, and why. Show the main pipeline structure. Do not fill in detailed implementations inside each function.
- **Detailed implementations — write complete:** Inside each function body, write complete, production-ready logic. Handle edge cases, error handling, validation, and constraints. This is where the complexity lives, but it's internal to each function—hidden from the orchestration layer above.

Completion criterion: all tests written, top-level architecture and flow clear with TODOs (human's ~30%), and all detailed implementations complete (AI's ~70%).

When done: report which files were modified, which were created, which tests were added, and which orchestration/flow functions are ready for human review. Do not report anything beyond the changes made.
