---
name: review-loop
description: Orchestrate focused outcome, risk, test, and clean review cycles with one targeted fix at a time. Use when a change should pass gated review stages while allowing the human to select or reorder them.
disable-model-invocation: true
license: MIT
---

# Review Loop

Run focused review skills as a gated loop. Review one target, fix one accepted target, verify the change, and rerun that review before moving on.

Return all progress and results directly in the current session. Do not create or modify a review report file unless explicitly asked.

## Inputs

Accept any combination of:

- **Context:** a directory, file, repository snapshot, issue, request, or current behavior.
- **Changed code:** a diff, branch, commit, pull request, or current `HEAD`.
- **Result evidence:** logs, command output, API responses, screenshots, stored data, or other observed results.
- **Review selection:** the stages to run, their order, and any stages to skip.

Missing evidence is an uncertainty to report, not a reason to invent facts.

## Recommended order

Unless the human chooses another selection or order, recommend and run:

1. **Outcome** → [review-outcome](../review-outcome/SKILL.md)
   - [ ] Intent — identify the actor, trigger, and observable result.
   - [ ] Acceptance — check the request's conditions and user flow.
   - [ ] Evidence — compare the actual result with the intended outcome.
2. **Risk** → [review-risk](../review-risk/SKILL.md)
   - [ ] Failure — check invalid input, dependency failure, and recovery.
   - [ ] Boundary — check external contracts and trust boundaries.
   - [ ] Concurrency — check shared state, retries, ordering, and atomicity.
3. **Test** → [review-test](../review-test/SKILL.md)
   - [ ] Behavior — identify the important behavior or contract to protect.
   - [ ] Test level — choose the smallest level that reliably observes it.
   - [ ] Test quality — check deterministic, independent, outcome-focused evidence.
4. **Clean** → [review-clean](../review-clean/SKILL.md)
   - [ ] Complexity — look for behavior-preserving deletion and simplification.
   - [ ] Cohesion — keep each responsibility focused and well-bounded.
   - [ ] Intent — make names, interfaces, and structure easy to understand.

Each stage shows no more than three review points; the linked skill owns the full criteria.

## Flexible selection

The human may choose any subset or order. Accept plain instructions such as:

```text
recommended
only outcome
outcome then risk
outcome, risk, test
risk then clean
skip risk
run test only
```

Available stages:

- `outcome`
- `risk`
- `test`
- `clean`

If the human gives no selection, show the recommended order and use it. Do not force unselected stages.

## Gated workflow

### 1. Establish the selection

Show:

- the selected stages and order;
- the recommended stages that were skipped;
- the available evidence;
- any important missing input.

Do not begin a stage outside the selection.

### 2. Review one stage

Dispatch the read-only `reviewer` sub-agent for the current stage using the explicit `subagent()` mechanism:

```typescript
subagent({
  name: "Reviewer",
  agent: "reviewer",
  task: "Review the selected stage: [stage]. Apply the criteria in [linked review-skill path]. Review this context, changed code/diff, and result evidence: [supplied inputs]. Return the required one-finding review output. Do not make edits or delegate.",
});
```

The linked review skill owns the review criteria; provide its path and relevant context to the reviewer without directly invoking the skill. Do not merge criteria from other stages into it. The reviewer is read-only (`tools: read, bash`, `spawning: false`) and must remain so.

The review must identify at most one primary target at a time. If several findings exist, prioritize the highest-impact finding and defer the rest until the current target is resolved. The Risk stage may inspect failure, boundary, and concurrency risks, but it must still report only one primary risk target at a time.

For the primary target, show the child review's human-readable:

- location;
- problem;
- reason;
- separate `Example` section with a fenced code block, real code, data, logs, or an ASCII diagram;
- recommended handling strategy.

### 3. Fix one target

For an accepted finding:

1. Confirm the exact target and intended behavior.
2. Make the smallest safe fix that addresses that target.
3. Do not bundle unrelated cleanup or speculative improvements.
4. Run the smallest relevant check available.
5. Re-run the same review stage against the updated state.

If the fix creates a new issue in the same review target, address only that new primary target before proceeding.

### 4. Accept or repeat

A stage is accepted only when:

- the current review has no remaining in-scope blocking finding;
- the relevant check supports the result, or the missing evidence is explicitly accepted as a risk; and
- the human accepts the stage, unless the human explicitly delegated acceptance to the review result.

If the stage is not accepted, stay on that stage. Do not advance to the next stage.

### 5. Advance

After acceptance, show the stage verdict and move to the next selected stage. The next stage reviews the current state, including all fixes from earlier stages.

If a later fix changes behavior that an earlier stage accepted, return to the earliest affected stage and repeat from there.

## Review control

- **One target per cycle:** never fix a list of findings in one pass.
- **One scope per stage:** do not use a stage to report another stage's concerns.
- **Current state wins:** every rerun uses the latest code and result evidence.
- **No false acceptance:** a passing command does not prove an outcome unless it observes that outcome.
- **No speculative work:** defer low-confidence or unrelated improvements.
- **Human control:** the human may accept, reject, reorder, skip, or stop at any stage.

## Session output

Use this structure:

```markdown
# Review Loop

## Selection
- Order: [stages]
- Skipped: [stages]
- Evidence: [context, changed code, result evidence]

## Current stage: [stage]

### Cycle [number] — [Open | Fixed | Accepted]
- **Target:** [one location or behavior]
- **Problem:** [short statement]
- **Reason:** [why it matters]

### Example

```text
[real code, data, logs, or ASCII diagram]
```

- **Recommended handling:** [strategy]
- **Action:** [fix made, check run, or decision pending]
- **Result:** [review/check result]

## Stage verdicts
| Stage | Verdict | Fixes | Evidence |
|---|---|---:|---|
| [stage] | [accepted/skipped/stopped] | [count] | [short evidence] |

## Final status
[Accepted pipeline | Accepted selected stages | Stopped at stage | Cannot determine]

## Deferred
- [out-of-scope or intentionally skipped concern]
```

Keep the response human-readable. Use fenced examples rather than prose-only placeholders. Do not write a persistent report unless explicitly requested.

## Completion criterion

The loop is complete only when every selected stage is accepted, skipped by explicit human choice, or stopped by the human. Every accepted finding has one targeted fix, a relevant check, and a re-review result recorded in the current session.
