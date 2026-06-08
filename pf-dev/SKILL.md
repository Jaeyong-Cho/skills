---
name: pf-dev
description: |
  Grill the user, read the codebase, then implement using TDD — no ADR, no report. Follows existing architecture and VAO layer conventions.
  Use when the user wants to implement something quickly without formal design docs. Triggers: "pf-dev", "just implement", "quick impl", "build this", "implement this feature", "add this".
---

# Simple Implementation

## Step 1: Grill

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: understand what to build and why, grounded in the existing codebase.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

## Step 2: Read the codebase

Read source files relevant to the feature. Understand existing architecture, layer conventions (`../pf/references/layers.md`), entry points, and patterns already in use. Do not design against the grain — follow what's there.

## Step 3: Implement — one behavior at a time

Extract behaviors from the grill conclusions. Implement each:

```
RED:   Write test via public interface → confirm fails
GREEN: Write minimal code → confirm passes
```

Do not write the next test until current is green. Read `../pf-impl/references/tdd-tests.md` for test examples, `../pf-impl/references/tdd-mocking.md` for mocking.

## Step 4: Refactor

Read `../pf-impl/references/tdd-refactoring.md`. Run all tests after each step. Never refactor while RED.

- [ ] Interface narrowable?
- [ ] Complexity hidden or exposed?
- [ ] Duplication to extract?

**Observability** (see `../pf-observe/REFERENCE.md`):
- [ ] Logs key inputs, outputs, and state changes?
- [ ] Errors include enough context to diagnose without a debugger?
- [ ] Existing `observe/` scripts still compatible?

## Step 5: Done

Show what was built. Suggest a commit message.
