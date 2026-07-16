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

**Working code:** Error handling infrastructure, language details (try/catch syntax, regex patterns), implementation mechanics.

**Holes:** Orchestration, component interactions, representative examples, business logic flow, transformation logic.

Completion criterion: all tests written, all files created with a mix of working code and strategic holes (human's ~30% holes, AI's ~70% working), showing the full flow and interactions.

When done: report which files were modified, which were created, which tests were added, and which steps have holes for human to fill. Do not report anything beyond the changes made.

## Example: Calculator

Applying the five rules:

**Working (AI):**
- `main()` try/catch + while loop structure (Rule 1: error infrastructure)
- `execute()` try/catch blocks for ValueError and ZeroDivisionError (Rule 1: error infrastructure)
- `Expression.evaluate()` implementation for operator '+' (Rule 2: show one case, others follow the pattern)
- Regex pattern syntax in `parse_expression()` (Rule 5: syntax, not logic)

**Holes (Human):**
- `main()` line 109-111: Call `usecase.execute(line)` and print (Rule 4: orchestration)
- `execute()` line 72-77: Sequence of parse → evaluate → return result (Rule 4: orchestration, Rule 5: data transformation)
- `execute()` error handling logic: which error triggers which message (Rule 3: decision logic)
- `Expression.evaluate()` implementation for operator '-' (Rule 2: one representative case; human applies pattern to '*' and '/')

Human reads working code (infrastructure, one example), fills holes (orchestration, decisions, representative pattern), and understands the full system without excessive typing.
