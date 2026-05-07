# TDD in AEO

Implementation always follows TDD: one behavior at a time, RED → GREEN → REFACTOR.

For test writing examples, read `references/tdd-tests.md`.
For mocking guidelines, read `references/tdd-mocking.md`.
For refactoring after green, read `references/tdd-refactoring.md`.
For interface design for testability, read `references/deep-modules.md`.

## What to test

Test through **public interfaces only** — value layer entry points and entity public actions.
Never test internal methods, private state, or implementation details.
A test that breaks on refactor without behavior changing is a bad test.

The ADR's **User Stories** map to test names. The ADR's **Testing Decisions** determine which modules get tests.

## Workflow

### 1. Before writing any code

From the ADR's Step-by-Step Plan, extract the behavior list:

- [ ] Which value-layer entry points are being added or changed?
- [ ] Which entity actions or behaviors need verification?
- [ ] Which behaviors are most critical? (test those first)
- [ ] Confirm with the user before starting

### 2. Tracer bullet

Write ONE test for the first behavior — the most end-to-end path that proves the wiring works.

```
RED:   test fails (behavior doesn't exist yet)
GREEN: minimal code to make it pass
```

### 3. Incremental loop

For each remaining behavior from the plan:

```
RED:   write next test → fails
GREEN: minimal code to pass → passes
```

Rules:
- One test at a time
- Only enough code to pass the current test
- Don't anticipate future tests

### 4. Refactor

After all tests are green, check for deep module opportunities (see `references/deep-modules.md`):

- [ ] Can any interface be narrowed?
- [ ] Is complexity hidden or exposed?
- [ ] Any duplication to extract?

Run tests after each refactor step. Never refactor while RED.

## AEO layer guidance

| Layer | What to test |
|---|---|
| **Value** | Entry point behavior — correct result for the user need |
| **Method** | Workflow outcome — given these entities, the right result is produced |
| **Entity** | Public actions and behaviors — state transitions, not internal fields |

## Checklist per cycle

```
[ ] Test names match User Stories from the ADR
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
