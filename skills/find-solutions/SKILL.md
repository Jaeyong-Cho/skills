---
name: find-solutions
description: For one or more problem-NN.md files, dispatch sub-agents to explore how to reduce the stated Gap — reuse first, then alternatives — running @skills/experiment on anything feasibility-uncertain, then compare options against the problem's Evaluation criteria/Constraints and recommend one. Writes one solutions-NN.md per problem, one or more options each. Third stage of the intent-to-cycle skill set. Invoke as /find-solutions.
disable-model-invocation: true
---

# Find Solutions

Mission for each problem: **reduce the Gap** it states — not rebuild anything the problem's own Current state already shows is fine.

1. **Read the problem(s).** Take the `problem-NN.md` file(s) the user names, or every `Status: open` problem under the confirmed `problems/` directory if none named — **MUST ASK** which if more than one candidate directory exists and it's not obvious. For each, read Desired state, Current state, Gap, Evidence, Evaluation criteria, Constraints, Boundary in full; the rest of this skill runs once per problem. Completion criterion: one Gap statement, Evaluation criteria, and Constraints list per problem, each traceable to its file.

2. **Reuse check, first.** Before inventing anything, dispatch a sub-agent to check whether the codebase/environment already has something that closes (or partly closes) the Gap — an existing helper, pattern, config, or stdlib/native feature already in use elsewhere, per the ladder's "already in this codebase?" / "stdlib?" / "native feature?" rungs. Cite file:line. A hit here is still a real option ("reuse X at file:line") and often the cheapest one — don't discard it in favor of something more elaborate without reason.

3. **Dispatch sub-agents for the other candidates.** For each distinct approach worth considering, dispatch a sub-agent to explore it independently (code investigation, docs research, prior art), per `../references/subagents-vs-skills.md`, and report back: description, how it closes the Gap, fit against Evaluation criteria, fit against Constraints, cost/risk, and evidence (file:line, doc reference, or prior art) — never a claim asserted without one. An option whose evidence is "should work" rather than "does work" is a hypothesis, not a settled option yet.

4. **Run an experiment where reading can't settle feasibility.** An option only verifiable by actually running something (a spike, prototype, benchmark) goes to `@skills/experiment` instead of being guessed — dispatch a sub-agent to run it, same as step 2/3's dispatch, and use its verdict as that option's evidence.

5. **Compare and recommend.** Score every option side by side against the problem's Evaluation criteria and Constraints, evidence cited for each. State the recommended option (➡️) with reasoning — the smallest option that satisfies the Evaluation criteria wins ties, not the most thorough one. If more than one option is genuinely defensible and the pick isn't obvious, ask the user one `❓`/`➡️` question per `../references/question-format.md` — a decision, not a fact, never guessed.

6. **Write it.** One file per problem.

   **MUST ASK** confirmation of the directory first, per `../references/question-format.md`'s ❓/➡️ format — recommend the current directory (`./solutions/`) as the default, unless the user asks to file it under the wiki instead, in which case read `../references/research-topic-directory.md` first and confirm `{NN}-{slug}` the same way (reuse the topic directory `problems/` was confirmed under, if this session already knows it, without re-asking). Once confirmed, write each to `./solutions/{nn}-{slug}.md` (creating `solutions/` if needed) or `{NN}-{slug}/solutions/{nn}-{slug}.md` under `~/wiki/today/research/` — `{nn}` the next zero-padded sequence number inside `solutions/` (count existing files there; starts at `01`).

   Each file is an OKF document per `../references/document-style/frontmatter.md`: five-field frontmatter (`type: Research Explore`, `title`, `description`, `tags`, `timestamp`; `resource` omitted unless one genuinely applies), plus a `derived_from: {problem-NN.md path}` line under the frontmatter. Body sections, in order: Mission (the source problem's Gap, restated), Options (one subsection per option — description, evidence, fit, cost/risk), Comparison, Decision (the selected option and reasoning, or "deferred" if the user didn't pick one), Status (`selected` once one option is chosen, `open` otherwise).

7. **Lint each file.** Run `python3 ../to-kb/scripts/lint_kb.py --plain {path}` (relative to this skill's directory) on every file written in step 6. Fix every reported error and re-run until clean.

Completion criterion: every solutions file exists at the confirmed path, carries valid OKF frontmatter and a `derived_from` line, `lint_kb.py --plain` is clean on each, every option is backed by real evidence (steps 2-4) and the Decision section reflects a real choice or an explicit deferral, nothing left silently assumed.

Once complete, tell the user the file path(s). Next step in this skill set (execute/evaluate) is not built yet — say so rather than inventing it.
