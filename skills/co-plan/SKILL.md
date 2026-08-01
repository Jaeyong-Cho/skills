---
name: co-plan
description: Collaborative-plan skill. Sequences a design into ordered TDD steps, fully written by AI like `/fs-plan`, then derives a Review Sequence — the same steps reordered along the code's actual data flow, from entry point to leaf — so a human can follow that order in the finished code and review it. Use when invoked as /co-plan.
disable-model-invocation: true
---

# Co-Plan (Collaborative Plan)

Read `.context/inbox/plan/` — if an existing review-plan (`**Type:** Review-Plan`) covers the same topic, read it and revise it rather than creating a new one.

Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`, `../references/tdd-refactoring.md`.

Build the action sequence the same way `/fs-plan` does: one red-green TDD cycle per unit of work, test step before implementation step, each step naming the exact file, function or class, and expected input/output. Every step is fully written, working code — there are no holes and no human-implementation steps; `/auto-action` writes the entire sequence itself, the same as a regular plan. The Action Sequence's fixed last step is running the project's full build/test suite (not just the tests written in this sequence) and confirming it passes — `/auto-action` gates marking `[x] Test` in Closeout on this passing.

Identify the main flow of the design (its **Scope**): the sequence of calls that carries data from input to output (e.g., input line → parse → evaluate → printed result). This flow, end-to-end, is what the human should be able to trace and review once the code exists. This scope identification is an agent-only working note — never a section in the shown result or the written plan file.

The action sequence above is build order (TDD: leaves are often implemented before the callers that wire them in), which is not the order that best shows a reviewer the flow. Separately derive a **Review Sequence**: every implementation step, reordered top-down along the flow identified earlier — starting at the flow's entry point (e.g., `main` or the client-facing call) and proceeding stage by stage toward the algorithm/leaf stage. For each entry, name the step, its exact file and function/class location, and one or two concrete points to verify there (e.g., "confirm the cache is checked before the DB call and its result short-circuits the DB path"). This lets the human trace input → output the way a reader would, using the finished code itself as the thing being reviewed — the Review Sequence is a reading order over real code, not a checklist of code left for them to write.

If the design is ambiguous or missing something the sequence needs, stop and ask the user to clarify rather than guessing. Otherwise show the user the full sequence and the Review Sequence, and ask for confirmation — do not include the Scope note itself; it's an agent-only working note used to build the Review Sequence, not part of the result. Completion criterion: action sequence is fully ordered, test-before-implementation on every unit of work, every implementation step appears in the Review Sequence top-down along the flow with a concrete verification point, user confirmed.

Derive a kebab-case slug from the topic. If revising an existing review-plan, reuse its slug and timestamp — edit that file in place. Otherwise get a fresh timestamp: run `date +%Y%m%d-%H%M%S`.

Fill in `../template/review-plan.md` with `**Type:** Review-Plan`, the resolved action sequence, and the Review Sequence, in this style `../references/document-style.md`, and write it to `.context/inbox/plan/{timestamp}-{slug}.md`. Leave the fixed Closeout checklist as-is — a review-plan's Closeout has both **Test** (checked by `/auto-action` once it writes the code and the tests pass, same as a regular plan) and **Review** (checked once the human has walked the Review Sequence against the finished code and confirmed each verification point holds — this is a manual read, not something `/auto-action` can detect from the code, so leave it unchecked for the human to confirm).

`mkdir -p .context/inbox/plan` if needed. Tell the user the file path. Next step: `/auto-action`.

**DO NOT START IMPLEMENT**
