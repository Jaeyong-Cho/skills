---
name: self-planning
description: Self-planning skill. Sequences an ADR's design into ordered TDD steps and marks, per implementation step, which parts are holes for human implementation vs working code. Use when invoked as /self-planning.
disable-model-invocation: true
---

# Self-Planning

Read the draft ADR to plan from `.context/adr/` — a draft is named `{timestamp}-{slug}.md` (a merged one has `.merged.md` and is no longer the active target). If multiple drafts exist, list them and ask the user which to use. If none exist, tell the user to run `/archi` first and stop.

Read `.context/plan/` — if an existing self-plan (`**Type:** Self-Plan`) covers the same topic, read it and revise it rather than creating a new one.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`, `../references/tdd-refactoring.md`, `../references/todo-hole.md`.

Build the action sequence the same way `/planning` does: one red-green TDD cycle per unit of work, test step before implementation step, each step naming the exact file, function or class, and expected input/output. Test steps are never holed — tests are always complete and AI-written.

For each implementation step, apply these five rules to decide, block-by-block, what is a hole and what is working code. Decide this while building the sequence, not while writing the actual code later:

1. **Remove happy-path logic** — keep error-handling structure, hole the core business flow
2. **One representative example per multiple case** — if there are multiple similar branches (e.g., multiple operators), hole only one representative case; human understands the pattern and applies it to others
3. **Hole the decision logic** — show *when* conditions are true/false, *what* triggers each path
4. **Hole the architectural flow** — how components call each other, the orchestration sequence, not the internal details of those calls
5. **Hole the transformations** — where data flows and changes shape, not the syntax of how it changes

**Priority:** Business logic flow (orchestration, transformations, decision paths) takes priority over error handling details (error message strings, exception catching structure).

**Working code:** Error handling infrastructure (try/catch blocks, exception catching), error message strings, language details (regex patterns, syntax).

**Holes:** Orchestration (component calls and sequence), transformations (data flow and changes), decision logic (when conditions), representative examples. For each hole, record its TODO text following `todo-hole.md`.

If the ADR is ambiguous or missing something the sequence needs, stop and send the user back to `/archi` rather than guessing. Otherwise show the user the full sequence, including each implementation step's hole/working breakdown, and ask for confirmation. Completion criterion: action sequence is fully ordered, test-before-implementation on every unit of work, every implementation step has its hole/working decision recorded, user confirmed.

Derive a kebab-case slug from the topic — reuse the ADR's slug so the plan pairs with it. If revising an existing self-plan, reuse its timestamp too — edit that file in place. Otherwise get a fresh timestamp: run `date +%Y%m%d-%H%M%S`.

Fill in `../template/self-plan.md` with the ADR's path, `**Type:** Self-Plan`, and the resolved action sequence (with hole/working annotations on implementation steps) in this style `../references/document-style.md`, and write it to `.context/plan/{timestamp}-{slug}.md`. Leave the fixed Closeout checklist as-is.

`mkdir -p .context/plan` if needed. Tell the user the file path. Next step: `/auto-action`.

**DO NOT START IMPLEMENT**
