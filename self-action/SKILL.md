---
name: self-action
description: Read a plan and scaffold implementation with TODO hints in source files
disable-model-invocation: true
---

# Self-Action

Read the plan to scaffold from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture and design context. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md` for testing patterns.

For each step in the plan's Action Sequence:

- **If editing an existing file:** Add a TODO hint directly at the source location (inline comment with implementation guidance, constraints, edge cases). Do not modify other code.
- **If creating a new file:** Create the file with skeleton functions (signatures only), each with a TODO hint explaining what it should do. Match the file structure and language idioms the plan specifies.
- **If the step involves tests:** Generate test code following the plan's test specifications. Tests should be ready to run immediately and cover the cases the plan lists.

Completion criterion: every step has scaffolding in place (TODOs added to existing code or skeleton code created for new code), and all specified tests are written.

When done: report which files were modified, which were created, and which tests were added. Do not report anything beyond the changes made.
