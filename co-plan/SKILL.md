---
name: co-plan
description: Collaborative-plan skill. Sequences an ADR's design into ordered TDD steps and marks, per implementation step, which parts are holes for human implementation vs working code. Use when invoked as /co-plan.
disable-model-invocation: true
---

# Co-Plan (Collaborative Plan)

Read the draft ADR to plan from `.context/adr/` — a draft is named `{timestamp}-{slug}.md` (a merged one has `.merged.md` and is no longer the active target). If multiple drafts exist, list them and ask the user which to use. If none exist, tell the user to run `/archi` first and stop.

Read `.context/plan/` — if an existing self-plan (`**Type:** Self-Plan`) covers the same topic, read it and revise it rather than creating a new one.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`, `../references/tdd-refactoring.md`, `../references/todo-hole.md`.

Build the action sequence the same way `/fs-plan` does: one red-green TDD cycle per unit of work, test step before implementation step, each step naming the exact file, function or class, and expected input/output. Test steps are never holed — tests are always complete and AI-written.

Read the ADR's Decision (Before/After) to identify the main flow: the sequence of calls that carries data from input to output (e.g., input line → parse → evaluate → printed result). This flow, end-to-end, is what the human should understand.

For each implementation step, a hole is never a whole function body and never a stage's full algorithm — it's one or a few specific lines. There are two kinds, and both are judgment calls, not a rigid checklist — recommend what best serves understanding:

1. **Flow-connecting hole:** the line(s) where a stage calls the next stage of the flow and uses the returned value (e.g., `main()` calling the use case and printing its result; a use case calling the parser then the evaluator).
2. **In-stage key-change hole:** the one line that is a stage's own core decision or transformation, even when it doesn't call another stage. If the stage has multiple similar branches (e.g., several operators, several conditions), hole exactly one representative branch's line — the rest stay working code, giving the human a pattern to generalize from.

Everything else is working code, always: the rest of a stage's own algorithm (setup, loops, the non-representative branches), and infrastructure (prompts, exit handling, try/except structure, error message strings).

To tell hole from working, ask: does this line carry the flow's data to the next stage, or is it the one line that embodies this stage's core decision? If neither, it's working code.

For each hole, record its TODO text following `todo-hole.md`.

**Budget:** across the whole sequence, holed lines should be roughly 30% of implementation lines, working code the other ~70%. This is a plan-wide budget, not a per-step cap — some steps may be all working code, a few may carry more holes, as long as the total lands near 30/70. After building the sequence, tally holed vs. working lines; if holes run well past 30%, cut back to the most important flow-connecting and key-change lines and demote the rest to working code.

The action sequence above is build order (TDD: leaves are often implemented before the callers that wire them in), which is not the order that best teaches the flow. Separately derive a **Recommended Human Work Order**: every implementation step that carries a hole, reordered top-down along the flow identified earlier — starting at the flow's entry point (e.g., `main` or the client-facing call) and proceeding stage by stage toward the algorithm/leaf stage. This lets the human trace input → output the way a reader would, jumping directly between hole steps regardless of where they fall in build order. Reference each entry by its step number and name; omit steps with no hole, since those are already complete working code.

If the ADR is ambiguous or missing something the sequence needs, stop and send the user back to `/archi` rather than guessing. Otherwise show the user the full sequence, including each implementation step's hole/working breakdown, the overall hole/working tally, and the Recommended Human Work Order, and ask for confirmation. Completion criterion: action sequence is fully ordered, test-before-implementation on every unit of work, every implementation step has its hole/working decision recorded, the ~30/70 budget holds, the Recommended Human Work Order lists every holed step top-down along the flow, user confirmed.

Derive a kebab-case slug from the topic — reuse the ADR's slug so the plan pairs with it. If revising an existing self-plan, reuse its timestamp too — edit that file in place. Otherwise get a fresh timestamp: run `date +%Y%m%d-%H%M%S`.

Fill in `../template/self-plan.md` with the ADR's path, `**Type:** Self-Plan`, the resolved action sequence (with hole/working annotations on implementation steps), and the Recommended Human Work Order, in this style `../references/document-style.md`, and write it to `.context/plan/{timestamp}-{slug}.md`. Leave the fixed Closeout checklist as-is.

`mkdir -p .context/plan` if needed. Tell the user the file path. Next step: `/auto-action`.

**DO NOT START IMPLEMENT**
