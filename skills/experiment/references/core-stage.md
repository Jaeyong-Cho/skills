# Core stage

Read only when you've reached this stage. Runs one **attempt** at a time — `questions/{slug}/experiments/{n}-{angle-slug}/` — and loops back to itself via the next-attempt gate until an attempt resolves the question or the budget runs out. `n` is only run order, not a cost ladder: tier is picked fresh each attempt based on what that attempt's angle needs. A question commonly resolves through two or three *cheap* attempts at different angles and never needs `full` at all; `full` is for when a specific angle needs more rigor than one quick check can give it, not "whatever attempt 2 defaults to."

**Read prior output first.** `questions/{slug}/.context/explore/...` is the default source for codebase/domain facts (grilling background, method design) across every attempt — treat it as sufficient, don't independently Read/Grep/re-dispatch `/explore` to double-check it. From attempt 2 onward, also read every earlier `experiments/{n}-*/result.md` — each states what it tested, its verdict, and why it didn't close the question; the next attempt is briefed on all of this so it never repeats a tested angle. Only go back to `/explore`, for that one gap, if grilling or method design surfaces something the evidence genuinely doesn't cover.

**Grill the user — attempt 1 only.** Run `grilling` on the request, with the explore evidence and root `goal.md` as background. Get: the real intent, the real question (may not match the wording), and why it's worth an experiment. `run_in_background: false`. Save output to `questions/{slug}/.context/grilling/` (shared across all attempts on this question). From attempt 2 onward, reuse it as-is — re-grill only if the next-attempt gate below decided the prior attempt's angle was based on a wrong premise about intent, not just an execution gap.

**Pick this attempt's tier and angle — every attempt, not just the first.**
- `tier: cheap` — a single quick, minimal check, run by **one claude-haiku-4.5 subagent** (never inline in the orchestrating thread — that thread runs on a more expensive model and a one-shot check is exactly the work a cheap model handles fine), no `/p4d` planning, no haiku swarm. Default whenever *this attempt's angle* is checkable with one shot — true for most angles, first or fourth alike.
- `tier: full` — the p4d-planned, haiku-swarm-executed procedure below. Use only when *this specific angle* is inherently comparative/causal at a scale a single quick check can't cover (needs multiple runs, controls, statistical power) — whether that's true on attempt 1 or only becomes clear after a cheap attempt on that same angle came back inconclusive for lack of rigor. Never pick `full` just because `n > 1`.
- `angle` — one line naming what this attempt specifically tests, distinct from every prior attempt's angle (see next-attempt gate). Slug it for the directory name, e.g. `2-cold-start-latency`. Most questions are multi-faceted enough that several angles, each cheap, is the expected shape — not a consolation prize before "the real" full-tier attempt.

**Frame the hypothesis.** Restate this attempt's angle as one falsifiable claim, plus the observations that would confirm or refute it. Write `questions/{slug}/experiments/{n}-{angle-slug}/hypothesis.md`.

**Design the method before touching anything.**
- `tier: cheap` — decide inline what the one check is and what result would confirm/refute it (this framing step is judgment, stays in the orchestrating thread); the check itself still goes to the haiku subagent below, not executed here.
- `tier: full` — **MUST DISPATCH** a claude-sonnet-5 subagent, briefed with the explore evidence and this attempt's `hypothesis.md` directly, to decide what varies, what stays fixed (control/baseline, if comparative), and what gets measured and how — via `/p4d`. Per `/p4d`'s own convention, this writes `experiments/{n}-{angle-slug}/method/index.md` (objective, prerequisites, group table) plus one `method/group-{n}.md` per parallel-execution group.

**Execute and collect raw results.**
- `tier: cheap` — **MUST DISPATCH** one claude-haiku-4.5 subagent, briefed with the check decided above (and the explore evidence it needs), to run it and report back actual output, not a summary. Save that output to `experiments/{n}-{angle-slug}/raw/output.md`. `run_in_background: false`.
- `tier: full` — read `method/index.md`'s group table. For each dependency wave (groups with no unmet `depends_on`, dispatched together; wait for a wave to finish before the next), **MUST DISPATCH** one claude-haiku-4.5 subagent per group, each given only that group's `method/group-{n}.md` — via `/work`, actual commands and output, never fabricated. Each subagent saves raw results under `experiments/{n}-{angle-slug}/raw/group-{n}/`. `run_in_background: false` for each wave.

**Analyze against the hypothesis.** Compare the raw results to the confirming/refuting observations and reach a verdict — supported, refuted, or inconclusive (state why if inconclusive). Write `experiments/{n}-{angle-slug}/result.md`: angle, tier, verdict, the reasoning, and — if inconclusive or superseded by a later attempt — what a next attempt would need to cover.

## Next-attempt gate — resolve, try another attempt, or stop?

- **This attempt's verdict resolves the real question, backed by its results:** done testing. Continue to this stage's viewpoints gate below.
- **Inconclusive for lack of rigor on this same angle** (right angle, but `tier: cheap` didn't have the power/samples/control to trust the result): next attempt, same angle, step up to `tier: full`.
- **Inconclusive, contradicted, or simply not yet covering the whole question** (measured the wrong thing, missed a confound, or this angle was only one perspective of a multi-part question): next attempt, new angle — pick whichever tier that new angle needs (usually still `cheap`; most next-angle attempts don't need to be more expensive than the last, just different).
- **Budget check:** default cap is 3 attempts per question. Before starting a 4th, stop and ask the user via `AskUserQuestion` whether to keep going (and on what angle) or close the question as inconclusive with every attempt documented — never loop silently past the cap.
- **All attempts exhausted or user says stop:** continue to this stage's viewpoints gate below with whatever the last/strongest attempt found; report.md's verdict reflects that state honestly (e.g. `Inconclusive`), it does not overstate resolution.

### Viewpoints gate

Does the resolving (or final) attempt's verdict, backed by its results, resolve the question without a visual?

- **Yes:** go straight to `../SKILL.md`'s Publish, no gallery. Mark Visualizations "Not built — not needed to resolve the question."
- **No** (subtle, comparative across runs/attempts, hard to follow from the result text/numbers alone, or needs to be seen to be trusted): ask the user via `AskUserQuestion` whether to build a gallery before Publish. If yes, continue to `../references/viewpoints-stage.md`, then Publish; if no, go to Publish and mark Visualizations "Not built — user declined."
