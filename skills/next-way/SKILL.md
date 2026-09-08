---
name: next-way
description: Find the next actionable Wayfinder node by checking recorded in-progress markers and dependencies, then explain its purpose, context, and next steps. Invoke as /next-way.
disable-model-invocation: true
---

# Next Way

Find one useful next work package from the recorded `ways/` plan. Navigation only: do not implement, redesign, change statuses, or write files.

## Selection

1. Inspect `./ways/`, or a user-supplied ways directory. Read each `0-goal.md`, linked way file, task status, `Needs`, `How`, root `Execution` section, and any existing task workspaces. Follow the recorded tree and links; do not infer order from filenames alone.
2. Check for an in-progress marker before looking for new work. Recognize these fields only:
   - `- Status: in-progress` on an inline task, uncertainty, or checkpoint;
   - `- Scope/status: in-progress` on a way group, with optional detail after the value.
3. If one in-progress node exists, recommend resuming it. If several exist, choose the earliest one in the recorded way-tree order, list the others as concurrent in-progress work, and explain why switching is not preferred.
4. If none is in progress, choose the earliest ready node in the root's `start now` guidance and recorded tree order whose `Needs` are empty or satisfied by `done` prerequisites. Do not choose `waiting`, `blocked`, or `done` work.
5. If no node is ready, report the first unresolved blocker or prerequisite that must change. If every node is done, report that the goal has no next way and recommend a new Wayfinder goal rather than inventing work.
6. If the selected node has `Kind: IMPL`, recommend it in the same `Next` position as any other task, preserving its recorded status, but add this alert:

   > ⚠️ **IMPL handoff:** `/next-way` only recommends this task. Do not implement it directly. Run `/req` → `/ood` → `/to-plan` → `/do-plan` in order, starting at the first missing approved artifact. `/next-way` must not invoke those skills, change status, or write files.

Do not set `in-progress` yourself. Report the marker exactly as recorded so `/to-way` or the user can update it when work actually starts. When work starts, create the task workspace beside its owning group file using the exact task ID (`A1/`, `A2/`, `B2/`) and place task-specific `experiment/`, `req/`, or `design/` artifacts there. Do not create it merely by selecting the next task.

## Explain the recommendation

Return one compact recommendation containing:

- **Next:** source ID, title, kind, status, exact file/anchor, and expected task workspace path (`<ID>/`).
- **Purpose:** the node's recorded `Why` and the parent outcome it enables.
- **Context:** the current parent goal/way, relevant completed evidence, prerequisites, blockers, and why this node is next.
- **How:** the node's recorded `How`, preserving its order. Do not invent implementation steps; if `How` is missing, report the invalid plan and ask for `/wayfinder` or `/to-way` correction.
- **IMPL alert:** if the node has `Kind: IMPL`, repeat the handoff warning and skill order above; recommend the task, but do not invoke the skills or implement it.
- **Done when:** the recorded completion signal.
- **After it:** the nodes or way it unlocks, if the plan states them.

For an in-progress node, lead with the existing progress marker and explain how to resume from its recorded `How`; do not restart completed steps. For a ready node, explain which prerequisite evidence makes it ready. Apply the IMPL alert to either status.

## Completion criterion

Every recorded way and inline executable node relevant to selection was inspected; existing task workspaces and artifacts were considered; the recommendation follows an existing in-progress marker before readiness and recorded tree order before filename order; the response names purpose, context, How, completion signal, and workspace path; an `IMPL` recommendation includes the handoff alert without invoking implementation skills; and no status, file, or plan content was changed.
