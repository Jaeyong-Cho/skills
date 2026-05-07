# TDD in AEO

Implementation always follows TDD: one behavior at a time, RED → GREEN → REFACTOR.

For test writing examples, read `references/tdd-tests.md`.
For mocking guidelines, read `references/tdd-mocking.md`.
For refactoring after green, read `references/tdd-refactoring.md`.
For interface design for testability, read `references/deep-modules.md`.

---

## Philosophy

**Core principle**: Tests verify behavior through public interfaces — not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation: they mock internal collaborators, test private methods, or verify through external means. The warning sign: your test breaks when you refactor, but behavior hasn't changed.

---

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code."

This produces bad tests:
- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, signatures) rather than user-facing behavior
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine
- You commit to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

---

## Workflow

### 1. Before writing any code

From the ADR's Step-by-Step Plan, extract the behavior list:

- [ ] Which value-layer entry points are being added or changed?
- [ ] Which entity actions or behaviors need verification?
- [ ] Which behaviors are most critical? (test those first)
- [ ] Confirm with the user before starting

**You can't test everything.** Focus on critical paths and complex logic, not every edge case.

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

Run tests after each refactor step. **Never refactor while RED.**

---

## AEO layer guidance

| Layer | What to test |
|---|---|
| **Value** | Entry point behavior — correct result for the user need |
| **Method** | Workflow outcome — given these entities, the right result is produced |
| **Entity** | Public actions and behaviors — state transitions, not internal fields |

## Checklist per cycle

```
[ ] Test names match User Stories from the ADR
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
