---
name: loop-run
description: Execute a prepared loop-design development loop; implement one verified gap at a time with a scoped sub-agent assessment. Use when `loop/verify/run.sh` exists and the user wants bounded RED-to-GREEN implementation; defaults to three change iterations.
---

# Loop Run

Run an existing `loop-design` loop to completion or a defined stop. The default maximum is **3 change iterations**; honor a user-provided positive maximum instead. A baseline verification run does not consume an iteration.

## Loop layout

Read `loop/README.md` first; it names the goal, scope, setup, verifier order, and completion condition. The loop may contain only the directories needed for its goal:

```text
loop/
├── README.md
├── setup/{run.sh,NN-{slug}.sh}
├── verify/{run.sh,NN-{slug}.sh}
├── tools/
├── config/
├── workspace/
└── runs/{timestamp}/
```

`setup/run.sh` and `verify/run.sh` are the entry points. Numbered scripts execute in numeric order; `verify/run.sh` stops at the first failure. `tools/` supplies only required check helpers, and `runs/` holds execution evidence. `loop-design` owns this layout: do not create or restructure it while operating the loop unless a missing verifier makes the loop invalid.

## Preconditions

Before changing code, confirm that `loop-design` has completed for this one goal: the `grill-me` session was confirmed, setup and ordered verification exist, and `loop/verify/run.sh` is runnable. Run `loop/setup/run.sh` if the prepared loop requires it. Build a current verification ledger from immediate command results.

Reuse an immediate passing result directly when its command, environment, and observed inputs are unchanged since it ran; do not rerun it merely to rebuild the ledger. Otherwise rerun that verifier. When no reliable ledger identifies the current first gap, run:

```bash
loop/verify/run.sh
```

- Passing evidence for every verifier means the goal is already complete: report the evidence and stop.
- A failure must identify the first failing verifier and include its expected state, actual state, and evidence.
- Missing, non-runnable, ambiguous, or non-deterministic verification is a setup gap. Stop and return to `loop-design`; do not invent acceptance criteria or implement against a guess.

## Each change iteration

For the current first failure, perform these steps, up to the limit:

1. **Check for contradiction.** Compare the goal, confirmed decisions, green verification prefix, and current failure. A contradiction exists when required invariants cannot all be true under the same conditions, required scripts need incompatible environment states, or a check conflicts with the confirmed goal. If found, make no change and alert the human with the conflicting requirements, verifier paths, and evidence. Do not skip, weaken, or reorder checks to hide it.
2. **Delegate assessment.** SHOULD dispatch one scoped sub-agent for this iteration. Give it the goal, current first failure, relevant source, green prefix, and prior attempts. It investigates read-only and returns: root-cause evidence, the smallest viable change, relevant risks, and any contradiction. It must not edit, broaden scope, or declare success. If delegation is unavailable, record that fact and proceed only when the existing evidence is sufficient.
3. **Orchestrate the change.** Judge the evidence and delegated assessment. If they reveal a contradiction or insufficient evidence, stop as above or improve observability before changing code. Otherwise make one small, cohesive change that closes the current gap; do not perform unrelated cleanup.
4. **Verify.** Rerun the failed script and every earlier check invalidated by the change. Reuse only valid immediate passing evidence for unaffected checks. Then run unverified or invalidated later scripts in order until the next failure. Once no gap remains, MUST run `loop/verify/run.sh` as the final full verification; reused evidence never replaces this final run. Use `loop/verify/run.sh` earlier when no trustworthy ledger exists, the affected scope is unclear, or it is cheaper than selective execution.
5. **Judge, commit, and choose the next behavior.** The orchestrator accepts an iteration only when current execution or valid reused evidence covers its failed check and prerequisites, the change is in scope, and no contradiction remains. It MUST inspect the Git status and diff, then create one focused commit for that accepted small change before taking another iteration. A later verifier may still expose the next gap; that does not invalidate the accepted prefix. If the diff cannot be cleanly scoped, the commit fails, or the change does not produce a clearer or smaller gap, stop and alert the human. Do not carry an accepted change uncommitted.

## Handoff after full completion

When the final `loop/verify/run.sh` exits `0` and every accepted iteration is committed, hand the verified commit series to `@skills/verify-and-ship` for independent target-repository validation, merge, and shipping.

## Stop conditions

Stop and report the current state when any of these occurs:

- The final `loop/verify/run.sh` exits `0` and every accepted iteration is committed: **complete**.
- Verification requirements contradict each other or the confirmed goal: **contradiction — human decision required**.
- Evidence is inadequate: **observability/design gap — return to loop-design**.
- The maximum number of change iterations is reached while verification still fails: **iteration limit reached**; include the first remaining failure and ask whether to extend the limit.
- A change fails to make progress: **blocked — human direction required**.

Never claim completion from implementation reasoning, sub-agent opinion, reused intermediate output, or a partial green prefix. Only the final full `loop/verify/run.sh` can complete the loop.

## Per-iteration report

After each iteration, report concisely:

```text
Iteration: N / maximum
First failure: NN-slug
Sub-agent: assessment summary or unavailable
Change: path(s) and intent
Verification: executed and reused check results, with invalidation basis
Orchestrator judgment: accepted | next gap | contradiction | blocked | complete
Commit: hash | not applicable | blocked
Next behavior: commit accepted change and implement next gap | hand off to verify-and-ship | stop and alert human
```
