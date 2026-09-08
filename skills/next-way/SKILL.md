---
name: next-way
description: Find the next actionable Wayfinder node; for an implementation task, run its requirements, design, and planning handoff after checking it still matches the recorded way. Invoke as /next-way.
disable-model-invocation: true
---

# Next Way

Find one useful next work package from the recorded `ways/` plan. Do not implement product code or change statuses. For an `IMPL` task, run its requirements, design, and planning handoff as described below; otherwise, only recommend the selected work.

## Selection

1. Inspect `./ways/`, or a user-supplied ways directory. Read each `0-goal.md`, linked way file, task status, `Needs`, `How`, root `Execution` section, and any existing task workspaces. Follow the recorded tree and links; do not infer order from filenames alone.
2. Check for an in-progress marker before looking for new work. Recognize these fields only:
   - `- Status: in-progress` on an inline `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT` task;
   - `- Scope/status: in-progress` on a way group, with optional detail after the value.
3. If one in-progress node exists, recommend resuming it. If several exist, choose the earliest one in the recorded way-tree order, list the others as concurrent in-progress work, and explain why switching is not preferred.
4. If none is in progress, choose the earliest ready node in the root's `start now` guidance and recorded tree order whose `Needs` are empty or satisfied by `done` prerequisites. Do not choose `waiting`, `blocked`, or `done` work.
5. If no node is ready, report the first unresolved blocker or prerequisite that must change. If every node is done, report that the goal has no next way and recommend a new Wayfinder goal rather than inventing work.
6. If the selected node has `Kind: IMPL`, preserve its recorded status and run the IMPL handoff below.

Do not set `in-progress` yourself. Report the marker exactly as recorded so `/to-way` or the user can update it when work actually starts. The invoked handoff skills may write their approved artifacts, but `/next-way` must not edit the way or create the task workspace merely by selecting it.

## IMPL handoff

For a selected `Kind: IMPL` node:

1. Read the selected task's `Why`, `What`, `How`, and `Done when`; its parent way's purpose, outcome, success signal, hypothesis, and assumptions when recorded; and the root goal's scope and grounding.
2. Reuse approved requirement artifacts when they exist; otherwise **MUST RUN** `/req` in the current conversation and wait for its approval gate.
3. Compare the approved requirements' actor, purpose, outcome, scope, acceptance criteria, dependencies, and assumptions with the selected task, parent way, and root goal.
4. A contradiction is critical only when it changes or negates the recorded purpose/outcome, refutes a hypothesis the way depends on, invalidates an assumption required for scope, safety, or prerequisites, or makes the selected task no longer the right work package. Missing wording or compatible added detail is not critical.
5. On a critical contradiction, stop the handoff before `/ood` or `/to-plan`, show the conflicting statements and artifact paths, and **SHOULD RUN** `/wayfinder` to revise the existing way. Preserve stable IDs and completed evidence through Wayfinder's update rules. Do not silently reconcile the conflict or continue from the stale way.
6. If no critical contradiction exists, reuse approved downstream artifacts and **MUST RUN** the remaining `/ood` → `/to-plan` sequence from the first missing artifact. Each skill retains its own human approval gate. Return the approved plan path, then **SHOULD STOP**. It may recommend `/do-plan` as the next user action, but `/next-way` must not invoke `/do-plan` or implement product code.

## Explain the recommendation

Return one compact recommendation containing:

- **Next:** source ID, title, kind, status, exact file/anchor, and expected task workspace path (`<ID>/`).
- **Purpose:** the node's recorded `Why` and the parent outcome it enables.
- **Context:** the current parent goal/way, relevant completed evidence, prerequisites, blockers, and why this node is next.
- **How:** the node's recorded `How`, preserving its order. Do not invent implementation steps; if `How` is missing, report the invalid plan and ask for `/wayfinder` or `/to-way` correction.
- **IMPL handoff:** if the node has `Kind: IMPL`, report the requirement-to-way consistency verdict and either the contradiction-driven `/wayfinder` revision or the approved requirement, design, and plan paths.
- **Done when:** the recorded completion signal.
- **After it:** the nodes or way it unlocks, if the plan states them.

For an in-progress node, lead with the existing progress marker and resume from its first missing handoff artifact or recorded `How`; do not restart completed steps. For a ready node, explain which prerequisite evidence makes it ready.

## Completion criterion

Every recorded way and inline executable node relevant to selection was inspected; existing task workspaces and artifacts were considered; the recommendation follows an existing in-progress marker before readiness and recorded tree order before filename order; and the response names purpose, context, How, completion signal, and workspace path. For `IMPL`, approved requirements were checked against the way's purpose, hypothesis, and assumptions before design and planning; a critical contradiction stopped the handoff and routed revision through `/wayfinder`, otherwise `/req` → `/ood` → `/to-plan` completed from the first missing artifact. `/next-way` stopped after `/to-plan`; it did not run `/do-plan`, implement product code, or change status.
