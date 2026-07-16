---
name: self-action
description: Read a plan and scaffold implementation with TODO hints in source files
disable-model-invocation: true
---

# Self-Action

Read the plan to scaffold from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture and design context. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md` for testing patterns.

For each step in the plan's Action Sequence:

- **If the step involves tests:** Generate complete test code following the plan's test specifications. Tests should be ready to run immediately and cover all cases the plan lists.
- **For each step: decide working or hole:** Some steps are fully implemented (working code). Some steps have holes (TODOs). Place holes strategically so the human sees purpose, operations, interactions, and flow without much typing.
- **Working steps:** Complete, production-ready implementations. These show how parts connect and provide working context.
- **Hole steps:** Leave a TODO with a brief explanation of what this step does and why. The human fills it to understand how the pieces interact, not to implement everything from scratch.

Completion criterion: all tests written, all files created with a mix of working code and strategic holes (human's ~30% holes, AI's ~70% working), showing the full flow and interactions.

When done: report which files were modified, which were created, which tests were added, and which steps have holes for human to fill. Do not report anything beyond the changes made.
