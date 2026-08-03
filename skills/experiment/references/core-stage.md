# Core stage

Read only when you've reached this stage.

**Read the explore stage's output first.** `questions/{slug}/.context/explore/...` is the default source for codebase/domain facts here (grilling background, method design). Treat it as sufficient — don't independently Read, Grep, or re-dispatch `/explore` to double-check it. Only go back to `/explore`, for that one gap, if grilling or method design surfaces something the evidence genuinely doesn't cover.

**Grill the user.** Run `grilling` on the request, with the explore evidence and root `goal.md` (states the goal and this question's own heading) as background. Get: the real intent, the real question (may not match the wording), and why it's worth an experiment. `run_in_background: false`. Save output to `questions/{slug}/.context/grilling/`.

**Frame the hypothesis.** Restate the real question as one falsifiable claim, plus the observations that would confirm or refute it. Write `questions/{slug}/hypothesis.md`.

**Design the method before touching anything.** **MUST DISPATCH** a claude-sonnet-5 subagent, briefed with the explore evidence and hypothesis.md directly, to decide what varies, what stays fixed (control/baseline, if comparative), and what gets measured and how — via `/p4d`. Per `/p4d`'s own convention, this writes `questions/{slug}/method/index.md` (objective, prerequisites, and the group table) plus one `questions/{slug}/method/group-{n}.md` per parallel-execution group — not a single flat file — before executing.

**Execute and collect raw results.** Read `method/index.md`'s group table. For each dependency wave (groups with no unmet `depends_on`, dispatched together; wait for a wave to finish before the next), **MUST DISPATCH** one claude-haiku-4.5 subagent per group, each given only that group's `method/group-{n}.md` — via `/work`, actual commands and output, never fabricated. Each subagent saves its raw results under `questions/{slug}/raw/group-{n}/` (namespaced per group so concurrent dispatches never write over each other). `run_in_background: false` for each wave.

**Analyze against the hypothesis.** Compare the raw results to the confirming/refuting observations and reach a verdict — supported, refuted, or inconclusive (state why if inconclusive).

## Gate — resolve here, or continue?

Does the verdict, backed by the results, resolve the question without a visual?

- **Yes:** go straight to `../SKILL.md`'s Publish, no gallery. Mark Visualizations "Not built — not needed to resolve the question."
- **No** (subtle, comparative across runs, or needs to be seen to be trusted): continue to `../references/viewpoints-stage.md`, then Publish.
