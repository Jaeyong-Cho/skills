---
name: pf-impl
description: |
  Implement code from an VAO ADR using TDD (RED → GREEN → REFACTOR).
  Use after an ADR has been written and confirmed. Reads the ADR's Step-by-Step Plan and User Stories, then implements one behavior at a time through the red-green-refactor loop.
  Triggers: "pf-impl", "implement the ADR", "implement with TDD", "start implementation", "write the code" when an VAO ADR exists.
---

Read `../pf/references/caveman.md` and apply caveman style throughout — including in all output documents.

Check for today's journal context:

```bash
[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null
```

If today.md found, read to understand user's current focus, active goals, blockers. Use to orient work — not to override task, but to connect implementation to user's broader context.

# VAO Implementation (TDD)

For TDD philosophy and RED→GREEN→REFACTOR loop, read `references/tdd.md`.

ADRs stored at `.pf/src/adr/<ID>-<slug>.md` (e.g. `adr-001` → `.pf/src/adr/0001-*.md`).

If user names ADR (e.g. "adr-001", "0001", "auth-flow"), find matching file with:

```bash
ls .pf/src/adr/ | grep 0001
```

If no ADR specified, list available ADRs and ask which to implement.

---

## Step 1: Extract behaviors from ADR

For layer definitions, read `../pf/references/layers.md`.

From ADR, collect:

1. **Behavior list** — each item in Step-by-Step Plan becomes one RED→GREEN cycle
2. **Test targets** — from Testing Decisions: which layers and modules get tests
3. **Priority order** — implement tracer bullet (most end-to-end behavior) first

Example behavior list extracted from ADR:
```
1. User can log in with valid credentials       [tracer bullet]
2. Login rejects unknown email
3. Login rejects wrong password
4. User object validates its own password hash
```

---

## Step 2: Implement — one behavior at a time

For test writing examples, read `references/tdd-tests.md`.
For mocking guidelines, read `references/tdd-mocking.md`.

For each behavior in plan:

```
RED:   Write test that describes behavior using public interface → confirm it fails
GREEN: Write minimal code to make it pass → confirm it passes
```

- Test names must match User Stories from ADR
- Test only through public interfaces (value-layer entry points, object public actions)
- Do not write next test until current one is green

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

Once all behaviors implemented and tests green:

1. Show user summary of what was built
2. Ask user to confirm code review
3. On confirmation: use `pf-docs` skill to update documentation, and mark ADR status as `Accepted`
