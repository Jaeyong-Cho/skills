---
name: fs-plan
description: Full self-plan skill. Sequences an ADR's design into ordered implementation steps as TDD cycles, then writes a plan fully written and executed by AI. Use when invoked as /fs-plan.
disable-model-invocation: true
---

# Fs-Plan (Full Self-Plan)

Read the draft ADR to plan from `.context/adr/` — a draft is named `{timestamp}-{slug}.md` (a merged one has `.done.md` and is no longer the active target). If multiple drafts exist, list them and ask the user which to use. If none exist, tell the user to run `/archi` first and stop.

Read `.context/plan/` — if an existing plan covers the same topic, read it and revise it rather than creating a new one.

Use this for a new plan or to resequence after the ADR changes.
Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`, `../references/tdd-refactoring.md`.

The ADR already resolved every open question — architecture, design, observability, test-loop, and verification criteria — so this isn't a grill; sequencing is mechanical, not exploratory. Build the action sequence directly from the ADR's Decision, Observability, Test-Loop Design, and Verification Criteria:

Sequence each unit of work as its own red-green cycle: a step to write the failing test first (tdd-tests.md for what makes a good test, tdd-mocking.md for when to mock), then a step to implement the minimum that turns it green (tdd.md) — never implementation before its test. Each step: one concern, one logical unit, describable without "and", and concrete enough for a junior developer to execute without making a design decision — name the exact file, function or class, and expected input/output, not just the goal. The template's fixed Closeout checklist (test) always follows as the last step.

If the ADR is ambiguous or missing something the sequence needs, stop and send the user back to `/archi` rather than guessing. Otherwise show the user the full sequence and ask for confirmation. Completion criterion: action sequence is fully ordered, test-before-implementation on every unit of work, no step leaves a design decision to whoever executes it, user confirmed.

Derive a kebab-case slug from the topic — reuse the ADR's slug so the plan pairs with it. If revising an existing plan, reuse its timestamp too — edit that file in place. Otherwise get a fresh timestamp: run `date +%Y%m%d-%H%M%S`.

Fill in `../template/plan.md` with the ADR's path and the resolved action sequence with this style `../references/document-style.md`, and write it to `.context/plan/{timestamp}-{slug}.md`. Leave the fixed Closeout checklist as-is.

`mkdir -p .context/plan` if needed. Tell the user the file path. Next step: `/auto-action`.

**DO NOT START IMPLEMENT**
