---
name: verify-and-ship
description: Independently verify a completed loop result in its target repository, add only missing useful tests, then merge and ship through the repository's established release path. Use after loop-run has produced an accepted, committed candidate.
---

# Verify and Ship

Independently validate a committed `loop-run` result in the target repository before it is merged and shipped. Verification evidence—not the prior loop's conclusion—controls acceptance.

## Preconditions

Resolve and inspect:

- the completed loop's goal, commit, verification evidence, and changed paths;
- the absolute target repository, candidate branch/commit, integration branch, and clean Git state;
- existing target-repository build, test, CI, merge, release, deployment, smoke-check, monitoring, and rollback mechanisms.

The candidate-to-target mapping and shipping path must be explicit. If either is unknown, the working tree contains unrelated changes, or a release command/rollback path cannot be established, stop and alert the human. Do not guess a branch, deployment target, credential, or release command.

## Verify in the target repository

1. Inspect the candidate diff and its behavior in the target repository. Reuse the target's existing checks and CI configuration.
2. Select the smallest sufficient independent evidence for the changed risk: build/type/lint checks, focused behavior or contract tests, integration checks, and E2E or smoke checks only when the change warrants them.
3. If an important changed behavior or enforceable constraint lacks coverage, add the smallest stable test or verification in the target repository. Do not create a test framework, duplicate a sufficient loop check, or add speculative coverage.
4. Run the selected checks and the target's required full suite. Capture commands, exit statuses, and failure evidence.
5. If verification changes were needed, inspect their diff, commit only the scoped candidate and verification changes, then rerun every affected check. Never absorb unrelated target-repository changes.

## Accept, merge, and ship

The orchestrator accepts the candidate only when all required target-repository verification passes, the diff remains in scope, the result matches the loop goal, and no contradictory evidence remains.

Before merging or shipping, **MUST obtain explicit human confirmation** with the candidate commit, target branch, selected evidence, release/deployment target, rollback path, and expected shipped outcome. A passing test suite does not replace this release gate.

After confirmation:

1. Merge the accepted candidate using the repository's established mechanism (for example, its required pull-request or merge command).
2. Verify the merged target branch with the repository's required post-merge checks.
3. Run the established release/deployment command; do not invent a release process.
4. Run the defined post-ship smoke check and inspect the specified monitoring signal.
5. If any merge, release, deployment, smoke, or monitoring check fails, stop and alert the human. Use rollback only through the established rollback procedure; otherwise leave the state unchanged and report the evidence.

## Verdicts

- **ready for approval:** target verification passes; awaiting the human merge/release gate.
- **shipped:** merge, ship, and post-ship evidence all pass.
- **verification failed:** target evidence rejects the candidate; do not merge.
- **blocked:** target/release facts, clean scope, or the approval gate is missing.
- **ship failed:** merging or shipping began but the required follow-up evidence failed; alert the human with rollback status.

## Report

```text
Candidate: commit and goal
Target: repository, candidate branch, integration branch
Verification: added checks and command results
Acceptance: accepted | rejected | blocked
Approval: pending | confirmed
Merge: commit/PR/result
Ship: target, release/deployment result, smoke and monitoring evidence
Verdict: ready for approval | shipped | verification failed | blocked | ship failed
```

Completion requires the **shipped** verdict, backed by target-repository and post-ship evidence.
