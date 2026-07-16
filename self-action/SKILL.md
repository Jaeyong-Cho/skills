---
name: self-action
description: Read a plan and scaffold implementation with TODO hints in source files
disable-model-invocation: true
---

# Self-Action

Read the plan to scaffold from `.context/plan/`. If multiple plans exist, list them and ask the user which to use. Read the matching ADR from `.context/adr/` (same slug, via the plan's `**ADR:**` line) for the architecture and design context. Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md` for testing patterns.

For each step in the plan's Action Sequence:

- **If the step involves tests:** Generate complete test code following the plan's test specifications. Tests should be ready to run immediately and cover all cases the plan lists.

**Decide what's working vs hole using these five rules:**

1. **Remove happy-path logic** — keep error-handling structure, hole the core business flow
2. **One representative example per multiple case** — if there are multiple similar branches (e.g., multiple operators), hole only one representative case; human understands the pattern and applies it to others
3. **Hole the decision logic** — show *when* conditions are true/false, *what* triggers each path
4. **Hole the architectural flow** — how components call each other, the orchestration sequence, not the internal details of those calls
5. **Hole the transformations** — where data flows and changes shape, not the syntax of how it changes

**Priority:** Business logic flow (orchestration, transformations, decision paths) takes priority over error handling details (error message strings, exception catching structure).

**Working code:** Error handling infrastructure (try/catch blocks, exception catching), error message strings, language details (regex patterns, syntax). Complete, runnable, no TODOs.

**Holes:** Orchestration (component calls and sequence), transformations (data flow and changes), decision logic (when conditions), representative examples. Mark each hole with a TODO comment explaining:
- What should happen at this point
- Why it matters (architectural context, data flow, decision logic)
- What the human should implement or understand

Completion criterion: all tests written, all files created with a mix of working code and strategic holes (human's ~30% holes, AI's ~70% working), showing the full flow and interactions.

When done: report which files were modified, which were created, which tests were added, and which steps have holes for human to fill. Do not report anything beyond the changes made.
