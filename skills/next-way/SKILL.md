---
name: next-way
description: Find the next actionable Wayfinder node; prepare an implementation task through planning, or review its do-plan result against the recorded outcome and purpose. Invoke as /next-way.
disable-model-invocation: true
---

# Next Way

Find one useful next work package from the recorded `ways/` plan. Do not implement product code. Recommend the next node and wait for the user to accept starting it; after acceptance, record that selected node as `in-progress` before any handoff or work begins. For an `IMPL` task, either run its requirements, design, and planning handoff or review a later `/do-plan` result as described below; otherwise, return the accepted task with its recorded working directory.

## Selection

1. Inspect `./ways/`, or a user-supplied ways directory. Resolve that directory and all recorded paths. Read each way's purpose, expected result, hypothesis, assumptions, scope, and success signal; each task's status, absolute `Workdir`, `Needs`, and `How`; every `IMPL` task's absolute `Target repo`; the root `Execution` section; and any existing task workspaces. Follow the recorded tree and links; do not infer order from filenames alone. If a way omits purpose, expected result, hypothesis, or assumptions, any task omits an absolute Workdir, or an `IMPL` task omits an absolute Target repo, stop and recommend `/wayfinder` revise the invalid plan before selecting work.
2. Before choosing new work, find any `IMPL` task whose linked plan has a `{plan-file}.report.md` result that its recorded Evidence does not yet review. Review the earliest one in way-tree order using the post-`/do-plan` review below. If that review must stop, do not select another node.
3. Check for an in-progress marker before looking for new work. Recognize these fields only:
   - `- Status: in-progress` on an inline `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT` task;
   - `- Scope/status: in-progress` on a way group, with optional detail after the value.
4. If one in-progress node exists, recommend resuming it. If several exist, choose the earliest one in the recorded way-tree order, list the others as concurrent in-progress work, and explain why switching is not preferred.
5. If none is in progress, choose the earliest ready node in the root's `start now` guidance and recorded tree order whose `Needs` are empty or satisfied by `done` prerequisites. Do not choose `waiting`, `blocked`, or `done` work.
6. If no node is ready, report the first unresolved blocker or prerequisite that must change. If every node is done, report that the goal has no next way and recommend a new Wayfinder goal rather than inventing work.
7. Present the selected node and ask the user to accept or decline starting it. Selection alone must not edit the way or create the task workspace.
8. If accepted, **SHOULD RUN** `/to-way` to change the selected task's `Status` (or selected way's `Scope/status`) to `in-progress`, preserving all other content. Verify the marker was recorded before starting anything. If the update fails or the user declines, stop without invoking work.
9. After the marker exists, use the task's absolute Workdir as the base for all task output. For `EXPERIMENT`, use `<Workdir>/experiments/`. For `IMPL`, use `<Workdir>/req/`, then `<Workdir>/ood/`, then `<Workdir>/plans/`; create each only when that stage starts and run the corresponding skill with that directory as its working directory. If the selected node has `Kind: IMPL`, then run the IMPL handoff below.

Report pre-existing `in-progress` markers exactly as recorded. A resumed node needs no second acceptance or status update, and starts from its first missing artifact. The invoked handoff skills may write approved artifacts only after the marker exists.

## Post-`/do-plan` result review

When an `IMPL` task has a `/do-plan` report:

1. Read the report, its plan, approved requirement/design artifacts, the task's `Why`, `What`, and `Done when`, the parent way's purpose/expected result/success signal/hypothesis/assumptions, and the root goal's same fields.
2. Check the report's actual changed behavior, action-item outcome, acceptance results, test/check evidence, review findings, residual risks, and commit state. Do not treat a report path, green build, or commit alone as proof of the task outcome.
3. Compare the actual observable result with the task's expected `What` and `Done when`, then decide whether it advances the parent way's purpose and expected outcome without refuting its hypothesis or required assumptions.
4. Return one verdict:
   - `MATCH` — the expected result is evidenced and still serves the recorded purpose;
   - `PARTIAL` — some expected result or evidence is missing/blocked, but the way's purpose remains valid;
   - `CONTRADICTION` — the result conflicts with the expected outcome, defeats the purpose, refutes a relied-on hypothesis, or invalidates a required assumption.
5. On `MATCH`, cite the report and evidence, then stop if the way has not recorded this review; recommend `/to-way` record the evidence and status before selecting dependent work. If the matching review is already recorded, continue normal selection.
6. On `PARTIAL`, stop and name the unmet `Done when` condition or missing evidence; recommend resuming the same plan or resolving its blocker. Do not mark the task done or unlock dependents.
7. On `CONTRADICTION`, stop, show both conflicting statements with paths, and **SHOULD RUN** `/wayfinder` to revise the existing way. Preserve stable IDs and completed evidence; do not silently redefine success around what was built.

`/next-way` reviews `/do-plan` output only on a later invocation; it still must not invoke `/do-plan` itself.

## IMPL handoff

For an accepted or already in-progress selected `Kind: IMPL` node:

1. Read the selected task's absolute `Target repo` and `Workdir`, `Why`, `What`, `How`, and `Done when`; its parent way's purpose, expected result, success signal, hypothesis, and assumptions; and the root goal's same fields, scope, and grounding. Inspect product code only in Target repo; keep handoff artifacts under the Workdir stage directories.
2. Reuse approved requirement artifacts when they exist; otherwise **MUST RUN** `/req` in the current conversation with `<Workdir>/req/` as its working directory and wait for its approval gate.
3. Compare the approved requirements' actor, purpose, outcome, scope, acceptance criteria, dependencies, and assumptions with the selected task, parent way, and root goal.
4. A contradiction is critical only when it changes or negates the recorded purpose/outcome, refutes a hypothesis the way depends on, invalidates an assumption required for scope, safety, or prerequisites, or makes the selected task no longer the right work package. Missing wording or compatible added detail is not critical.
5. On a critical contradiction, stop the handoff before `/ood` or `/to-plan`, show the conflicting statements and artifact paths, and **SHOULD RUN** `/wayfinder` to revise the existing way. Preserve stable IDs and completed evidence through Wayfinder's update rules. Do not silently reconcile the conflict or continue from the stale way.
6. If no critical contradiction exists, reuse approved downstream artifacts and **MUST RUN** the remaining `/ood` → `/to-plan` sequence from the first missing artifact, using `<Workdir>/ood/` and `<Workdir>/plans/` respectively while keeping Target repo explicit. Each skill retains its own human approval gate. Return absolute approved artifact paths, then **SHOULD STOP**. It may recommend `/do-plan` as the next user action, but `/next-way` must not invoke `/do-plan` or implement product code.

## Explain the recommendation

Return one compact recommendation containing:

- **Next:** source ID, title, kind, status, exact file/anchor, and recorded absolute Workdir; include the absolute Target repo for `IMPL`.
- **Purpose:** the node's recorded `Why`, the parent purpose it serves, and the expected result it enables.
- **Context:** the current parent goal/way, relevant completed evidence, prerequisites, blockers, and why this node is next.
- **How:** the node's recorded `How`, preserving its order. Do not invent implementation steps; if `How` is missing, report the invalid plan and ask for `/wayfinder` or `/to-way` correction.
- **IMPL review/handoff:** for an `IMPL` result, report `MATCH`, `PARTIAL`, or `CONTRADICTION` with evidence; for an `IMPL` not yet executed, report the requirement-to-way consistency verdict and either the contradiction-driven `/wayfinder` revision or the approved requirement, design, and plan paths.
- **Done when:** the recorded completion signal.
- **After it:** the nodes or way it unlocks, if the plan states them.

For an in-progress node, lead with the existing progress marker and resume from its first missing handoff artifact or recorded `How`; do not restart completed steps. For a ready node, explain which prerequisite evidence makes it ready, ask for start acceptance, and do not begin until its in-progress marker is recorded.

## Completion criterion

Every recorded way and inline executable node relevant to selection was inspected; every task's absolute Workdir and every `IMPL` task's absolute Target repo were validated; existing task workspaces, linked plans, and `/do-plan` reports were considered before new readiness. A pending result received a `MATCH`, `PARTIAL`, or `CONTRADICTION` verdict against the task's expected result and parent way's purpose, with exact evidence; unmatched or unrecorded results stopped before dependent selection. Otherwise, the recommendation follows an existing in-progress marker before readiness and recorded tree order before filename order, and names purpose, context, How, completion signal, and workspace path. For a newly selected node, the user accepted its start and its recorded state changed to `in-progress` before work began. For a not-yet-executed `IMPL`, approved requirements were checked against the way before `/ood` and `/to-plan`, with artifacts written from the recorded `req/`, `ood/`, and `plans/` stage directories. `/next-way` stopped after `/to-plan` and never invoked `/do-plan` or implemented product code.
