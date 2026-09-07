---
name: to-way
description: Record a Wayfinder task plan as navigable Markdown work packages, preserving uncertainties, prerequisites, and parallel execution guidance. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Record one Wayfinder plan without redesigning or executing it. Preserve its goal, grounding, tree, each task's Why/What/How, uncertainty details, dependencies, conditions, completion signals, and execution guidance. A tree alone is insufficient if the information needed to execute its leaves is missing.

## Layout: files for ways, tasks inline

- Write `0-goal.md` for the root and one group file per **way** (work package).
- Keep task, uncertainty, and checkpoint leaves inside their immediate parent's file, with an explicit anchor for each source ID. Do not create one-line task files or lifecycle-stage directories.
- A child way at depth `D`, sibling position `N`, uses `{D}-{N}-{slug}.md`. Count positions in the original tree, including inline leaves; gaps in file numbering are valid.
- Child way files live in a directory matching the parent's numeric path key (`0-goal`, `1-2`, etc.), not its logical source ID (`G`, `B`, etc.). Preserve the full ancestry to avoid collisions.
- Numbers preserve presentation order, **not** prerequisites or mandatory serial execution. Dependencies determine readiness and parallelism.
- Preserve source IDs in content; do not replace them with filename numbers.

For the illustrative modal-editing plan in Wayfinder:

```text
ways/01-add-modal-insertion-and-saving/
├── 0-goal.md                         # G, execution overview, inline checkpoint C
└── 0-goal/
    ├── 1-1-edit-the-buffer.md        # A, inline tasks A1 and A2
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
   - readiness and parallel guidance do not contradict prerequisites or recorded resource conflicts.

   Explicitly partial branches blocked by named uncertainties are valid; retain their limits. Missing planning information is not permission to invent it. For a legacy requirements/design/implement/test tree or other invalid source, explain the missing decisions and ask for a revised Wayfinder plan. Do not silently upgrade it or serialize empty placeholders.
2. **Confirm the destination.** Reuse a destination confirmed in this session; otherwise ask one standalone question, recommending `./ways/`:

   ❓ **Q1** - **Destination**: Where should this plan be recorded?

   ➡️ `./ways/` in the current directory, under a numbered goal directory.

   Once confirmed, use `ways/{nn}-{slug}/`; update an existing same-goal directory rather than creating a duplicate. Inspect existing files first. Preserve user annotations and completed-work evidence; if a revised tree conflicts with them, ask rather than overwrite. If migration/reordering would remove or strand old group or task files, show the affected paths and get confirmation before removing or moving them. Do not leave contradictory old files mixed into a reported-complete plan.
3. **Map and write.** Build one source-ID → file/anchor mapping for the entire plan before writing. Root and ways own files; every executable leaf appears exactly once as a section in its parent's file. Link child ways and cross-way prerequisites using relative Markdown links. Preserve all source notes at their owning node; do not fabricate descriptions or signals to fill the format.
4. **Check the recorded plan.** Compare every source node's Why/What/How, dependency, uncertainty, condition, and completion signal with its recorded location. Preserve ordered How steps and their evidence references; do not compress them into a generic action label. Verify links/anchors resolve, sibling order is preserved, paths do not collide, and the root execution overview still matches the task dependencies. No generic lifecycle nodes or unsupported parallel claims may be introduced by serialization.
5. **Report.** Give the output directory, root entry point, group-file count, and any remaining blockers. The linked root is the navigation index; do not dump every inline task as a file path.

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
- Status: <ready | waiting | blocked | done, with source evidence where supplied>
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

Every source node has exactly one canonical location; all planning meaning survives recording, every link resolves, and a reader can start at `0-goal.md` to find what can proceed, what must wait and why, how to resolve blockers, and what proves completion. No redundant task files, lost dependency edges, invented work, or unapproved migration remains.
