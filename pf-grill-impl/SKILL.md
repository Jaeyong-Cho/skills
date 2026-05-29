---
name: pf-grill-impl
description: |
  Design and implement a feature in one session using VAO + TDD — no ADR written.
  Grills the user to reach a clear VAO design, extracts behaviors, then implements one at a time via RED→GREEN→REFACTOR.
  Use when the user wants to think through a design and implement immediately without writing a formal ADR.
  Triggers: "pf-grill-impl", "design and implement", "think through and build", "quick impl", "no ADR just implement".
---

For layer definitions read `../pf/references/layers.md`. For TDD philosophy read `../pf-impl/references/tdd.md`.

# VAO Design + Implement (No ADR)

Design direction: **Value → Aspect → Object** (iterative in practice).

## Step 1: Grill the design

Read `../pf/references/deep-modules.md`, `../pf/references/layers.md`. Run `grill-me` skill with user's scenario as starting context. No maximum questions — keep going until all ambiguity is gone and consensus is reached. When referencing source code, show the relevant snippet inline with `file:line` header before asking. User can say **"wrap up"** to move on.

## Step 2: Extract behavior list

From grill conclusions derive and show:

```
Behavior list:
1. <tracer bullet behavior>    [value]
2. <next behavior>             [aspect]
3. <next behavior>             [object]

Test targets:
- <file> → <what gets tested>
```

Ask via `AskUserQuestion`: "Ready to implement?" — adjust list if needed.

## Step 3: Implement — one behavior at a time

Read `../pf-impl/references/tdd-tests.md` for test examples, `../pf-impl/references/tdd-mocking.md` for mocking.

For each behavior:
```
RED:   Write test via public interface → confirm fails
GREEN: Write minimal code → confirm passes
```
Do not write next test until current is green.

## Step 4: Refactor (after all green)

Read `../pf-impl/references/tdd-refactoring.md`, `../pf/references/deep-modules.md`.

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

Ask via `AskUserQuestion`: "Write the markdown report?" — if no, skip and go to Step 6.

## Step 5: Markdown report

Save: `reports/impl/YYYY-MM-DD-<slug>.md` (slug = feature name, lowercase, hyphens, max 40 chars)

Free-form markdown — write what matters. Always include: behavior results table (behavior, layer, GREEN/RED, test name). Include when warrants: refactor summary, key design decisions, open questions.

```
Report: reports/impl/YYYY-MM-DD-<slug>.md
```

## Step 6: Done

Show summary of what was built. Suggest commit message using `../pf/references/commit.md`.
