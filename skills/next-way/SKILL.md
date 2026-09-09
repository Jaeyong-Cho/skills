---
name: next-way
description: Find the next actionable Wayfinder node; advance implementation according to its recorded approach, or review its implementation evidence against the recorded outcome and purpose. Invoke as /next-way.
disable-model-invocation: true
---

# Next Way

Find one useful next work package from the recorded `ways/` plan. Do not implement product code. Recommend the next node and let the user decide whether to start it; when work begins, record that selected node as `in-progress` when practical. For an `IMPL` task, follow its recorded approach. Return the selected task with its recorded working directory.

## Selection

1. Inspect `./ways/`, or a user-supplied ways directory. Resolve that directory and all recorded paths. Read each way's purpose, expected result, hypothesis, assumptions, scope, and success signal; each task's status, absolute `Workdir`, `Needs`, and `How`; every `IMPL` task's absolute `Target repo`; the root `Execution` section; and any existing task workspaces. Follow the recorded tree and links; do not infer order from filenames alone. If required planning fields are missing, flag the gaps and recommend revising the plan; continue with a clearly stated limitation when a useful recommendation is still possible.
2. Before choosing new work, find any `IMPL` task whose implementation evidence is not yet reviewed. Review the earliest one in way-tree order using the post-implementation review below. If that review finds an issue, report it before recommending additional work.
3. Check for an in-progress marker before looking for new work. Recognize these fields only:
   - `- Status: in-progress` on an inline `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT` task;
   - `- Scope/status: in-progress` on a way group, with optional detail after the value.
4. If one in-progress node exists, recommend resuming it. If several exist, choose the earliest one in the recorded way-tree order, list the others as concurrent in-progress work, and explain why switching is not preferred.
5. If none is in progress, recommend the earliest ready node in the root's `start now` guidance and recorded tree order whose `Needs` are empty or satisfied by `done` prerequisites. If useful, a `waiting` or `blocked` node may also be selected when its missing prerequisite is explicitly reported and the user chooses to proceed; never select `done` work as new work.
6. If no node is ready, report the first unresolved blocker or prerequisite and offer the user the choice to resolve it or proceed with a documented risk. If every node is done, report that the goal has no obvious next way and recommend a new Wayfinder goal rather than inventing work.
7. Present the selected node and ask whether the user wants to start it. Selection alone need not edit the way or create the task workspace.
8. When the user accepts or explicitly asks to proceed, record the selected task's `Status` (or selected way's `Scope/status`) as `in-progress` when practical, preserving all other content. If the update is skipped or fails, report that state instead of treating it as a hard stop.
9. After the marker exists, use the task's absolute Workdir as the base for all task output. For `EXPERIMENT`, keep trial artifacts isolated beneath the Workdir. For `IMPL`, follow its recorded How and create only the artifact directories required by that approach. Direct implementation to the recorded Target repo when the task is ready for it.

Report pre-existing `in-progress` markers exactly as recorded. A resumed node needs no second acceptance or status update, and starts from its next incomplete action. Supporting work may write artifacts only after the marker exists.

## Post-implementation result review

When an `IMPL` task has implementation evidence:

1. Read the available implementation evidence and the task's `Why`, `What`, and `Done when`, the parent way's purpose/expected result/success signal/hypothesis/assumptions, and the root goal's same fields.
2. Check the actual changed behavior, acceptance results, test/check evidence, review findings, residual risks, and commit state. Do not treat a file path, green build, or commit alone as proof of the task outcome.
3. Compare the actual observable result with the task's expected `What` and `Done when`, then decide whether it advances the parent way's purpose and expected outcome without refuting its hypothesis or required assumptions.
4. Return one verdict:
   - `MATCH` — the expected result is evidenced and still serves the recorded purpose;
   - `PARTIAL` — some expected result or evidence is missing/blocked, but the way's purpose remains valid;
   - `CONTRADICTION` — the result conflicts with the expected outcome, defeats the purpose, refutes a relied-on hypothesis, or invalidates a required assumption.
5. On `MATCH`, cite the evidence, recommend recording the evidence and status, and continue normal selection when useful.
6. On `PARTIAL`, name the unmet `Done when` condition or missing evidence. Recommend continuing the same work, but allow unrelated or explicitly accepted follow-up work to continue; do not present the task as fully verified.
7. On `CONTRADICTION`, show both conflicting statements with paths and recommend revising the existing way. Preserve stable IDs and completed evidence; if the user continues, clearly label the work as proceeding against a conflicting plan.

Review implementation output only on a later invocation; this selection step must not implement product code itself.

## IMPL execution guidance

For an accepted or already in-progress selected `Kind: IMPL` node:

1. Read the selected task's absolute `Target repo` and `Workdir`, `Why`, `What`, `How`, and `Done when`; its parent way's purpose, expected result, success signal, hypothesis, and assumptions; and the root goal's same fields, scope, and grounding. Inspect product code only in Target repo.
2. Inspect any existing context or implementation evidence, but do not require artifacts that the recorded How does not use.
3. Follow the task's recorded How and return the selected task's next action. Do not impose a process sequence or implement product code during selection.
4. A contradiction is critical only when it changes or negates the recorded purpose/outcome, refutes a hypothesis the way depends on, invalidates an assumption required for scope, safety, or prerequisites, or makes the selected task no longer the right work package. Missing wording or compatible added detail is not critical.
5. On a critical contradiction, show the conflicting statements and artifact paths, and recommend revising the existing way. Preserve stable IDs and completed evidence through the recording step. If the user elects to continue, make the contradiction explicit.
6. If no critical contradiction exists, return the selected task and its next action.

## Explain the recommendation

Return one compact recommendation containing:

- **Next:** source ID, title, kind, status, exact file/anchor, and recorded absolute Workdir; include the absolute Target repo for `IMPL`.
- **Purpose:** the node's recorded `Why`, the parent purpose it serves, and the expected result it enables.
- **Context:** the current parent goal/way, relevant completed evidence, prerequisites, blockers, and why this node is next.
- **How:** the node's recorded `How`, preserving its order. Do not invent implementation steps; if `How` is missing, report the invalid plan and request a plan revision.
- **IMPL review:** for an `IMPL` result, report `MATCH`, `PARTIAL`, or `CONTRADICTION` with evidence; for an `IMPL` not yet executed, report its readiness, relevant context, and next action.
- **Done when:** the recorded completion signal.
- **After it:** the nodes or way it unlocks, if the plan states them.

For an in-progress node, lead with the existing progress marker and resume from its next incomplete action or recorded `How`; do not restart completed steps. For a ready node, explain which prerequisite evidence makes it ready and ask whether to start it. For a waiting or blocked node selected by the user, state the missing prerequisite and risk before proceeding. If work begins without a marker, state that clearly.

## Completion criterion

Every recorded way and inline executable node relevant to selection was inspected; every task's absolute Workdir and every `IMPL` task's absolute Target repo were checked; existing task workspaces and any linked implementation evidence were considered before new readiness. A pending result received a `MATCH`, `PARTIAL`, or `CONTRADICTION` verdict against the task's expected result and parent way's purpose, with exact evidence and any risks clearly stated. The recommendation follows an existing in-progress marker before readiness when one exists, and recorded tree order before filename order. For an `IMPL`, the recorded How determines the next action; no process sequence is imposed.
