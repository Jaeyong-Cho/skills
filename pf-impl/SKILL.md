---
name: pf-impl
description: |
  Implement code from an VAO ADR using TDD (RED → GREEN → REFACTOR).
  Use after an ADR has been written and confirmed. Reads the ADR's Step-by-Step Plan and User Stories, then implements one behavior at a time through the red-green-refactor loop.
  Triggers: "pf-impl", "implement the ADR", "implement with TDD", "start implementation", "write the code" when an VAO ADR exists.
---


# VAO Implementation (TDD)

For TDD philosophy and RED→GREEN→REFACTOR loop, read `references/tdd.md`.

Find the ADR file — search the project for markdown files matching the name or ID the user gives (`find . -name "*.md" | grep <id>`). If none specified, list candidates and ask which to implement.

## Step 1: Extract behaviors from ADR

For layer definitions, read `../pf/references/layers.md`.

From ADR collect:
1. **Behavior list** — each item in Step-by-Step Plan becomes one RED→GREEN cycle
2. **Test targets** — from Testing Decisions: which layers and modules get tests
3. **Priority order** — implement tracer bullet (most end-to-end behavior) first

Example:
```
1. User can log in with valid credentials       [tracer bullet]
2. Login rejects unknown email
3. Login rejects wrong password
4. User object validates its own password hash
```

## Step 2: Implement — one behavior at a time

For test writing examples read `references/tdd-tests.md`. For mocking read `references/tdd-mocking.md`.

For each behavior:
```
RED:   Write test via public interface → confirm fails
GREEN: Write minimal code → confirm passes
```

Test names must match ADR User Stories. Test only through public interfaces. Do not write next test until current is green.

## Step 3: Refactor (after all behaviors green)

For refactoring guidelines read `references/tdd-refactoring.md`. For interface design read `../pf/references/deep-modules.md`.

- [ ] Interface narrowable?
- [ ] Complexity hidden or exposed?
- [ ] Duplication to extract?

**Observability checklist** (see `../pf-observe/REFERENCE.md` for patterns and CLI flag conventions):
- [ ] Logs key inputs, outputs, and state changes at appropriate level?
- [ ] Logs environment info (runtime version, env name, config values) on startup or entry?
- [ ] Logs dependency versions where relevant?
- [ ] Writes important runtime state to a file (structured log, snapshot, or output file) for later inspection?
- [ ] Errors include enough context (input values, state) to diagnose without a debugger?
- [ ] Existing `observe/` scripts still compatible? (`ls observe/ 2>/dev/null` — check each script still targets valid paths, interfaces, and output formats)

Run all tests after each refactor step. Never refactor while RED.

## Step 4: Markdown report

Ask via `AskUserQuestion`: "Write the markdown report?" — if no, skip and go to Step 5.

Save: `reports/impl/YYYY-MM-DD-<slug>.md` (slug from ADR name, lowercase, hyphens, max 40 chars)

Free-form markdown — write what matters. Always include: behavior results table (behavior, GREEN/RED, test name). Include when warrants: refactor summary, open questions.

```
Report: reports/impl/YYYY-MM-DD-<slug>.md
```

## Step 5: Done

Show summary of what was built. Ask user to confirm code review. On confirmation: update documentation and mark ADR status as `Accepted`.
