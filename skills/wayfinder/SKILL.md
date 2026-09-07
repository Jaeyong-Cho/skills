---
name: wayfinder
description: Plan one goal as concrete ways and tasks, with evidence-backed uncertainties, dependencies, execution order, and safe parallel work. Invoke as /wayfinder.
disable-model-invocation: true
---

# Wayfinder

Produce a task plan, not a lifecycle checklist. Answer:

> What work is actually needed, what do we not know yet, what can start now, and what must wait for what?

Planning only: inspect context, but do not implement, run experiments, write detailed designs, or invoke downstream skills. Propose evidence-gathering work when needed; never report a proposed check as completed.

## Ways and tasks

- A **way** is an outcome-oriented work package contributing to its parent. Siblings are normally all needed, not competing solutions.
- A **task** is a concrete action with a usable result and an observable completion signal. A way may contain tasks, sub-ways, or both.
- Give every node a stable, globally unique ID; every non-root node has exactly one parent. Dependencies are separate from parentage.
- Split only when children have distinct deliverables, prerequisites, uncertainties, or useful handoff boundaries. Collapse a wrapper that merely renames its only child.
- Stop when a task can be picked up without another planning round. Routine implementation choices can remain local; unresolved choices that change scope, boundaries, or safety must be explicit.
- Name the actual change or decision: `Preserve the trailing newline when serializing the buffer`, not `Implement serialization`. If a title could be pasted into an unrelated feature unchanged, rewrite or remove it.
- **Never append requirements → design → implement → test to each leaf.** Requirements and design become tasks only when a specific unresolved decision or contract needs its own deliverable. Put local checks in the task's completion signal; add separate verification tasks only for distinct integration, regression, or release work.
- Do not enumerate functions, classes, commands, or every test case. Include a short ordered procedure inside a task only when its sequence is not obvious from the action and completion signal.

## Planning process

1. **Ground the goal.** Capture the success signal and scope. Inspect supplied context and the relevant repository paths, existing behavior, and tests. Distinguish observed facts (cite paths), user decisions, assumptions, and missing evidence. Do not plan rebuilding existing capabilities. If the goal or success signal is missing, ask a focused question before proceeding.
2. **Find consequential unknowns.** Look for gaps in behavior, integration contracts, feasibility, data safety, external dependencies, and validation. Record only those that could change the plan or prevent trustworthy completion; do not invent an uncertainty quota.
3. **Decompose by outcomes.** Identify the needed ways and concrete tasks using the rules above. Cover the goal once, including integration and failure handling where relevant. If an unknown changes a branch's decomposition, leave that branch explicitly partial instead of inventing children; continue independent branches.
4. **Wire prerequisites.** For each executable leaf, record the leaf IDs it needs and the result consumed from each. Include dependencies across ways. Share a prerequisite once rather than duplicating it under every consumer.
5. **Find the execution frontier.** Identify ready work, then describe which completions unlock which tasks, safe parallel lanes, shared-resource conflicts, and the final convergence check. Order by actual constraints, not by repeating development phases.
6. **Prune and validate.** Apply the completion criterion below. Return a useful partial plan when blocked, with the next resolving action; do not claim the entire plan is executable.

## Uncertainty handling

Place each uncertainty at the smallest common parent of the work it affects. It is an executable leaf (kind `uncertainty`) with:

- **Question and impact:** what is unknown and which choice, scope, or safety property depends on it.
- **Resolve by:** the cheapest reliable inspection, focused experiment, or owner decision; name the evidence source or responsible decision-maker.
- **Exit signal:** what evidence or decision closes the question. For experiments, state the method and distinguishing outcomes, including what to do if inconclusive.
- **Blocks:** affected task/way IDs and how different answers change the next work.

Use the uncertainty's ID as a prerequisite of known dependent tasks. If their tasks cannot yet be named, mark the affected way `partial; blocked by <ID>` and return to decomposition after the answer. Do not block unrelated ways or require all uncertainties to resolve before any implementation.

An uncertainty can be ready to investigate while its consumers are blocked. Mark it done only with recorded evidence. If context is unavailable, say so and plan inspection rather than claiming a repository fact. If no consequential unknown remains, say why briefly; do not create an `Experiment` placeholder.

For an owner question, use a standalone block with choices, consequences, and a recommendation:

❓ **Q1** - **<decision>**: <question and consequences of each answer>

➡️ <recommended answer and reason; not an approved decision until answered>

## Dependencies and parallelism

- `Needs: —` means no prerequisite. Otherwise list executable leaf IDs plus the required result. A task becomes ready only when all its prerequisites are satisfied and its conditions hold.
- Use `ready`, `waiting` (unfinished prerequisites), `blocked` (unresolved uncertainty/decision), or `done` (evidence supplied). Propagate blockers to dependent work. Parent completion means its required children are complete; depend on the relevant leaves, not on parents or descendants of yourself.
- Dependencies must exist and be acyclic. Tree indentation and sibling order express scope/presentation, **not** a global serial schedule.
- Recommend parallel tasks only when there is no dependency path between them and their write surfaces, mutable resources, and contracts do not conflict. State the reason or required isolation/contract. Different branches alone do not establish independence.
- If work shares an unsettled interface, first plan the concrete contract decision that unlocks both sides. If work shares files/resources, sequence it or state an isolation and integration strategy. When context is insufficient, label parallelism conditional rather than promising it.
- Show readiness transitions, not mandatory batches: an unrelated slow task must not hold up a task whose own prerequisites are done. Never invent durations or call a chain the critical path without estimates.

## Output

Keep the plan compact, but include the information needed to act:

1. **Goal and grounding** — success, scope, key evidence/assumptions.
2. **Way tree** — outcome-oriented ways and concrete leaves; give each way a concise scope and success signal, and mark partial branches.
3. **Work map** — one row per executable leaf: ID, kind (`task | uncertainty | checkpoint`), action/result, needs (with reasons), status, and done when. Keep all IDs aligned with the tree. Add short task-specific procedures only where useful.
4. **Uncertainties** — question, impact, resolution method, exit signal, and affected IDs; or a grounded statement that none remain.
5. **Execution** — start now, unlocks/sequence, safe or conditional parallel lanes with reasons, convergence check, and next action. These summarize the work map, not a second conflicting schedule.

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
│   └── B3  Persist the snapshot using the agreed file-safety policy
└── C  Verify edit → save → reopen and recovery after a failed save
```

Example work-map entries (the actual output must cover every executable leaf):

| ID | Kind | Action/result | Needs | Status | Done when |
|----|------|---------------|-------|--------|-----------|
| A1 | task | Route printable keys only in insert mode | — | ready | Insert mode changes text; normal-mode navigation does not |
| B1 | task | Agree save request/result and snapshot contract | — | ready | Both modules can work from one documented contract, including failure results |
| B3 | task | Persist snapshot using agreed safety policy | U1: file policy; B1: snapshot/result contract | blocked | Saved bytes match snapshot; forced failure preserves original and recoverable edits |

U1: inspect file-opening behavior and supported paths; ask the owner if policy is unspecified. Exit: supported file types and preservation guarantees are recorded. Blocks B3: replace-by-rename may work for regular files, but symlink/metadata requirements may change the strategy. Do not choose one without evidence.

Execution: start A1, B1, and the U1 inspection independently. A2 needs A1's insertion behavior; B2 needs B1's command contract; B3 needs B1 and U1. B2 need not wait for U1. After B1, B2 and B3 can run in parallel once U1 is resolved, provided the separate-module boundary holds. C joins A2, B2, and B3 to verify the real session and failed-save recovery.

## Completion criterion

- Every requested outcome is covered by concrete work or an explicitly blocked partial branch; existing work is not needlessly recreated.
- No generic lifecycle chains, renamed single-child wrappers, or `Test the tests` branches remain.
- Every executable leaf has a useful deliverable, correct prerequisites, status, and observable completion signal. Planned evidence is not presented as fact.
- Every consequential uncertainty has a resolving action and clearly scoped blockers; there is no guessed decomposition behind a blocker.
- IDs are unique, every non-root node has one parent, all dependency references resolve, and the dependency graph is acyclic.
- The execution summary matches dependencies, explains parallel safety/conflicts, and names an immediately useful next action (including an owner decision when that is all that can proceed).
