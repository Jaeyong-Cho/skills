---
name: evaluate-solution
description: After @skills/execute-solution, re-check the real current state against the problem's original Desired state — don't just trust the report's green tests — to verdict Resolved/Partially Resolved/Unresolved, name any remaining gap, and write feedback recommending the next cycle (or none). Fifth and last stage of the intent-to-cycle skill set. Invoke as /evaluate-solution.
disable-model-invocation: true
---

# Evaluate Solution

A green test in `@skills/do-plan`'s report is evidence the plan's acceptance criteria passed once, not proof the original problem is actually closed — this skill re-checks for real and closes the loop with feedback.

1. **Pick the problem.** Take the `problem-NN.md` the user names, or the newest one with `Status: executed`/`partially-executed` under the confirmed `problems/` directory if none named — **MUST ASK** which if more than one candidate exists. Follow its Status pointer (added by `@skills/execute-solution`) to the plan and `{plan-file}.report.md`. **MUST NOT** proceed if that pointer is missing — `@skills/execute-solution` hasn't run yet, say so instead of guessing. Completion criterion: the problem's Desired state/Evaluation criteria and the report's acceptance-criteria results, each traceable to a file.

2. **Read the execution result.** Pull the report's acceptance-criteria pass/fail table and "what changed" list as-is — this is evidence already produced, not re-derived.

3. **Re-check the real current state.** Dispatch a sub-agent to verify, right now, whether the codebase/environment actually matches the problem's original Desired state — grep/read/run a read-only inspection command, per `../references/subagents-vs-skills.md`. Don't stop at "the report says pass" — code can drift after a commit, and a green test can miss what the Desired state actually asked for. Cite file:line or command output for every claim, same as `@skills/define-problem`'s Current state step.

4. **Compute the remaining gap.** Diff step 3's fresh current state against the Desired state — same method as `@skills/define-problem`'s Gap step. An empty diff means fully closed; anything else is a named remaining gap, not silently dropped.

5. **Verdict.** State directly, with reasoning citing steps 2-4's evidence: `Resolved` (no remaining gap), `Partially Resolved` (some Evaluation criteria hold, a real gap remains), or `Unresolved` (none of it holds up). Most calls here are a straight readout of step 4 — only ask the user a single `❓`/`➡️` question per `../references/question-format.md` when the verdict is a genuine judgment call (criteria technically pass but the result doesn't serve the intent's original Need/Pain, per its `intents.md`) — a decision, not a fact.

6. **Feedback.** One short paragraph: what was learned, why any gap remains (if it does), and the recommended next action — re-run `@skills/define-problem` on the remaining gap, re-run `@skills/find-solutions` for an alternate option, or "done, no further cycle needed" for a clean Resolved verdict. This is a recommendation, not an auto-triggered next step — the human decides whether to start the next cycle.

7. **Write it.** **MUST ASK** confirmation of the directory first, per `../references/question-format.md`'s ❓/➡️ format — recommend the current directory (`./evaluations/`) as the default, unless the user asks to file it under the wiki instead, in which case read `../references/research-topic-directory.md` first and confirm `{NN}-{slug}` the same way (reuse the topic directory already confirmed this session, without re-asking). Once confirmed, write to `./evaluations/{nn}-{slug}.md` (creating `evaluations/` if needed) or `{NN}-{slug}/evaluations/{nn}-{slug}.md` under `~/wiki/today/research/` — `{nn}` the next zero-padded sequence number inside `evaluations/` (count existing files there; starts at `01`).

   The file is an OKF document per `../references/document-style/frontmatter.md`: five-field frontmatter (`type: Research Evaluation`, `title`, `description`, `tags`, `timestamp`; `resource` omitted unless one genuinely applies), plus `derived_from: {problem-NN.md path}` and `evidence_from: {report path}` lines under the frontmatter. Body sections, in order: Execution result, Re-checked current state, Remaining gap, Verdict, Feedback.

8. **Lint it.** Run `python3 ../to-kb/scripts/lint_kb.py --plain {path}` (relative to this skill's directory). Fix every reported error and re-run until clean.

9. **Close the loop.** Update the source `problem-NN.md`'s Status to the step 5 verdict (`resolved`/`partially-resolved`/`unresolved`), with a one-line pointer to this evaluation file. Don't rewrite the problem's other sections — this is a status update, not a re-derivation.

Completion criterion: the evaluation file exists at the confirmed path, carries valid OKF frontmatter and its two reference lines, `lint_kb.py --plain` is clean, and the problem file's Status reflects the real verdict with a pointer to it.

Once complete, tell the user the file path and the verdict, and state the Feedback's recommended next action plainly so the human can decide whether to start the next cycle.
