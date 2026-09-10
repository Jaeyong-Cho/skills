---
name: highway
description: Automatically dispatch ready, independent Wayfinder tasks to subagents in parallel, continuing batch by batch until no safe work can proceed. Invoke as /highway.
disable-model-invocation: true
license: MIT
---

# Highway

Run the executable frontier of a recorded `ways/` plan concurrently and keep advancing it automatically. Unlike [next-way](../next-way/SKILL.md), do not recommend one task or wait for user confirmation: reserve every safe, non-blocked task, dispatch its subagent immediately, and continue with the next frontier until work is blocked.

Do not implement product work in the orchestrator. Do not claim a task is done from dispatch or child exit alone; require the task's recorded completion signal and evidence.

## Select the frontier

1. Inspect `./ways/`, or a user-supplied ways directory. Resolve the directory and all recorded paths. Read every way's purpose, expected result, assumptions, scope, and success signal; every executable task's kind, status, absolute `Workdir`, `Needs`, `How`, conditions/conflicts, and `Done when`; every `IMPL` task's absolute `Target repo`; and the root `Execution` section.
2. Follow recorded links and dependencies. Do not infer readiness or parallel safety from filenames, presentation order, or separate branches.
3. Exclude tasks that are `done`, `in-progress`, `waiting`, or `blocked`. An executable task is dispatchable only when:
   - its status is `ready`;
   - every `Needs` prerequisite is satisfied by recorded evidence and `done` status;
   - its conditions hold; and
   - the plan's execution guidance, task boundaries, or inspected write surfaces show that it can run safely beside every other selected task.
4. Exclude `CHECKOUT` tasks from subagent dispatch. They require human judgment, approval, or hands-on verification; report them as human actions instead.
5. If no task is dispatchable, report the first blocker or missing prerequisite and stop. Never invent work or silently run a blocked task. If all tasks are complete, report completion instead of a blocker.

### Parallel safety

Dispatch tasks together only when there is no dependency path between them and no conflict over files, target repositories, mutable resources, contracts, ports, or external state. Require isolation for experiments and separate worktrees or target repositories for parallel `IMPL` tasks; a disjoint write surface is sufficient only when workers do not share a mutable working tree or git index. Read-only `EXPLORE` tasks may run together unless their recorded conditions say otherwise.

If the plan does not establish safe parallelism, leave the task undispatched and name the missing isolation or conflict decision. Ready does not mean safe to parallelize.

## Dispatch

Before dispatching, mark each selected task `Status: in-progress` when practical, preserving its recorded content. Then dispatch every selected task in the same turn without waiting for another child:

```typescript
selectedTasks.forEach((task) => {
  subagent({
    name: `Highway-${task.id}`,
    agent: task.kind === "EXPLORE" ? "scout" : "worker",
    task: `Execute exactly task ${task.id} from [plan path]. Kind: [kind]. Workdir: [absolute Workdir]. Target repo: [absolute Target repo, IMPL only]. Follow its recorded Why, What, How, Needs, conditions, and Done when. For EXPLORE, remain read-only. For EXPERIMENT, keep all trial changes and evidence inside the Workdir. For IMPL, change only the Target repo within the recorded scope. Do not wait for sibling tasks, delegate, or expand scope. Return the observable result, commands/checks, failures, and evidence path; do not claim done without the recorded completion signal.`,
  });
});
```

Use `scout` only for read-only `EXPLORE`. Use `worker` for executable `EXPERIMENT` and `IMPL` tasks, passing the exact recorded paths and constraints. Do not dispatch a child for a `CHECKOUT`. Every child is independent and must not wait for another highway child.

Dispatch is non-blocking: send all calls before collecting any result. Report the batch immediately with task IDs, child names, kinds, workspaces, target repositories, and the safety reason for parallel execution. Running is not completed.

## Automatic run loop

Do not stop after the first batch or ask for confirmation between batches:

1. Dispatch every currently eligible task in one parallel batch.
2. Collect and reconcile the returned results as they arrive; independent children do not wait for one another to start.
3. Recompute the dependency frontier after the batch's results are available.
4. If any safe, non-blocked task is newly ready, reserve it and dispatch the next batch immediately.
5. Continue until no safe task can proceed. A failed or blocked task pauses its dependent lane, but independent safe lanes may continue. Stop the whole run for a shared-state conflict, missing plan decision, or other blocker that makes further dispatch unsafe.

When the run stops, distinguish `blocked` (the plan or dependency prevents progress) from `complete` (all executable work is done) and `waiting` (a human `CHECKOUT` remains).

## Reconcile results

When child results arrive:

1. Match each result to its task ID. Treat missing, failed, cancelled, or ambiguous results as unresolved; never convert them to `done`.
2. Check the result against the task's `What`, `Done when`, expected result state, parent way purpose, and root goal. A green command or child exit is evidence only when it observes the recorded completion signal.
3. Record accepted evidence and `Status: done` in the plan only when the task's observable completion signal is met. Preserve failures and missing evidence as `blocked` or unresolved, with the reason.
4. Recompute the frontier after each completion and automatically dispatch a newly unblocked task in the next parallel batch, without user confirmation, after parallel safety is checked.
5. If a completed task changes a shared contract, write surface, or dependency assumption, stop dispatching affected tasks and report the conflict for plan revision.

Do not merge branches, release, or override a `CHECKOUT` decision. Leave those actions for the human.

## Session output

Use this structure:

```markdown
# Highway

## Plan
- **Ways:** [resolved path]
- **Goal:** [root goal]
- **Batch:** [number]

## Dispatched in parallel
| Task | Kind | Agent | Workdir | Target repo | Safety basis |
|---|---|---|---|---|---|
| [ID] | [kind] | [name] | [absolute path] | [absolute path or —] | [reason] |

## Not dispatched
- **[ID]** — [blocked, waiting, in-progress, CHECKOUT, or unsafe conflict and the exact prerequisite/decision]

## Running
- **[ID]** — [child name; completion not yet evidenced]

## Results
- **[ID]** — [verified completion evidence, failure, cancellation, or unresolved result]

## Next frontier
- [newly ready tasks dispatched automatically, or the first blocker]

## Run status
- [running | advancing automatically | blocked | waiting for human checkout | complete]
```

Show all selected dispatches together in one batch. Do not serialize the report by waiting for the first task, and do not report a task as complete merely because its subagent was launched.

## Completion criterion

Every task considered for dispatch was inspected with its dependencies, status, absolute paths, completion signal, and parallel-safety basis. Every selected ready task was reserved and dispatched without waiting for sibling tasks; newly unblocked tasks were dispatched automatically in subsequent parallel batches until progress stopped. Every excluded task has a recorded reason. Returned results are matched to task IDs and either verified against the recorded completion signal and evidence or explicitly left unresolved. No blocked task, human-owned `CHECKOUT`, unsafe parallel work, invented prerequisite, or unverified `done` status is hidden.
