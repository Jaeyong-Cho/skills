---
name: to-way
description: Create or update a Wayfinder task plan as navigable Markdown work packages, preserving task kinds, uncertainties, prerequisites, parallel execution guidance, and completed-task evidence. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Create or update one Wayfinder plan without redesigning or executing it. Preserve every way's purpose, current state, expected result state, hypothesis, assumptions, grounding, tree, each task's kind/current state/Why/What/How/expected result state, uncertainty details, dependencies, conditions, completion signals, execution guidance, and evidence for completed tasks. A tree alone is insufficient if the information needed to execute its leaves is missing.

## Layout: files for ways, tasks inline

- Write `0-goal.md` for the root and one group file per **way** (work package).
- Keep `EXPLORE`, `EXPERIMENT`, `IMPL`, and `CHECKOUT` leaves inside their immediate parent's file, with an explicit anchor for each source ID. These are inline task kinds, not ways or lifecycle-stage directories. Do not create one-line task files or lifecycle-stage directories.
- A child way at depth `D`, sibling position `N`, uses `{D}-{N}-{slug}.md`. Count positions in the original tree, including inline leaves; gaps in file numbering are valid.
- Child way files live in a directory matching the parent's numeric path key (`0-goal`, `1-2`, etc.), not its logical source ID (`G`, `B`, etc.). Preserve the full ancestry to avoid collisions.
- Numbers preserve presentation order, **not** prerequisites or mandatory serial execution. Dependencies determine readiness and parallelism.
- Preserve source IDs in content; do not replace them with filename numbers.
- Keep every task inline, and record its workspace as a resolved absolute path to a directory named exactly by its source ID.
- Put the workspace beside its owning group file: a task in `0-goal.md` uses `<absolute-goal>/<ID>/`; a task in a child group file uses `<absolute-goal>/<parent-numeric-dir>/<ID>/`.
- Declare the absolute workspace path for every task, but do not create an untouched task's directory. Store task artifacts beneath it using directories chosen by the task's recorded How or the executing skill. Every `IMPL` task also records its resolved absolute target repository path.

For the illustrative modal-editing plan in Wayfinder:

```text
ways/01-add-modal-insertion-and-saving/
├── 0-goal.md                         # G, execution overview, inline CHECKOUT C
└── 0-goal/
    ├── 1-1-edit-the-buffer.md        # A, inline tasks A1 and A2
    └── 1-2-save-the-buffer.md        # B, inline U1 and tasks B1–B3
```

If B contains a sub-way in position 2, that sub-way's file is `0-goal/1-2/2-2-{slug}.md`. A goal with only tasks needs only `0-goal.md`.

## Workflow

1. **Gather and validate before writing.** Use the supplied plan or the complete Wayfinder result in the session, including its work map and execution notes. If missing, ask for it. Check:
   - one goal root, unique IDs, exactly one parent per non-root node;
   - every way, including the root, has a purpose, evidence-grounded current state, observable expected result state, falsifiable hypothesis, and explicit assumptions (`—` when none), consistent with its parent and evidence; the current state must not be invented when evidence is unavailable;
   - concrete domain work rather than repeated lifecycle chains;
   - every executable leaf has exactly one allowed kind: `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT`; none is a separate way or root-level node;
   - `EXPLORE` is read-only search/inspection, `EXPERIMENT` resolves an uncertainty through an isolated trial, `IMPL` changes production code only after its context/uncertainty prerequisites are done, and `CHECKOUT` is a human decision/approval/check;
   - the selected kind is the cheapest reliable method: no experiment when read/search can answer, and no human fact-finding when the agent can inspect or experiment;
   - every executable leaf has a resolved absolute Workdir, evidence-grounded current state, concrete Why (purpose/consequence of omission), What (scoped result), How (approach/steps or explicit blocking decision), expected result state, prerequisites (explicitly none where appropriate), status, and completion signal; every `IMPL` leaf also has a resolved absolute Target repo;
   - uncertainties retain their question, impact, resolving action, exit signal, and affected IDs;
   - dependency references exist, point to executable leaves, and contain no cycles;
   - readiness and parallel guidance do not contradict prerequisites or recorded resource conflicts;
   - every `done` task has supplied completion evidence; an `IMPL` task has a review of its implementation evidence against the expected result state and parent purpose. Never infer evidence from its title, status, green build, or commit alone.

   Explicitly partial branches blocked by named uncertainties are valid; retain their limits. Missing planning information is not permission to invent it. For a legacy requirements/design/implement/test tree or other invalid source, explain the missing decisions and ask for a revised Wayfinder plan. Do not silently upgrade it or serialize empty placeholders.
2. **Recommend create or update after inspection.** Reuse a destination confirmed in this session; otherwise ask one standalone question, recommending `./ways/`:

   ❓ **Q1** - **Destination**: Where should this plan be recorded?

   ➡️ `./ways/` in the current directory, under a numbered goal directory.

   Do not ask the user to choose create or update at the beginning. Inspect the confirmed destination and recommend the operation after validation: create `ways/{nn}-{slug}/` using the next sequence number for a new goal; update the matching goal directory in place for an existing goal or new child way. Preserve stable IDs, user annotations, completed-work evidence, and existing `done` statuses. Add new nodes with globally unique IDs.

   If a revised tree would move or remove files, strand tasks, or conflict with recorded evidence, show the affected paths and ask before changing them. A completed task omitted from a revised plan is not silently deleted; preserve it or get explicit removal confirmation.
3. **Map and write.** Resolve the destination to an absolute path, then build one source-ID → file/anchor/workdir mapping for the entire plan before writing. Root and ways own files; every executable leaf appears exactly once as a section in its parent's file. Link child ways and cross-way prerequisites using relative Markdown links, but write every task Workdir and every `IMPL` Target repo as absolute paths. Preserve all source notes at their owning node. In update mode, merge new/changed nodes into the existing files and retain annotations/evidence that the source did not supersede; do not fabricate descriptions, signals, or done evidence. If an active task or supplied artifact has a workspace, create or preserve its `<ID>/` directory beside the owning group file; do not create untouched task directories. Task-specific artifacts remain under the recorded workspace.
4. **Record progress explicitly.** Preserve an existing `Status: in-progress` marker during updates. When work starts, record `Status: in-progress`; when the source supplies evidence that a task finished, write `Status: done` and retain the evidence beside that status. Keep not-started tasks `ready`, `waiting`, or `blocked`; do not infer completion because a dependent task is done. If a task is marked done without evidence, stop and request the evidence instead of writing a false completion.
5. **Check the recorded plan.** Compare every way's purpose/current state/expected result state/hypothesis/assumptions and every task's Workdir, Target repo when applicable, current state/Why/What/How/expected result state, dependency, uncertainty, condition, completion signal, status, and completion evidence with its recorded location. Preserve ordered How steps and their evidence references; do not compress them into a generic action label. Verify links/anchors resolve, sibling order is preserved, paths do not collide, and the root execution overview still matches the task dependencies. No generic lifecycle nodes, unsupported parallel claims, lost annotations, or unproven `done` statuses may be introduced by serialization.
6. **Report.** Give the model-recommended operation (`created` or `updated`), output directory, root entry point, group-file count, and any remaining blockers. Summarize created/updated ways and the IDs recorded as done; do not dump every inline task as a file path.

No JSON, implementation, detailed design documents, or new planning decisions.

## Group file format

```markdown
---
type: Way Group
title: <node title>
description: <source summary>
tags: [wayfinder, task-plan]
timestamp: <ISO 8601 datetime>
---

# <node title>

## Outcome
- ID: <source ID>
- Position: <D-N; 0 for root; presentation only>
- Parent: <relative link; omit for root>
- Purpose: <why this way exists and which need of its parent it serves>
- Current state: <observed starting state, grounded in evidence; use `unknown` and link the resolving work when unavailable>
- Expected result state: <observable state or capability when successful>
- Hypothesis: <falsifiable reason this work should produce the result or advance the parent>
- Assumptions: <explicit conditions with evidence/uncertainty links, or —>
- Success: <source completion signal>
- Scope/status: <source scope, conditions, partial/blocked status if present>

## Work
<Direct children in source order: link each child way; render each leaf using the section format below.>

## Context and uncertainties
<Source evidence, assumptions, decisions, and package-level notes. Uncertainty leaves live in Work, not duplicated here. Omit this section if empty.>
```

For each inline leaf in `Work`:

```markdown
<a id="B3"></a>
### B3 — <concrete task title>
- Kind: <EXPLORE | EXPERIMENT | IMPL | CHECKOUT>
- Current state: <observed starting condition, grounded in evidence; use `unknown` and name the resolving work when unavailable>
- Why: <source purpose, parent outcome, and consequence of omitting this task>
- What: <source behavior/decision/artifact and scope boundaries>
- Expected result state: <target state this task must produce>
- How: <source approach; preserve ordered steps as a nested list when present, including any named blocking decision>
- Needs: <linked prerequisite IDs and the result needed from each; or —>
- Status: <ready | in-progress | waiting | blocked | done, with source evidence where supplied>
- Workdir: <resolved absolute `<ID>/` task workspace; always present even before creation> not repo path.
- Target repo: <resolved absolute repository path; IMPL only>
- Evidence: <proof for a done status; for IMPL include a review of implementation evidence against `What`, `Done when`, and parent purpose; required only when done>
- Done when: <observable completion signal>
- Conditions/conflicts: <only if present in source>

<For an uncertainty-resolving EXPLORE, EXPERIMENT, or CHECKOUT task, retain the question, impact, resolving method/owner, exit signal, blocked IDs, and answer-dependent consequences. Reuse Why/What/How rather than duplicating them. For an IMPL task, preserve only the implementation approach and verification explicitly present in the source; do not infer process steps.>
```

An intra-file prerequisite can link to `[B1](#B1)`; a cross-way prerequisite links to its owning file and anchor, e.g. `[A2](1-1-edit-the-buffer.md#A2)` from the sibling B file. Use explicit anchors matching source IDs rather than title-derived anchors.

The root additionally contains:

- **Grounding:** goal context, evidence, assumptions, and exclusions from the source.
- **Way tree:** the source hierarchy as a compact linked index, including inline leaf anchors.
- **Execution:** start-now tasks, dependency-driven unlocks, parallel lanes and their safety conditions, conflicts, convergence check, and next action. Link referenced IDs to their owning files/anchors. Preserve partial-plan warnings and owner questions.

Do not infer new prerequisites or parallel lanes from file numbers. If a needed field is missing rather than explicitly unknown/blocked, return to validation instead of inserting `Planned` or `None` as filler.

## Completion criterion

Every source node has exactly one canonical location; every task records its resolved absolute Workdir and every `IMPL` task records its resolved absolute Target repo; every way preserves its purpose, evidence-grounded current state, expected result state, hypothesis, and assumptions; every task preserves its current state and expected result state; all planning meaning survives recording, every link resolves, and a reader can start at `0-goal.md` to find what can proceed, what must wait and why, how to resolve blockers, and what proves completion. Every leaf retains one of `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT`; `IMPL` leaves remain inline with their implementation approach and review evidence preserved. New goals are created without collisions, existing goals are updated in place, task workspaces are created only when work or artifacts require them, annotations and in-progress/completed tasks are preserved, and every recorded `done` status has evidence. No redundant task files, lost dependency edges, invented work, or unapproved migration remains.
