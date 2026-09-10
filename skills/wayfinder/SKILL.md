---
name: wayfinder
description: Use grill-me to plan and report one goal as cheapest-first EXPLORE, EXPERIMENT, IMPL, and CHECKOUT tasks with explicit dependencies and safe parallel work; never write way documents. Invoke as /wayfinder.
disable-model-invocation: true
---

# Wayfinder

Produce a task plan, not a lifecycle checklist. Answer:

> What work is actually needed, what do we not know yet, what can start now, and what must wait for what?

Plan first: use grill-me for the user conversation and inspect context, but do not implement, run experiments, or persist the result. Wayfinder may inspect the relevant `contexts/` directory (including one alongside the supplied goal, repository, or way path when present) and read applicable `*-facts-*`, `*-intents-*`, and `*-constraints-*` files as read-only inputs while planning. Keep confirmed facts, user intent, constraints, and unresolved questions explicitly distinct; do not turn inferences or open questions into facts or decisions. After the user confirms the plan, return the plan in the conversation only. Propose evidence-gathering work when needed; never report a proposed check as completed.

**MUST NOT** create, update, or write any way document, even when persistence is requested during the Wayfinder invocation. Separate to-context or other recording operations may persist confirmed context after confirmation; those operations are outside Wayfinder. End with a clear handoff for the separate recording step.

## Recommend the recording operation

- Inspect the supplied way path, or `./ways/`, as read-only context before planning. Do not ask the user to choose create or update at the beginning.
- Decide and recommend the operation at the end, after the plan and target have been inspected: create a new numbered way for a new goal; update the matching goal in place for an existing goal; update the parent goal when adding a child way.
- For a recommended update, identify stable IDs, completed-work evidence, and user annotations that the recording step must preserve; new nodes need globally unique IDs.
- If the proposed update would move or remove files, strand old tasks, or conflict with recorded evidence, report the conflict before recording; do not change anything.
- Always return the confirmed plan and recommended operation without writing files.

## Task types

Every executable leaf has exactly one of these kinds:

- `EXPLORE` — resolve an uncertainty using read-only inspection: search, read files/docs, trace existing code, or inspect already-produced evidence. It must not edit files, run a behavioral trial, or change production state.
- `EXPERIMENT` — resolve an uncertainty that inspection cannot answer by running an isolated experiment. Its How names the question, expected distinguishing result, and isolation boundary.
- `IMPL` — eventually change production code using inspected context and resolved consequential uncertainties. It is an inline task kind, not a separate way or root-level node; an existing leaf ID such as `A4` or `B3` remains stable. Every `IMPL` task should name its target repository as a resolved absolute path.
- `CHECKOUT` — a human checkpoint for a decision, approval, or hands-on verification that cannot be delegated to inspection or experiment. It states exactly what the human must decide or check and what evidence/answer releases dependent work.

Use the cheapest reliable kind that can close the task: existing evidence before new work, `EXPLORE` before `EXPERIMENT`, and either before asking a human to discover a fact. Use `CHECKOUT` for human judgment or authority, not as a substitute for agent fact-finding. Do not create an `EXPLORE` step when inspection is already known to be unable to answer the question, and do not experiment when a search/read can settle it.

Use at least one `EXPLORE` or `EXPERIMENT` before an `IMPL` task when it reduces a real uncertainty; skip it when existing context is sufficient.

An `IMPL` task owns the implementation work for its product-code scope. Its How describes the concrete implementation approach and verification. It may be `ready` when available context is sufficient, with missing context recorded as a risk. Do not add separate lifecycle nodes merely to represent process steps. After implementation, the available evidence is reviewed against the task's expected result state and the way's purpose. A critical requirement or result contradiction should be reported and may be resolved by revising the existing way.

## Shared understanding with grill-me

When clarification is useful, run `@skills/grill-me`: read `../grill-me/SKILL.md` and follow its session sequence in this conversation. Do not delegate an active interview to a background agent or replace it with a custom questionnaire.

The interview is about **the user's goal and its ways**, not how to configure Wayfinder. It spans the planning process below:

- Start with grill-me's calibration using a concrete scenario from the goal when interactive clarification is useful. Ask for the user's answer, but if it is unavailable, mark the understanding provisional and continue with explicit assumptions. Teach only essential gaps and use its teach-back before decision rounds. Reuse already established understanding and decisions rather than restarting an active session.
- Use the goal's success signal, scope/exclusions, proposed ways and their boundaries, consequential unknowns, prerequisites, and safe parallel work as the decision tree. Settle parent scope before dependent decomposition; do not grill every routine implementation detail.
- Show a small draft way tree as proposals become grounded. Ask whether its outcomes and boundaries match the user's intent, not just whether the user agrees with a finished plan. Update the draft and affected dependencies after each answer.
- Let grill-me own question format, examples, mode selection, impact/uncertainty labels, and round size. Inspect repository facts yourself. Within this planning session, record unresolved fact-finding as `EXPLORE` or `EXPERIMENT` work rather than executing it automatically.
- Keep confirmed decisions, provisional assumptions, and unresolved evidence separate. A delegated choice such as “you decide” may adopt the recommendation provisionally; it does not establish an external fact or remove an evidence blocker.
- Before finalizing, summarize the understood goal, ways, ordering/parallel constraints, and remaining assumptions/blockers; invite confirmation using grill-me's question format when appropriate. A plan may remain explicitly provisional or partial; do not pretend its unknowns are resolved. If corrected, revise affected work.

## Ways and tasks

- A **way** is an outcome-oriented work package contributing to its parent. Every way, including the root goal, records:
  - **Purpose:** why this way exists and which need of its parent it serves.
  - **Current state:** the observed starting state, grounded in evidence; write `unknown` and name the resolving work when it cannot yet be established.
  - **Expected result state:** the observable state or capability that should exist when the way succeeds.
  - **Hypothesis:** why the planned work is expected to produce that result or advance the parent goal; keep it falsifiable rather than restating the expected result state.
  - **Assumptions:** conditions treated as true but not yet proven, each with evidence or an uncertainty task; write `—` when there are none rather than hiding assumptions.
- Siblings are normally all needed, not competing solutions.
- A **task** is a concrete `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT` action with a usable result and an observable completion signal. A way may contain tasks, sub-ways, or both.
- Every task should record a resolved absolute `Workdir` inside the recommended way directory, ending in its stable ID (for example, `/abs/path/ways/01-goal/0-goal/A1`). This declares artifact location without requiring the directory to exist before work starts. Task-specific artifact subdirectories are chosen by the task's How or the executing skill; never leave required paths relative.
- Give every node a stable, globally unique ID; every non-root node has exactly one parent. Dependencies are separate from parentage.
- Split only when children have distinct deliverables, prerequisites, uncertainties, or useful handoff boundaries. Collapse a wrapper that merely renames its only child.
- Stop when a task can be picked up without another planning round. Routine implementation choices can remain local; unresolved choices that change scope, boundaries, or safety must be explicit.
- Name the actual change or decision: `Preserve the trailing newline when serializing the buffer`, not `Implement serialization`. If a title could be pasted into an unrelated feature unchanged, rewrite or remove it.
- **Never append a fixed process sequence to each leaf.** Add a separate task only when a distinct decision, deliverable, integration, regression, or release check is needed. Put local checks in the task's completion signal. Product-code implementation is represented by an inline `Kind: IMPL` task at the relevant outcome, not by a lifecycle chain beneath every leaf.
- Keep detail proportional to the task: name relevant existing modules/files when known, but do not enumerate every function, class, command, or test case.

## Preferred ways and task order

- **Prefer the cheapest reliable method.** Reuse existing evidence first; use `EXPLORE` for search/read; use `EXPERIMENT` only when inspection cannot answer; use `CHECKOUT` only when human judgment, authority, or hands-on verification is required.
- Do not demand a complete or polished result at the beginning of a goal.
- Build a fast, simple first working happy-path vertical slice before broad edge-case hardening when safety permits.
- Then improve edge cases, security, and quality incrementally from the working system.
- Do not build polished automation first. Automation creates management cost; add it incrementally after cheap exploration or experimentation shows it is needed.

## Task details: Why, What, How

Every executable leaf, regardless of kind, must explain:

- **Workdir:** the resolved absolute task workspace path in the recorded way directory. An `IMPL` task also records **Target repo:** as a resolved absolute repository path. If either base is unknown, resolve it before finalizing rather than writing `./`, `~/`, or a path relative to the current shell.
- **Current state:** the observed starting condition for this task, grounded in evidence; write `unknown` and name the resolving work when it cannot yet be established.
- **Why:** the parent outcome it enables, risk it reduces, or downstream work it unblocks—and what fails or stays blocked if it is omitted. “Needed for the feature” is not a reason; remove work with no concrete justification.
- **What:** the specific behavior, decision, or artifact to deliver, with its scope and important boundaries. Do not just repeat the title. Keep **Expected result state** and **Done when** as separate statements: one describes the target state, and the other proves it exists.
- **How:** the concrete approach and steps needed to produce that result, including what to inspect/reuse/change and how to check it. Use a short ordered list when sequence matters; a single specific action suffices for a trivial task. A generic process list is not an approach. An `IMPL` task ends with implementation evidence reviewed against `What`, `Done when`, and the parent purpose.

Ground How in inspected context or explicit user decisions. If a consequential choice is unresolved, name the blocking `EXPLORE`, `EXPERIMENT`, or `CHECKOUT` task and what can happen before/after it; do not invent a mechanism or leave only “TBD.” For uncertainty work, Why is its impact, What is the evidence or decision to obtain, and How is the cheapest reliable resolving method. These are fields within the task, not extra child nodes or lifecycle stages.

## Planning process

1. **Ground the goal.** Use the shared-understanding session above when needed. Capture the success signal and scope with the user. Inspect the relevant `contexts/` directory and read applicable `*-facts-*`, `*-intents-*`, and `*-constraints-*` files, alongside any supplied way, relevant repository paths, existing behavior, and tests; all are read-only inputs, and defer the create/update decision. Distinguish confirmed facts (cite paths), user intent, constraints, assumptions, and unresolved questions or missing evidence. Do not plan rebuilding existing capabilities. If the goal or success signal is missing, clarify it before dependent planning or mark the plan provisional.
2. **Find consequential unknowns.** Look for gaps in behavior, integration contracts, feasibility, data safety, external dependencies, and validation. Record only those that could change the plan or prevent trustworthy completion; do not invent an uncertainty quota.
3. **Decompose by outcomes.** Identify the needed ways and concrete tasks using the rules above. For every way, state its purpose, current state, expected result state, falsifiable hypothesis, and assumptions before decomposing its children. Cover the goal once, including integration and failure handling where relevant. If an unknown changes a branch's decomposition, leave that branch explicitly partial instead of inventing children; continue independent branches.
4. **Wire prerequisites.** For each executable leaf, record the leaf IDs it needs and the result consumed from each. Include dependencies across ways. Share a prerequisite once rather than duplicating it under every consumer.
5. **Find the execution frontier.** Identify ready work, then describe which completions unlock which tasks, safe parallel lanes, shared-resource conflicts, and the final convergence check. Order by actual constraints, not by repeating development phases.
6. **Prune and validate the draft.** Check the planning criteria below. Keep blocked branches explicitly partial with their next resolving actions; do not claim unresolved work is verified.
7. **Finalize.** Summarize the shared understanding and invite correction or confirmation when useful. At the end, inspect the final plan against the available way files and recommend `create` or `update` with the resolved absolute target path and reason; do not ask for this choice at the beginning. Derive every task's absolute `Workdir` from that target and resolve every `IMPL` target repository before finalizing. Do not implement or create/update any way document; return the plan for the separate recording step.

## Uncertainty handling

Place each uncertainty at the smallest common parent of the work it affects. Represent it as `EXPLORE`, `EXPERIMENT`, or `CHECKOUT` according to the cheapest reliable resolution method, with:

- **Question and impact:** what is unknown and which choice, scope, or safety property depends on it.
- **Resolve by:** the cheapest reliable inspection, focused experiment, or owner decision; name the evidence source or responsible decision-maker.
- **Exit signal:** what evidence or decision closes the question. For experiments, state the method and distinguishing outcomes, including what to do if inconclusive.
- **Blocks:** affected task/way IDs and how different answers change the next work.

Use the uncertainty's ID as a prerequisite of known dependent tasks when the dependency is real. If their tasks cannot yet be named, mark the affected way `partial; risk noted for <ID>` and continue independent work. Do not block unrelated ways or require all uncertainties to resolve before implementation.

An uncertainty-resolution task can be ready while its consumers wait. Mark it done only with recorded evidence when available. If context is unavailable, use `EXPLORE` rather than claiming a repository fact. Escalate to `EXPERIMENT` only when read-only inspection cannot answer; use `CHECKOUT` only for a human-owned decision or check. If no consequential unknown remains, say why briefly; do not create a placeholder task.

Ask owner decisions through grill-me, with concrete examples, answer-dependent consequences, and a recommendation. Keep unresolved external-owner decisions as blockers when the current user cannot settle them.

## Dependencies and parallelism

- `Needs: —` means no prerequisite. Otherwise list executable leaf IDs plus the required result. A task becomes ready only when all its prerequisites are satisfied and its conditions hold.
- Use `ready`, `waiting` (unfinished prerequisites), `blocked` (unresolved uncertainty/decision), or `done` (evidence supplied). These statuses guide sequencing rather than create hard gates; the user may choose to proceed from `waiting` or `blocked` work after the risk is stated. An `IMPL` task is normally considered fully verified after its implementation evidence supports the expected result state and parent purpose, with the review recorded; if that evidence is missing, label the result unverified and state the risk rather than silently claiming success. Parent completion means its required children are complete; depend on the relevant leaves, not on parents or descendants of yourself.
- Dependencies must exist and be acyclic. Tree indentation and sibling order express scope/presentation, **not** a global serial schedule.
- Recommend parallel tasks only when there is no dependency path between them and their write surfaces, mutable resources, and contracts do not conflict. State the reason or required isolation/contract. Different branches alone do not establish independence.
- If work shares an unsettled interface, first plan the concrete contract decision that unlocks both sides. If work shares files/resources, sequence it or state an isolation and integration strategy. When context is insufficient, label parallelism conditional rather than promising it.
- Show readiness transitions, not mandatory batches: an unrelated slow task must not hold up a task whose own prerequisites are done. Never invent durations or call a chain the critical path without estimates.

## Output

During the interview, show only the draft context needed for the current questions. After shared-understanding confirmation, return a compact final plan with:

1. **Goal and grounding** — purpose, current state, expected result state, hypothesis, assumptions, success, scope, and key evidence.
2. **Way tree** — outcome-oriented ways and concrete leaves; give each way its purpose, current state, expected result state, hypothesis, assumptions, concise scope, and success signal, and mark partial branches.
3. **Work map** — one record per executable leaf: ID/title, kind (`EXPLORE | EXPERIMENT | IMPL | CHECKOUT`), absolute Workdir, absolute Target repo for `IMPL`, current state, Why, What, expected result state, How, needs (with reasons), status, and done when. Keep all IDs aligned with the tree. Use short task blocks so explanations and ordered steps remain readable instead of squeezing them into a wide table.
4. **Uncertainties** — question, impact, resolution method, exit signal, and affected IDs; or a grounded statement that none remain.
5. **Execution** — start now, unlocks/sequence, safe or conditional parallel lanes with reasons, convergence check, and next action. These summarize the work map, not a second conflicting schedule.
6. **Recording handoff** — recommend `create` or `update`; name the target directory, evidence for the recommendation, and any preservation/blocking condition. Explicitly say that no way document was changed and return the plan for the separate recording step.

Use a simple ELI5 word and sentence for a way's title and description when practical.

### Example shape — not a template of required tasks

Illustrative facts: insertion behavior is already agreed; the command loop and file writer are separate modules; their request/result contract is not yet agreed. Adapt to actual repository evidence.

```text
G  Add modal insertion and explicit saving
├── A  Edit the in-memory buffer
│   ├── A1  Route printable keys only in insert mode (IMPL)
│   └── A2  Keep cursor placement valid after insertion and mode exit (IMPL)
├── B  Save the current buffer without losing recoverable edits
│   ├── U1  Inspect current path and metadata behavior (EXPLORE)
│   ├── B1  Decide file policy and approve the save contract (CHECKOUT)
│   ├── B2  Dispatch write commands without exiting the session (IMPL)
│   └── B3  Persist the snapshot using the agreed file-safety policy (IMPL)
└── C  Check edit → save → reopen and failed-save recovery (CHECKOUT)
```

Example work-map entries (the actual output must cover every executable leaf):

### A1 — Route printable keys only in insert mode
- Kind: IMPL
- Workdir: /abs/path/ways/01-modal-editor/0-goal/A1
- Target repo: /abs/path/modal-editor
- Current state: Printable-key handling exists in the command loop, but its mode-specific mutation behavior is not yet established.
- Why: Enables text entry without making normal-mode navigation keys accidentally modify the buffer.
- What: Mode-aware routing of printable ASCII input; preserve existing normal-mode navigation. Cursor adjustment belongs to A2.
- Expected result state: Printable ASCII changes the buffer only in insert mode; normal mode retains navigation behavior.
- How:
  1. Route printable ASCII to buffer insertion only in insert mode; retain the existing normal-mode dispatch.
  2. Exercise the same printable key in both modes to check that only insert mode changes text.
- Needs: —
- Status: ready
- Done when: Insert mode changes text; normal-mode navigation does not.

### B3 — Persist the snapshot using the agreed file-safety policy
- Kind: IMPL
- Workdir: /abs/path/ways/01-modal-editor/0-goal/1-2/B3
- Target repo: /abs/path/modal-editor
- Current state: The writer's supported target paths and failure-preservation guarantees are not established until U1 and B1 complete.
- Why: Makes edits durable without destroying the original file or recoverable edits when a write fails.
- What: Save the snapshot from B1 to the supported target paths, returning success/failure through B1's contract. Command dispatch belongs to B2.
- Expected result state: Saved bytes match the approved snapshot, and a failed write preserves the original file and recoverable edits.
- How:
  1. Use B1's approved file policy and snapshot/result contract.
  2. Adapt the existing file-writer boundary to those guarantees and check saved bytes plus a forced write failure.
- Needs: B1: approved file policy and snapshot/result contract
- Status: blocked
- Done when: Saved bytes match the snapshot; forced failure preserves the original and recoverable edits.

U1 (`EXPLORE`; Workdir: `/abs/path/ways/01-modal-editor/0-goal/1-2/U1`): search and read file-opening behavior and supported paths. Exit: repository evidence about supported file types and preservation behavior is recorded, including a clear “not specified” result when applicable. Blocks B1, whose human `CHECKOUT` decides any policy the evidence cannot establish.

Execution: start A1 and U1 independently. A2 needs A1's insertion behavior; B1 needs U1's evidence; B2 and B3 need B1's approved contract. After B1, B2 and B3 can run in parallel if the separate-module boundary still holds. C joins A2, B2, and B3 for the human check of the real session and failed-save recovery.

## Completion criterion

- The goal and its ways have been discussed enough to act, with confirmation or clearly labeled provisional assumptions and partial branches.
- Every requested outcome is covered by concrete work or an explicitly partial branch with its risk or dependency named; existing work is not needlessly recreated.
- Every way, including the root, explicitly records its purpose, current state, expected result state, falsifiable hypothesis, and assumptions (`—` when none); these fields agree with its parent and inspected evidence.
- No generic lifecycle chains, renamed single-child wrappers, or `Test the tests` branches remain.
- Every executable leaf has a resolved absolute Workdir, evidence-grounded current state, concrete Why, scoped What, expected result state, actionable How (or named decision), relevant prerequisites, status, and observable completion signal. Every `IMPL` leaf also has a resolved absolute Target repo. No generic rationale or lifecycle boilerplate substitutes for task details. Planned evidence is labeled as planned or provisional.
- Every task uses exactly one allowed kind; every consequential uncertainty has a cheapest-reliable `EXPLORE`, `EXPERIMENT`, or `CHECKOUT` action and clearly scoped risks; every `IMPL` task records available context and unresolved uncertainties without inventing unsupported decomposition.
- IDs are unique, every non-root node has one parent, all dependency references resolve, and the dependency graph is acyclic.
- The execution summary matches dependencies, explains parallel safety/conflicts, and names an immediately useful next action (including an owner decision when that is all that can proceed).
- Each product-code handoff is represented by an inline `Kind: IMPL` leaf. Its recorded How describes the work and verification without prescribing a process sequence. A later review checks the available implementation evidence against the expected result state and way purpose. A critical requirement or result contradiction should be surfaced, and the existing way can be revised when needed.
- Wayfinder has only reported the confirmed plan: it has not created, updated, or written any way document. The final response returns the plan for the separate recording step.
