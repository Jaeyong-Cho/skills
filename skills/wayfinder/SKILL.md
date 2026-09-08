---
name: wayfinder
description: Use grill-me to reach shared understanding of one goal and its ways, then create or update a recorded way with concrete tasks, uncertainties, dependencies, and safe parallel work. Invoke as /wayfinder.
disable-model-invocation: true
---

# Wayfinder

Produce a task plan, not a lifecycle checklist. Answer:

> What work is actually needed, what do we not know yet, what can start now, and what must wait for what?

Plan first: use grill-me for the user conversation and inspect context, but do not implement or run experiments. After the user confirms the plan, persist it only when requested: use `@skills/to-way` to create a new way or update the matching existing way. Propose evidence-gathering work when needed; never report a proposed check as completed.

## Create or update a way

- Inspect the supplied way path, or `./ways/`, as context before planning. Do not ask the user to choose create or update at the beginning.
- Decide and recommend the operation at the end, after the plan and target have been inspected: create a new numbered way for a new goal; update the matching goal in place for an existing goal; update the parent goal when adding a child way.
- For updates, preserve stable IDs, completed-work evidence, and user annotations; add new nodes with globally unique IDs.
- If updating would move or remove files, strand old tasks, or conflict with recorded evidence, stop and ask before changing them.
- Do not write either form before the shared-understanding confirmation. If the user wants planning only, return the confirmed plan and the model's recommended operation without invoking `@skills/to-way`.

## Implementation tasks

- When a leaf changes product code, mark that leaf `Kind: IMPL`. `IMPL` is a task kind, not a separate way or root-level node; an existing leaf ID such as `A4` or `B3` remains its stable ID.
- An `IMPL` task owns the implementation handoff for its product-code scope. Its ordered How is `/req` → `/ood` → `/to-plan` → `/do-plan`; use existing approved artifacts and start at the first missing handoff stage when possible.
- Do not add separate `REQ`, `OOD`, `TO-PLAN`, or `DO-PLAN` nodes for individual ways or tasks. Do not expand the handoff into lifecycle children. Multiple ways may contain their own `IMPL` task when their product-code work has a separate handoff.
- An `IMPL` task can be `ready` when its Wayfinder prerequisites are satisfied, but that readiness does not authorize direct implementation. `/next-way` recommends it like any other ready task and alerts the user to run the handoff skills; it never invokes them or implements the task.

## Shared understanding with grill-me

**MUST RUN `@skills/grill-me`**: read `../grill-me/SKILL.md` and follow its session sequence in this conversation. Do not merely recommend that the user launch it, delegate the interview to a background agent, or replace it with a custom questionnaire.

The interview is about **the user's goal and its ways**, not how to configure Wayfinder. It spans the planning process below:

- Start with grill-me's calibration using a concrete scenario from the goal, then wait for the user's answer. Teach only essential gaps and use its teach-back before decision rounds. Reuse already established understanding and decisions rather than restarting an active session.
- Use the goal's success signal, scope/exclusions, proposed ways and their boundaries, consequential unknowns, prerequisites, and safe parallel work as the decision tree. Settle parent scope before dependent decomposition; do not grill every routine implementation detail.
- Show a small draft way tree as proposals become grounded. Ask whether its outcomes and boundaries match the user's intent, not just whether the user agrees with a finished plan. Update the draft and affected dependencies after each answer.
- Let grill-me own question format, examples, mode selection, impact/uncertainty labels, and round size. Inspect repository facts yourself. Within this planning session, record proposed experiments as uncertainty-resolution tasks rather than executing them automatically.
- Keep confirmed decisions, provisional assumptions, and unresolved evidence separate. A delegated choice such as “you decide” may adopt the recommendation provisionally; it does not establish an external fact or remove an evidence blocker.
- Before finalizing, summarize the agreed goal, ways, ordering/parallel constraints, and remaining assumptions/blockers; ask for confirmation using grill-me's question format and wait. Confirmation may approve an explicitly partial plan, not pretend its unknowns are resolved. If corrected, revise affected work and confirm again.

## Ways and tasks

- A **way** is an outcome-oriented work package contributing to its parent. Siblings are normally all needed, not competing solutions.
- A **task** is a concrete action with a usable result and an observable completion signal. A way may contain tasks, sub-ways, or both.
- Give every node a stable, globally unique ID; every non-root node has exactly one parent. Dependencies are separate from parentage.
- Split only when children have distinct deliverables, prerequisites, uncertainties, or useful handoff boundaries. Collapse a wrapper that merely renames its only child.
- Stop when a task can be picked up without another planning round. Routine implementation choices can remain local; unresolved choices that change scope, boundaries, or safety must be explicit.
- Name the actual change or decision: `Preserve the trailing newline when serializing the buffer`, not `Implement serialization`. If a title could be pasted into an unrelated feature unchanged, rewrite or remove it.
- **Never append requirements → design → implement → test to each leaf.** Requirements and design become tasks only when a specific unresolved decision or contract needs its own deliverable. Put local checks in the task's completion signal; add separate verification tasks only for distinct integration, regression, or release work. Product-code implementation is represented by an inline `Kind: IMPL` task at the relevant outcome, not by a lifecycle chain beneath every leaf.
- Keep detail proportional to the task: name relevant existing modules/files when known, but do not enumerate every function, class, command, or test case.

## Prefered Ways and Tasks Order
- At the beginning of the starting goal, I don't want to fully completed output and result.
- Uncertainty should be resolved with `/experience` or just explore. **MUST USE** a cheapest method.
- Build first **fast**, **simple**, **not perfect** something first, It is important to see the **first working happy path vertical slice**. **Verification** for details should be later. 
- After that review the edge cases, security and improvement for reach a perfect.
- Increamentally improve and building a positive working loop and system from the working system.
- Do not well made automation first. The automation system is create management effort. Fast experiment, finding uncertainty first, building automation system increamentally after. 

## Task details: Why, What, How

Every executable leaf, including uncertainty and checkpoint work, must explain:

- **Why:** the parent outcome it enables, risk it reduces, or downstream work it unblocks—and what fails or stays blocked if it is omitted. “Needed for the feature” is not a reason; remove work with no concrete justification.
- **What:** the specific behavior, decision, or artifact to deliver, with its scope and important boundaries. Do not just repeat the title. Keep **Done when** as the separate observable proof that this result exists.
- **How:** the concrete approach and steps needed to produce that result, including what to inspect/reuse/change and how to check it. Use a short ordered list when sequence matters; a single specific action suffices for a trivial task. “Define requirements, design, implement, test” is not an approach.

Ground How in inspected context or explicit user decisions. If a consequential choice is unresolved, name the blocking uncertainty and what can be done before/after its resolution; do not invent a mechanism or leave only “TBD.” For uncertainty work, Why is its impact, What is the evidence/decision to obtain, and How is the resolving method; reuse those details rather than duplicating them. These are fields within the task, not extra child nodes or lifecycle stages.

## Planning process

1. **Start grill-me and ground the goal.** Begin the shared-understanding session above. Capture the success signal and scope with the user. Inspect any supplied way plus relevant repository paths, existing behavior, and tests, but defer the create/update decision. Distinguish observed facts (cite paths), user decisions, assumptions, and missing evidence. Do not plan rebuilding existing capabilities. If the goal or success signal is missing, clarify it through grill-me before dependent planning.
2. **Find consequential unknowns.** Look for gaps in behavior, integration contracts, feasibility, data safety, external dependencies, and validation. Record only those that could change the plan or prevent trustworthy completion; do not invent an uncertainty quota.
3. **Decompose by outcomes.** Identify the needed ways and concrete tasks using the rules above. Cover the goal once, including integration and failure handling where relevant. If an unknown changes a branch's decomposition, leave that branch explicitly partial instead of inventing children; continue independent branches.
4. **Wire prerequisites.** For each executable leaf, record the leaf IDs it needs and the result consumed from each. Include dependencies across ways. Share a prerequisite once rather than duplicating it under every consumer.
5. **Find the execution frontier.** Identify ready work, then describe which completions unlock which tasks, safe parallel lanes, shared-resource conflicts, and the final convergence check. Order by actual constraints, not by repeating development phases.
6. **Prune and validate the draft.** Check the planning criteria below. Keep blocked branches explicitly partial with their next resolving actions; do not claim the entire plan is executable.
7. **Confirm and finalize.** Complete grill-me's shared-understanding confirmation and wait for the user's answer. At the end, inspect the final plan against the available way files and recommend `create` or `update` with the target path and reason; do not ask for this choice at the beginning. Only after confirmation return the final plan in the output format below. If persistence was requested, invoke `@skills/to-way` with that recommendation; corrections reopen the affected decisions. Do not implement or record files before confirmation.

## Uncertainty handling

Place each uncertainty at the smallest common parent of the work it affects. It is an executable leaf (kind `uncertainty`) with:

- **Question and impact:** what is unknown and which choice, scope, or safety property depends on it.
- **Resolve by:** the cheapest reliable inspection, focused experiment, or owner decision; name the evidence source or responsible decision-maker.
- **Exit signal:** what evidence or decision closes the question. For experiments, state the method and distinguishing outcomes, including what to do if inconclusive.
- **Blocks:** affected task/way IDs and how different answers change the next work.

Use the uncertainty's ID as a prerequisite of known dependent tasks. If their tasks cannot yet be named, mark the affected way `partial; blocked by <ID>` and return to decomposition after the answer. Do not block unrelated ways or require all uncertainties to resolve before any implementation.

An uncertainty can be ready to investigate while its consumers are blocked. Mark it done only with recorded evidence. If context is unavailable, say so and plan inspection rather than claiming a repository fact. If no consequential unknown remains, say why briefly; do not create an `Experiment` placeholder.

Ask owner decisions through grill-me, with concrete examples, answer-dependent consequences, and a recommendation. Keep unresolved external-owner decisions as blockers when the current user cannot settle them.

## Dependencies and parallelism

- `Needs: —` means no prerequisite. Otherwise list executable leaf IDs plus the required result. A task becomes ready only when all its prerequisites are satisfied and its conditions hold.
- Use `ready`, `waiting` (unfinished prerequisites), `blocked` (unresolved uncertainty/decision), or `done` (evidence supplied). Propagate blockers to dependent work. Parent completion means its required children are complete; depend on the relevant leaves, not on parents or descendants of yourself.
- Dependencies must exist and be acyclic. Tree indentation and sibling order express scope/presentation, **not** a global serial schedule.
- Recommend parallel tasks only when there is no dependency path between them and their write surfaces, mutable resources, and contracts do not conflict. State the reason or required isolation/contract. Different branches alone do not establish independence.
- If work shares an unsettled interface, first plan the concrete contract decision that unlocks both sides. If work shares files/resources, sequence it or state an isolation and integration strategy. When context is insufficient, label parallelism conditional rather than promising it.
- Show readiness transitions, not mandatory batches: an unrelated slow task must not hold up a task whose own prerequisites are done. Never invent durations or call a chain the critical path without estimates.

## Output

During the interview, show only the draft context needed for the current questions. After shared-understanding confirmation, return a compact final plan with:

1. **Goal and grounding** — success, scope, key evidence/assumptions.
2. **Way tree** — outcome-oriented ways and concrete leaves; give each way a concise scope and success signal, and mark partial branches.
3. **Work map** — one record per executable leaf: ID/title, kind (`task | uncertainty | checkpoint`), Why, What, How, needs (with reasons), status, and done when. Keep all IDs aligned with the tree. Use short task blocks so explanations and ordered steps remain readable instead of squeezing them into a wide table.
4. **Uncertainties** — question, impact, resolution method, exit signal, and affected IDs; or a grounded statement that none remain.
5. **Execution** — start now, unlocks/sequence, safe or conditional parallel lanes with reasons, convergence check, and next action. These summarize the work map, not a second conflicting schedule.
6. **Persistence** — the model's end-of-plan recommendation: `create`, `update`, or planning-only; name the target directory, evidence for the recommendation, and any preservation/blocking condition.

**MUST USE** a simple ELI5 word and sentence for a way's title and description. 

### Example shape — not a template of required tasks

Illustrative facts: insertion behavior is already agreed; the command loop and file writer are separate modules; their request/result contract is not yet agreed. Adapt to actual repository evidence.

```text
G  Add modal insertion and explicit saving
├── A  Edit the in-memory buffer
│   ├── A1  Route printable keys only in insert mode
│   └── A2  Keep cursor placement valid after insertion and mode exit
├── B  Save the current buffer without losing recoverable edits
│   ├── U1  Determine whether saving must preserve symlinks and file metadata
│   ├── B1  Agree the save request/result and buffer snapshot contract
│   ├── B2  Dispatch write commands without exiting the session
│   └── B3  Persist the snapshot using the agreed file-safety policy (IMPL)
└── C  Verify edit → save → reopen and recovery after a failed save
```

Example work-map entries (the actual output must cover every executable leaf):

### A1 — Route printable keys only in insert mode
- Kind: task
- Why: Enables text entry without making normal-mode navigation keys accidentally modify the buffer.
- What: Mode-aware routing of printable ASCII input; preserve existing normal-mode navigation. Cursor adjustment belongs to A2.
- How:
  1. Trace the existing key-dispatch and mode state paths.
  2. Route printable ASCII to buffer insertion only in insert mode; retain the existing normal-mode dispatch.
  3. Exercise the same printable key in both modes to check that only insert mode changes text.
- Needs: —
- Status: ready
- Done when: Insert mode changes text; normal-mode navigation does not.

### B3 — Persist the snapshot using the agreed file-safety policy
- Kind: IMPL
- Why: Makes edits durable without destroying the original file or recoverable edits when a write fails.
- What: Save the snapshot from B1 to the supported target paths, returning success/failure through B1's contract. Command dispatch belongs to B2.
- How:
  1. Run `/req` for the complete goal, `/ood` for the approved requirement batch, `/to-plan` for the resulting implementation plan, and `/do-plan` for that approved plan, starting at the first missing artifact.
  2. Resolve U1's file-policy decision and B1's snapshot/result contract.
  3. Adapt the existing file-writer boundary to those guarantees and check saved bytes plus a forced write failure. Select the persistence mechanism after U1, not by assuming replace-by-rename is safe.
- Needs: U1: file policy; B1: snapshot/result contract
- Status: blocked
- Done when: Saved bytes match the snapshot; forced failure preserves the original and recoverable edits.

U1: inspect file-opening behavior and supported paths; ask the owner if policy is unspecified. Exit: supported file types and preservation guarantees are recorded. Blocks B3: replace-by-rename may work for regular files, but symlink/metadata requirements may change the strategy. Do not choose one without evidence.

Execution: start A1, B1, and the U1 inspection independently. A2 needs A1's insertion behavior; B2 needs B1's command contract; B3 needs B1 and U1. B2 need not wait for U1. After B1, B2 and B3 can run in parallel once U1 is resolved, provided the separate-module boundary holds. C joins A2, B2, and B3 to verify the real session and failed-save recovery.

## Completion criterion

- Grill-me has established shared understanding of the goal and its ways, and the user has confirmed the summary, including any provisional assumptions and partial branches.
- Every requested outcome is covered by concrete work or an explicitly blocked partial branch; existing work is not needlessly recreated.
- No generic lifecycle chains, renamed single-child wrappers, or `Test the tests` branches remain.
- Every executable leaf has a concrete Why, scoped What, actionable How (or named blocking decision), correct prerequisites, status, and observable completion signal. No generic rationale or lifecycle boilerplate substitutes for task details. Planned evidence is not presented as fact.
- Every consequential uncertainty has a resolving action and clearly scoped blockers; there is no guessed decomposition behind a blocker.
- IDs are unique, every non-root node has one parent, all dependency references resolve, and the dependency graph is acyclic.
- The execution summary matches dependencies, explains parallel safety/conflicts, and names an immediately useful next action (including an owner decision when that is all that can proceed).
- Each product-code handoff is represented by an inline `Kind: IMPL` leaf, and `/next-way` recommends it with the handoff alert instead of executing it; no separate `IMPL` way or lifecycle chain exists.
