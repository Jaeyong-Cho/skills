---
name: to-way
description: Create or update a Wayfinder task plan as navigable Markdown work packages, preserving uncertainties, prerequisites, parallel execution guidance, and completed-task evidence. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Create or update one Wayfinder plan without redesigning or executing it. Preserve its goal, grounding, tree, each task's Why/What/How, uncertainty details, dependencies, conditions, completion signals, execution guidance, and evidence for completed tasks. A tree alone is insufficient if the information needed to execute its leaves is missing.

## Layout: files for ways, tasks inline

- Write `0-goal.md` for the root and one group file per **way** (work package).
- Keep task, uncertainty, and checkpoint leaves inside their immediate parent's file, with an explicit anchor for each source ID. Do not create one-line task files or lifecycle-stage directories.
- A child way at depth `D`, sibling position `N`, uses `{D}-{N}-{slug}.md`. Count positions in the original tree, including inline leaves; gaps in file numbering are valid.
- Child way files live in a directory matching the parent's numeric path key (`0-goal`, `1-2`, etc.), not its logical source ID (`G`, `B`, etc.). Preserve the full ancestry to avoid collisions.
- Numbers preserve presentation order, **not** prerequisites or mandatory serial execution. Dependencies determine readiness and parallelism.
- Preserve source IDs in content; do not replace them with filename numbers.
- Keep task, uncertainty, and checkpoint details inline, but give a task an optional workspace directory named exactly by its source ID when work starts or it owns an artifact.
- Put the workspace beside its owning group file: a task in `0-goal.md` uses `<goal>/<ID>/`; a task in a child group file uses `<goal>/<parent-numeric-dir>/<ID>/`.
- Store task-specific artifacts in that workspace, such as `experiment/`, `req/`, or `design/`. Do not create empty workspaces for untouched tasks.

For the illustrative modal-editing plan in Wayfinder:

```text
ways/01-add-modal-insertion-and-saving/
├── 0-goal.md                         # G, execution overview, inline checkpoint C
└── 0-goal/
    ├── 1-1-edit-the-buffer.md        # A, inline tasks A1 and A2
    ├── A1/                            # optional workspace for task A1
    │   └── experiment/
    └── 1-2-save-the-buffer.md        # B, inline U1 and tasks B1–B3
```

If B contains a sub-way in position 2, that sub-way's file is `0-goal/1-2/2-2-{slug}.md`. A goal with only tasks needs only `0-goal.md`.

## Workflow

1. **Gather and validate before writing.** Use the supplied plan or the complete Wayfinder result in the session, including its work map and execution notes. If missing, ask for it. Check:
   - one goal root, unique IDs, exactly one parent per non-root node;
   - concrete domain work rather than repeated lifecycle chains;
   - every executable leaf has a concrete Why (purpose/consequence of omission), What (scoped result), How (approach/steps or explicit blocking decision), prerequisites (explicitly none where appropriate), status, and completion signal;
   - uncertainties retain their question, impact, resolving action, exit signal, and affected IDs;
   - dependency references exist, point to executable leaves, and contain no cycles;
   - readiness and parallel guidance do not contradict prerequisites or recorded resource conflicts;
   - every `done` task has supplied completion evidence; never infer evidence from its title or status alone.

   Explicitly partial branches blocked by named uncertainties are valid; retain their limits. Missing planning information is not permission to invent it. For a legacy requirements/design/implement/test tree or other invalid source, explain the missing decisions and ask for a revised Wayfinder plan. Do not silently upgrade it or serialize empty placeholders.
2. **Recommend create or update after inspection.** Reuse a destination confirmed in this session; otherwise ask one standalone question, recommending `./ways/`:

   ❓ **Q1** - **Destination**: Where should this plan be recorded?

   ➡️ `./ways/` in the current directory, under a numbered goal directory.

   Do not ask the user to choose create or update at the beginning. Inspect the confirmed destination and recommend the operation after validation: create `ways/{nn}-{slug}/` using the next sequence number for a new goal; update the matching goal directory in place for an existing goal or new child way. Preserve stable IDs, user annotations, completed-work evidence, and existing `done` statuses. Add new nodes with globally unique IDs.

   If a revised tree would move or remove files, strand tasks, or conflict with recorded evidence, show the affected paths and ask before changing them. A completed task omitted from a revised plan is not silently deleted; preserve it or get explicit removal confirmation.
3. **Map and write.** Build one source-ID → file/anchor mapping for the entire plan before writing. Root and ways own files; every executable leaf appears exactly once as a section in its parent's file. Link child ways and cross-way prerequisites using relative Markdown links. Preserve all source notes at their owning node. In update mode, merge new/changed nodes into the existing files and retain annotations/evidence that the source did not supersede; do not fabricate descriptions, signals, or done evidence. If an active task or supplied artifact has a workspace, create or preserve its `<ID>/` directory beside the owning group file and link it from the task section; do not create empty directories. Downstream skills may require canonical `spec/` or `design/` paths, so link those paths from the task workspace instead of silently changing their conventions.
4. **Record progress explicitly.** Preserve an existing `Status: in-progress` marker during updates. When work starts, record `Status: in-progress`; when the source supplies evidence that a task finished, write `Status: done` and retain the evidence beside that status. Keep not-started tasks `ready`, `waiting`, or `blocked`; do not infer completion because a dependent task is done. If a task is marked done without evidence, stop and request the evidence instead of writing a false completion.
5. **Check the recorded plan.** Compare every source node's Why/What/How, dependency, uncertainty, condition, completion signal, status, and completion evidence with its recorded location. Preserve ordered How steps and their evidence references; do not compress them into a generic action label. Verify links/anchors resolve, sibling order is preserved, paths do not collide, and the root execution overview still matches the task dependencies. No generic lifecycle nodes, unsupported parallel claims, lost annotations, or unproven `done` statuses may be introduced by serialization.
6. **Report.** Give the model-recommended operation (`created` or `updated`), output directory, root entry point, group-file count, and any remaining blockers. Summarize created/updated ways and the IDs recorded as done; do not dump every inline task as a file path.

No JSON, implementation, detailed design documents, new planning decisions, or downstream skill handoffs.

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
- Kind: <task | uncertainty | checkpoint>
- Why: <source purpose, parent outcome, and consequence of omitting this task>
- What: <source behavior/decision/artifact and scope boundaries>
- How: <source approach; preserve ordered steps as a nested list when present, including any named blocking decision>
- Needs: <linked prerequisite IDs and the result needed from each; or —>
- Status: <ready | in-progress | waiting | blocked | done, with source evidence where supplied>
- Workspace: <relative `<ID>/` directory for task artifacts, only when created or required>
- Evidence: <proof for a done status, such as a test result, commit, or user-confirmed completion; required only when done>
- Done when: <observable completion signal>
- Conditions/conflicts: <only if present in source>

<For an uncertainty, retain question, impact, resolving method/owner, exit signal, blocked IDs, and answer-dependent consequences. Reuse the Why/What/How fields for matching details rather than duplicating them.>
```

An intra-file prerequisite can link to `[B1](#B1)`; a cross-way prerequisite links to its owning file and anchor, e.g. `[A2](1-1-edit-the-buffer.md#A2)` from the sibling B file. Use explicit anchors matching source IDs rather than title-derived anchors.

The root additionally contains:

- **Grounding:** goal context, evidence, assumptions, and exclusions from the source.
- **Way tree:** the source hierarchy as a compact linked index, including inline leaf anchors.
- **Execution:** start-now tasks, dependency-driven unlocks, parallel lanes and their safety conditions, conflicts, convergence check, and next action. Link referenced IDs to their owning files/anchors. Preserve partial-plan warnings and owner questions.

Do not infer new prerequisites or parallel lanes from file numbers. If a needed field is missing rather than explicitly unknown/blocked, return to validation instead of inserting `Planned` or `None` as filler.

## Completion criterion

Every source node has exactly one canonical location; all planning meaning survives recording, every link resolves, and a reader can start at `0-goal.md` to find what can proceed, what must wait and why, how to resolve blockers, and what proves completion. New goals are created without collisions, existing goals are updated in place, task workspaces are created only when work or artifacts require them, annotations and in-progress/completed tasks are preserved, and every recorded `done` status has evidence. No redundant task files, lost dependency edges, invented work, or unapproved migration remains.
