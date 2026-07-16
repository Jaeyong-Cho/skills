---
name: self-action
description: Read a plan and scaffold implementation with TODO hints in source files
disable-model-invocation: true
---

# Self-Action

Read the plan to scaffold from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture and design context. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md` for testing patterns.

For each step in the plan's Action Sequence:

- **If the step involves tests:** Generate complete test code following the plan's test specifications. Tests should be ready to run immediately and cover all cases the plan lists.
- **Create holes in the code:** Write complete file structure and implementations, but leave strategic gaps (TODOs) throughout the code. Place holes where they teach understanding: at key decision points, transformation steps, and logical branches. Not every detail—just enough that filling them reveals how the system works end-to-end.
- **Holes guide learning:** Each TODO explains what should happen at that point and why. The human fills these holes to understand the full flow, not just the top-level architecture.
- **Supporting code is complete:** Error handling, validation, infrastructure, and edge case scaffolding are production-ready. Only the strategic, learning-critical pieces are holes.

Completion criterion: all tests written, all files created with complete supporting code and strategic holes placed throughout (human's ~30%), ready for human implementation.

When done: report which files were modified, which were created, which tests were added, and which functions contain holes for human implementation. Do not report anything beyond the changes made.
