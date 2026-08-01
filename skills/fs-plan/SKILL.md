---
name: fs-plan
description: Full self-plan skill. Sequences a design into ordered implementation steps as TDD cycles, then writes a plan fully written and executed by AI. Use when invoked as /fs-plan.
disable-model-invocation: true
---

# Fs-Plan (Full Self-Plan)

Read `.context/inbox/plan/` — if an existing plan covers the same topic, read it and revise it rather than creating a new one.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`, `../references/tdd-refactoring.md`.

Build the action sequence directly from the design and its verification criteria:

Sequence each unit of work as its own red-green cycle: a step to write the failing test first (tdd-tests.md for what makes a good test, tdd-mocking.md for when to mock), then a step to implement the minimum that turns it green (tdd.md) — never implementation before its test. Each step: one concern, one logical unit, describable without "and", and concrete enough for a junior developer to execute without making a design decision — name the exact file, function or class, and expected input/output, not just the goal. The Action Sequence's fixed last step is running the project's full build/test suite (not just the tests written in this sequence) and confirming it passes — `/auto-action` gates marking `[x] Test` in Closeout on this passing. The template's fixed Closeout checklist (test) always follows as the last step.

Derive a kebab-case slug from the topic. If revising an existing plan, reuse its slug and timestamp — edit that file in place. Otherwise get a fresh timestamp: run `date +%Y%m%d-%H%M%S`.

Fill in `../template/plan.md` with the resolved action sequence in this style `../references/document-style.md`, and write it to `.context/inbox/plan/{timestamp}-{slug}.md`. Leave the fixed Closeout checklist as-is.

`mkdir -p .context/inbox/plan` if needed. Tell the user the file path. Next step: `/auto-action`.

**DO NOT START IMPLEMENT**
