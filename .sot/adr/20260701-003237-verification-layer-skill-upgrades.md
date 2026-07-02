# ADR: Verification Layer Skill Upgrades

**Date:** 2026-07-01

## Context

Directing, planning, and evaluate skills lack verification thinking. Directing only captures the happy path — no failure criteria defined. Planning defaults to unit tests because it reads TDD references, skipping E2E / test-loop design. Evaluate prints pass/fail statistics without pattern analysis or root cause reasoning. The fix is to upgrade each skill in-place by expanding existing steps, not adding new skills or pipeline stages.

## Decision

- **Directing**: add a new grill question for failure modes between Goal and Decision space; add `## Failure Criteria` and `## Ambiguous Zone` to the output template.
- **Planning**: remove TDD reference reads (tdd.md, tdd-tests.md, tdd-mocking.md) from planning — they belong in action/auto-action where implementation happens. Rewrite steps 3–6 to include runtime checkpoints, per-scenario observation method classification, and explicit links back to directing's Failure Criteria.
- **Evaluate**: add a pattern analysis step after per-scenario comparison; add `## Patterns` to the output format.
- **Action / Auto-Action**: add TDD reference reads so implementation skills retain that context.
- No new skills. No new pipeline stages. Expand existing steps only.

## Design

**Directing** grill questions (renumbered):
1. Goal
2. **Failure modes** ← new: what does bad look like? what is the ambiguous middle zone?
3. Decision space
4. Constraints
5. Direction

**Directing** output template — new sections added:
```
## Failure Criteria
## Ambiguous Zone
```

**Planning** reference reads — remove:
- `../references/tdd.md`
- `../references/tdd-tests.md`
- `../references/tdd-mocking.md`

Keep: `meta-pattern.md`, `deep-modules.md`, `test-loop.md`

**Planning** steps 3–6 rewrites:
- Step 3 (Observability): add "include runtime checkpoints — what internal state, logs, or intermediate data to observe mid-execution, not just final output."
- Step 4 (Test-loop design): add "For each scenario, classify the observation method: binary pass/fail | numeric metric range (with expected range) | qualitative rubric (with explicit criteria). Reference directing's Goal and Failure Criteria for each scenario's expected outcome."
- Step 5 (Test plan): remove "Apply TDD" language. Keep "UT and IT only (E2E is covered by the test-loop). For each module: what behavior needs a unit test, what integration scenario needs an IT?"
- Step 6 (Evaluation criteria): add "Map each criterion to directing's Good / Ambiguous / Bad definitions."

**Evaluate** step after step 4:
- Step 4.5 (Pattern analysis): "Group all unexpected results — what pattern do they share? Name the pattern (e.g. 'all failures on empty input', 'fails only on large payloads'). Identify the likely single root cause of the pattern."

**Evaluate** output format — add:
```
## Patterns
{Named patterns across unexpected results, each with root cause}
```
Placed between `Unexpected / Ambiguous` and `Next steps`.

**Action / Auto-Action**: add at the top (after ADR read):
```
Read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`.
```

## Action Sequence

1. Edit `directing/skill.md`: insert Failure modes as grill question 2; renumber old questions 2→3, 3→4, 4→5.
2. Edit `directing/skill.md`: add `## Failure Criteria` and `## Ambiguous Zone` sections to the output template.
3. Edit `planning/skill.md`: remove `tdd.md`, `tdd-tests.md`, `tdd-mocking.md` from the Read line.
4. Edit `planning/skill.md`: rewrite step 3 (Observability) to include runtime checkpoints.
5. Edit `planning/skill.md`: rewrite step 4 (Test-loop design) to include per-scenario observation method classification and reference to directing's Failure Criteria.
6. Edit `planning/skill.md`: rewrite step 5 (Test plan) to remove TDD language; keep UT/IT only framing.
7. Edit `planning/skill.md`: rewrite step 6 (Evaluation criteria) to reference directing's Good/Ambiguous/Bad definitions.
8. Edit `evaluate/skill.md`: add step 4.5 (pattern analysis — group unexpected results, name pattern, identify root cause).
9. Edit `evaluate/skill.md`: add `## Patterns` section to the output format.
10. Edit `action/skill.md`: add TDD reference reads after the ADR read line.
11. Edit `auto-action/skill.md`: add TDD reference reads after the ADR read line.

## Test-Loop Design

No automated test-loop — skills invoke AI models and are nondeterministic. Evaluation is human review only.

## Test Plan

No UT/IT — the artifacts being modified are markdown prompt files, not code.

## Evaluation Criteria

Human review after invoking each upgraded skill on a sample problem:

**Directing**: Run `/directing` on any sample goal → output file must contain `## Failure Criteria` with at least one named failure condition and `## Ambiguous Zone` with at least one named partial-success case. Neither may be empty placeholders.

**Planning**: Run `/planning` on a direction file → (1) test-loop design step must classify each scenario as binary/metric/qualitative; (2) evaluation criteria must reference "Good / Ambiguous / Bad" from directing; (3) no mention of "Apply TDD" or TDD test-writing instructions in the output.

**Evaluate**: Run `/evaluate` on a sample result set → output must contain a `## Patterns` section that groups at least one unexpected result into a named pattern with a stated root cause. Not just a list of individual failures.

**Action / Auto-Action**: After TDD ref reads are added, confirm the skill reads those files when invoked — verify they appear in the read list at skill startup.
