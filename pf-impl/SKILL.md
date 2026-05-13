---
name: pf-impl
description: |
  Implement code from an AEO ADR using TDD (RED → GREEN → REFACTOR).
  Use after an ADR has been written and confirmed. Reads the ADR's Step-by-Step Plan and User Stories, then implements one behavior at a time through the red-green-refactor loop.
  Triggers: "pf-impl", "implement the ADR", "implement with TDD", "start implementation", "write the code" when an AEO ADR exists.
---

> Use `/caveman` for compressed output during this session.

# AEO Implementation (TDD)

For TDD philosophy and the RED→GREEN→REFACTOR loop, read `references/tdd.md`.

ADRs are stored at `.pf/src/adr/<ID>-<slug>.md` (e.g. `adr-001` → `.pf/src/adr/0001-*.md`).

If the user names an ADR (e.g. "adr-001", "0001", "auth-flow"), find the matching file with:

```bash
ls .pf/src/adr/ | grep 0001
```

If no ADR is specified, list available ADRs and ask which one to implement.

---

## Step 1: Extract behaviors from the ADR

For layer definitions, read `../pf/references/layers.md`.

From the ADR, collect:

1. **Behavior list** — each item in the Step-by-Step Plan becomes one RED→GREEN cycle
2. **Test targets** — from Testing Decisions: which layers and modules get tests
3. **Priority order** — implement the tracer bullet (most end-to-end behavior) first

Example behavior list extracted from an ADR:
```
1. User can log in with valid credentials       [tracer bullet]
2. Login rejects unknown email
3. Login rejects wrong password
4. User object validates its own password hash
```

Confirm the behavior list and priority with the user before writing any code.

---

## Step 2: Implement — one behavior at a time

For test writing examples, read `references/tdd-tests.md`.
For mocking guidelines, read `references/tdd-mocking.md`.

For each behavior in the plan:

```
RED:   Write a test that describes the behavior using the public interface → confirm it fails
GREEN: Write minimal code to make it pass → confirm it passes
```

- Test names must match the User Stories from the ADR
- Test only through public interfaces (value-layer entry points, object public actions)
- Do not write the next test until the current one is green

---

## Step 3: Refactor (after all behaviors are green)

For refactoring guidelines, read `references/tdd-refactoring.md`.
For deep module and interface design principles, read `../pf/references/deep-modules.md`.

- [ ] Can any interface be narrowed?
- [ ] Is complexity hidden or exposed?
- [ ] Any duplication to extract?

Run all tests after each refactor step. Never refactor while RED.

---

## Step 4: Done

Once all behaviors are implemented and tests are green:

1. Show the user a summary of what was built
2. Ask the user to confirm the code review
3. On confirmation: use the `pf-docs` skill to update the documentation, and mark the ADR status as `Accepted`

