---
name: review-loop
description: Orchestrate focused outcome, risk, test, and clean review cycles with one targeted fix at a time. Use when a change should pass gated review stages while allowing the human to select or reorder them.
disable-model-invocation: true
license: MIT
---

# Review Loop

Run the selected review skills in parallel against the current state. Show each selected stage's highest-impact finding in the same review cycle, then handle fixes as a gated loop: fix one accepted target, verify the change, and rerun the parallel review batch before moving on.

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

If the human gives no selection, show the recommended order and use it. Do not force unselected stages. The selected order controls finding resolution and stage verdicts; it does not serialize reviewer dispatch.

## Parallel gated workflow

### 1. Establish the selection

Show:

- the selected stages and order;
- the recommended stages that were skipped;
- the available evidence;
- any important missing input.

Do not begin a stage outside the selection.

### 2. Dispatch the selected reviews in parallel

Dispatch one read-only `reviewer` sub-agent for every selected stage before waiting for any result. Use the explicit `subagent()` mechanism and invoke all calls in the same turn:

```typescript
selectedStages.forEach((stage) => {
  subagent({
    name: `Reviewer-${stage}`,
    agent: "reviewer",
    task: "Review the selected stage: [stage]. Apply the criteria in [linked review-skill path]. Review this context, changed code/diff, and result evidence: [supplied inputs]. Return the required one-finding review output, including the exact violated checklist item or criterion (or Violation: None when clean). Do not make edits or delegate.",
  });
});
```

Do not await or serialize one stage before dispatching the next. Collect all results from the batch before deciding actions. Every reviewer must receive the same current-state snapshot and evidence. The linked review skill owns each review's criteria; provide its path without directly invoking the skill. Do not merge criteria from other stages into it. Reviewers are read-only (`tools: read, bash`, `spawning: false`) and must remain so.

Each reviewer must identify and show only its highest-impact or highest-risk primary target first, and label the exact violated checklist item or criterion from its linked skill (for example, `review-risk — Concurrency`). If no in-scope finding remains, report `Violation: None`. Show every selected stage's result together in the same review cycle; process only one accepted finding at a time in the selected order. The Risk stage may inspect failure, boundary, and concurrency risks, but it must still report only one primary risk target at a time.

For each selected stage's primary target/result, show the child review's human-readable fields in the same cycle:

- location;
- violation — the exact checklist item or criterion that is violated, or `None`;
- problem;
- reason;
- separate `Example` section with a fenced code block, real code, data, logs, or an ASCII diagram;
- recommended handling strategy.

### 3. Fix one target at a time

For one accepted finding from the parallel batch:

1. Confirm the exact target and intended behavior.
2. Make the smallest safe fix that addresses that target.
3. Do not bundle unrelated cleanup or speculative improvements.
4. Run the smallest relevant check available.
5. Invalidate all results from the pre-fix snapshot and dispatch every selected reviewer in parallel against the updated state.

If the fix creates a new issue in the same review target, address only that new primary target before proceeding. Never fix multiple parallel findings in one pass.

### 4. Accept or repeat

A stage with no remaining in-scope review point/finding in the latest parallel batch is automatically accepted and advances once the required relevant check supports the result. Do not ask the human to confirm a clean stage.

When any current reviewer reports a review point/finding, show all selected stages' current findings together in the same cycle and pause for the human's decisions or handling. Do not hide a stage's finding, auto-fix, auto-accept, or advance. Fix accepted findings one at a time. If a finding is not accepted or resolved, stay on that stage; results for other stages remain provisional until the current state is cleanly reviewed.

### 5. Advance

After the latest parallel batch is clean and required verification passes, automatically show each stage verdict in the selected order and move to the next selected stage. Every stage verdict must use a result from the latest current-state batch, including all fixes from earlier stages.

If a later fix changes behavior that an earlier stage accepted, return to the earliest affected stage and repeat from there.

## Review control

- **One target per reviewer per cycle:** show one prioritized finding from every selected reviewer in the same cycle; never fix a list of findings in one pass.
- **One scope per stage:** do not use a stage to report another stage's concerns.
- **Current state wins:** every rerun uses the latest code and result evidence.
- **No false acceptance:** a passing command does not prove an outcome unless it observes that outcome.
- **No speculative work:** defer low-confidence or unrelated improvements.
- **Human control:** the human controls every finding and may accept, reject, reorder, skip, or stop at any stage; clean stages advance automatically after required verification.

## Session output

Use this structure:

```markdown
# Review Loop

## Selection
- Order: [stages]
- Skipped: [stages]
- Evidence: [context, changed code, result evidence]

## Review cycle [number]

Show one result block for every selected stage in this same cycle:

### [stage] — [Open | Clean]
- **Target:** [one location or behavior, or `None`]
- **Violation:** [exact checklist item or criterion, or `None`]
- **Problem:** [short statement, or `None`]
- **Reason:** [why it matters, or `None`]

### Example

```text
[real code, data, logs, or ASCII diagram]
```

- **Recommended handling:** [strategy, or `None`]
- **Action:** [fix made, check run, decision pending, or none]
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
