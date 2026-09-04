---
name: define-problem
description: Dispatch sub-agents to find the real current state, then compare it against an intents.md's desired state to compute the gap, evaluation criteria, and boundary for each resulting problem. Writes one problem-NN.md per independently-evaluable gap. Second stage of the intent-to-cycle skill set. Invoke as /define-problem.
disable-model-invocation: true
---

# Define Problem

Turn an `intents.md`'s desired state into one or more concrete problems by finding the real current state, not guessing it.

1. **Read the intent.** Take the `intents.md` the user names, or the newest one under the current directory / today's `~/wiki/today/research/` tree if none is named — **MUST ASK** which one if more than one candidate exists and it's not obvious. Pull its Desired outcome and Constraints sections as-is; this is the desired state, not re-derived. Completion criterion: a stated desired state and constraint list, each traceable to that file.

2. **Dispatch sub-agents for the current state.** For every part of the desired state, dispatch a sub-agent to find the real current state by inspecting the codebase/environment/docs (grep/read/run a read-only command), per `../references/subagents-vs-skills.md` — on pi, that's the `fact-finder` agent, named explicitly, never a bare dispatch (`../references/pi-subagents.md`). Never ask the user for a fact a sub-agent can find. Record each finding with its file:line or command-output evidence attached — never "should"/"probably"/"likely". Completion criterion: every part of the desired state has a current-state finding with cited evidence.

3. **Run an experiment where reading can't settle it.** A claim only observable by actually running something (not by reading) goes to `@skills/experiment` instead of being guessed — dispatch a sub-agent to run it (plan the cheapest experiment, run it for real, report back a verdict), same as step 2's dispatch — on pi, that's the `experimenter` agent (`../references/pi-subagents.md`) — and use that verdict as the evidence for that finding.

4. **Compute the gap.** Diff the current state (steps 2-3) against the desired state (step 1) — one gap per point where they diverge. A desired-state point the current state already satisfies is not a gap; drop it, don't write a problem for something already true. Completion criterion: every divergence is a named gap, every match is explicitly dropped (not silently ignored).

5. **Set evaluation criteria and boundary per gap.** For each gap, state directly, with reasoning: the observable check that would confirm it closed (Evaluation criteria — a value, a test, a visible state), and the minimum independently-evaluable slice of the gap this one problem covers (Boundary) — a gap too large for one Evaluation criterion splits into more than one problem, don't force it into one. Most calls here are Low uncertainty and get stated directly as a `Decision:` line with its reasoning. Only where a call is genuinely High uncertainty (per `../references/grill-impact.md`'s definition) does it become a single `❓`/`➡️` question, per `../references/question-format.md` — one question per uncertain call, not a full interview round.

6. **Write it.** One file per resulting problem from step 5.

   **MUST ASK** confirmation of the directory first, per `../references/question-format.md`'s ❓/➡️ format — recommend the current directory (`./problems/`) as the default, unless the user asks to file it under the wiki instead, in which case read `../references/research-topic-directory.md` first and confirm `{NN}-{slug}` the same way (reuse the topic directory `intents.md` was confirmed under, if this session already knows it, without re-asking). Once confirmed, write each problem to `./problems/{nn}-{slug}.md` (creating `problems/` if needed) or `{NN}-{slug}/problems/{nn}-{slug}.md` under `~/wiki/today/research/` — `{nn}` the next zero-padded sequence number inside `problems/` (count existing files there; starts at `01`).

   Each file is an OKF document per `../references/document-style/frontmatter.md`: six-field frontmatter (`type: Research Problem`, `title`, `description`, `tags`, `timestamp`; `resource` omitted unless one genuinely applies), plus a `derived_from: {intents.md path}` line under the frontmatter so the problem traces back to the intent it came from. Body sections, in order: Desired state, Current state, Gap, Evidence, Evaluation criteria, Constraints, Boundary, Status (`open` at creation).

7. **Lint each file.** Run `python3 ../to-kb/scripts/lint_kb.py --plain {path}` (relative to this skill's directory) on every problem file written in step 6 — checks the frontmatter carries all five plain-OKF fields and the file isn't oversized. Fix every reported error and re-run until clean.

Completion criterion: every problem file exists at the confirmed path, carries valid OKF frontmatter and a `derived_from` line, `lint_kb.py --plain` is clean on each, every body section is backed by real evidence (steps 1-4) or a recorded decision with reasoning (step 5), nothing left silently assumed.

Once complete, tell the user the file path(s). Next step in this skill set is `@skills/find-solutions`.
