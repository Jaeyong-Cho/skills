---
name: review-loop
description: Orchestrate clean and thermo review cycles with reviewed fixes. Use when a change should pass focused quality review while allowing the human to select or reorder the stages and confirm each fix.
disable-model-invocation: true
license: MIT
---

# Review Loop

Run the selected review skills in parallel against the current state. Show up to three findings from each selected stage in the same review cycle, then fix all non-blocking findings one at a time: verify each fix and wait for human confirmation before rerunning reviews or proceeding.

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

1. **Clean** → [review-clean](../review-clean/SKILL.md)
   - [ ] Complexity — look for behavior-preserving deletion and simplification.
   - [ ] Cohesion — keep each responsibility focused and well-bounded.
   - [ ] Intent — make names, interfaces, and structure easy to understand.
2. **Thermo** → [review-thermo](../review-thermo/SKILL.md)
   - [ ] Abstraction — challenge structural complexity and missing simplifications.
   - [ ] Spaghetti — flag ad-hoc branching and misplaced feature logic.
   - [ ] Decomposition — flag unhealthy file growth and weak module boundaries.

Each reviewer reports no more than three review points per cycle, ordered by impact; the linked skill owns the full criteria.

## Flexible selection

The human may choose any subset or order. Accept plain instructions such as:

```text
recommended
only clean
clean then thermo
only thermo
skip thermo
```

Available stages:

- `clean`
- `thermo`

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

Dispatch one read-only `reviewer` sub-agent for every selected stage before waiting for any result. Clean and Thermo must be dispatched in parallel in the same turn when both are selected; neither may wait for the other. `review-thermo` is invoked only through this dispatch path; do not call it directly outside the review loop. Use the explicit `subagent()` mechanism and invoke all calls in the same turn:

```typescript
selectedStages.forEach((stage) => {
  subagent({
    name: `Reviewer-${stage}`,
    agent: "reviewer",
    task: "Review the selected stage: [stage]. Apply the criteria in [linked review-skill path]. Review this context, changed code/diff, and result evidence: [supplied inputs]. Return up to three findings in descending priority, each including the exact violated checklist item or criterion (or Violation: None when clean). Do not make edits or delegate.",
  });
});
```

Do not await or serialize one stage before dispatching the next. Collect all selected results from the batch before deciding actions. Every reviewer must receive the same current-state snapshot and evidence. The linked review skill owns each review's criteria; provide its path without directly invoking the skill. Do not merge criteria from other stages into it. Reviewers are read-only (`tools: read, bash`, `spawning: false`) and must remain so.

Each reviewer may identify up to three in-scope targets, ordered from highest impact to lowest, and label the exact violated checklist item or criterion from its linked skill. If no in-scope finding remains, report `Violation: None`. Show every selected stage's findings together in the same review cycle; process one finding at a time in the selected order.

For each selected stage's reported finding, show the child review's human-readable fields in the same cycle:

- location;
- violation — the exact checklist item or criterion that is violated, or `None`;
- problem;
- reason;
- separate `Example` section with a fenced code block, real code, data, logs, or an ASCII diagram;
- recommended handling strategy.

### 3. Fix one target, then wait for confirmation

Process findings one at a time, in selected stage order and descending priority. Before fixing each finding, stop and request human handling if any of these conditions apply:

- the finding or required behavior is ambiguous, unresolved, or marked `Cannot determine`;
- the finding is explicitly critical or has `Blocker` severity;
- any reviewer says the change does not match the user's intent or acceptance criteria.

Otherwise:

1. make the smallest safe fix for that target only;
2. run the smallest relevant check available;
3. show the fix and check result, then wait for explicit human confirmation;
4. only after confirmation, invalidate all results from the pre-fix snapshot and dispatch every selected reviewer in parallel against the updated state.

Do not bundle unrelated cleanup or speculative improvements. If the check fails, stop and request human handling. If a confirmed fix creates a new issue, handle only that new highest-priority target before proceeding.

### 4. Accept or stop

A stage with no remaining in-scope review point/finding in the latest parallel batch is automatically accepted and advances once the required relevant check supports the result. Do not ask the human to confirm a clean stage.

When a current reviewer reports findings, show all selected stages' findings together in the same cycle and fix the next non-blocking target. After verification, pause for explicit human confirmation before rerunning reviews or advancing; continue this loop until all non-blocking findings are fixed or no longer reported. Do not hide a finding. If a stop condition applies, pause with that finding and keep the pipeline stopped; results for other stages remain provisional until the current state is cleanly reviewed.

### 5. Advance

After the latest parallel batch is clean and required verification passes, automatically show each stage verdict in the selected order and move to the next selected stage. Every stage verdict must use a result from the latest current-state batch, including all fixes from earlier stages.

If a later fix changes behavior that an earlier stage accepted, return to the earliest affected stage and repeat from there.

## Review control

- **Maximum three findings:** each reviewer reports at most three prioritized findings per cycle.
- **One scope per stage:** do not use a stage to report another stage's concerns.
- **Current state wins:** every rerun uses the latest code and result evidence.
- **No false acceptance:** a passing command does not prove an outcome unless it observes that outcome.
- **No speculative work:** defer low-confidence or unrelated improvements.
- **Gated handling:** fix every concrete, non-blocking finding one at a time, verify each fix, then wait for explicit human confirmation before rerunning reviews or proceeding; stop for ambiguity, explicit critical/Blocker severity, or intent mismatch.

## Session output

Use this structure:

```markdown
# Review Loop

## Selection
- Order: [stages]
- Skipped: [stages]
- Evidence: [context, changed code, result evidence]

## Review cycle [number]

Show up to three result blocks for every selected stage in this same cycle, ordered by priority:

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

The loop is complete only when every selected stage is accepted, skipped, or stopped by a defined stop condition or the human. Every fixed finding has one targeted fix, a relevant check, human confirmation, and a re-review result recorded in the current session.
