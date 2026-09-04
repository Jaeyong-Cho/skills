---
name: execute-solution
description: Apply a find-solutions Decision for real — feed it and its source problem's Evaluation criteria into @skills/to-plan (already-grilled input, no re-interview), then run @skills/do-plan to build it, verify it, and commit it. Updates the solution/problem Status once done. Fourth stage of the intent-to-cycle skill set. Invoke as /execute-solution.
disable-model-invocation: true
---

# Execute Solution

Turn a picked solution into a real change instead of re-deriving what to build — `@skills/to-plan` and `@skills/do-plan` already do planning and execution well; this skill only wires their input to what `@skills/find-solutions` already decided.

1. **Pick the solution.** Take the `solutions-NN.md` the user names, or the newest one with `Status: selected` under the confirmed `solutions/` directory if none named — **MUST ASK** which if more than one candidate exists. **MUST NOT** proceed if its Status isn't `selected` (an empty or "deferred" Decision section means `@skills/find-solutions` isn't done yet — say so instead of guessing a pick). Read its Decision section and follow `derived_from` to the source `problem-NN.md`. Completion criterion: one selected option, and the problem's Desired state/Evaluation criteria/Constraints, each traceable to a file.

2. **Draft the plan via `@skills/to-plan`.** Run it with this session's already-settled input, per its own step 1's "named target" path — the target is the Decision from step 1, already grilled through `intent-grill-me` → `define-problem` → `find-solutions`, so **skip** `to-plan`'s fallback of running `dev-grill-me`/`req-grill-me` first. Seed its draft directly:
   - **Acceptance criteria** — the problem's Evaluation criteria, rewritten as Given–When–Then rows per `../references/requirement-engineering.md`, each with a real Verification Method.
   - **Constraints/Out of scope** — the problem's Constraints and Boundary sections, carried forward as-is.
   - **Action items** — what the selected option's Decision describes, decomposed and abstraction-tagged per `to-plan`'s own step 8 rule.

   Every other `to-plan` step (worktree, build/test commands, Deferred items, Assertions, Commit message draft) runs exactly as that skill defines. Completion criterion: `to-plan` reports a written plan file path.

3. **Run `@skills/do-plan`** on that plan file — builds each action item for real, verifies acceptance criteria against the real repo state, commits only after the human confirms, and writes the report. Completion criterion: `do-plan` reports a report file path (or a named blocker).

4. **Close the loop.** Update the source `solutions-NN.md`'s Status to `executed` and add a one-line pointer to the plan and report paths from step 2/3; update the source `problem-NN.md`'s Status to `executed` (or `partially-executed` if `do-plan` left any action item or acceptance criterion blocked/failing) with the same pointer. Don't rewrite either file's other sections — this is a status update, not a re-derivation.

Completion criterion: the plan is executed (or its blocker is named), the report exists, and both the solution and problem files reflect the real outcome with a pointer to it.

Once complete, tell the user the plan and report file paths, and paste `do-plan`'s "Try it yourself" QA checklist into the session. Next step in this skill set (evaluate) is not built yet — say so rather than inventing it.
