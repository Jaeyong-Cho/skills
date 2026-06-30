# Verification Layer Skill Upgrades

## Goal

Each of directing, planning, and evaluate explicitly handles verification thinking — what good/bad/ambiguous looks like, how to observe it in real E2E runs, and why results happened. Skills stay lean by expanding existing steps, not adding new sections or new skills.

## Direction

Upgrade directing, planning, and evaluate in-place by expanding their existing questions/steps:

**Directing** — currently only surfaces the happy path. Expand the grilling step to explicitly surface failure modes and the ambiguous middle zone. The direction output file must capture what "bad looks like" and "ambiguous looks like", not just what success looks like.

**Planning** — currently defaults to unit tests because its references are unit-test-heavy. Expand the planning output format to require, for each goal from directing:
- Observation method: is this binary pass/fail, a numeric metric range, or a qualitative rubric?
- Runtime behavior checkpoints: what to observe mid-execution (logs, intermediate state), not just the final result.
- E2E / test-loop command: a single repeatable command or script that sets up the real-world scenario and runs it end-to-end. This is the test-loop target — not a unit test.

**Evaluate** — currently prints pass/fail counts and statistics, stops there. Expand to require pattern analysis and root cause reasoning: what pattern do the results form? What is the likely cause of that pattern? Which failures are expected (by directing's criteria) and which are surprising?

## Constraints

- No new skills added to the pipeline.
- No new structural sections in skill files — expand existing grilling questions and existing output format steps only.
- Skills must stay short enough that the agent actually executes them fully.
- Test-loop E2E and verify/observe scripts are the same thing — one command per scenario.

## Out of Scope

- New standalone verification or observation skill.
- New pipeline steps between directing → planning → evaluate.
- Separate verification output templates or linked files across skills.
