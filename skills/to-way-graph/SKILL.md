---
name: to-way-graph
description: Create or update the authoritative ways/ways.json graph from a confirmed Wayfinder plan, lint it, and generate semantically equivalent Markdown way documents.
disable-model-invocation: true
---

# To-Way Graph

Turn one confirmed Wayfinder plan into the canonical graph at `ways/ways.json`, then generate the current navigable Markdown layout from that JSON. Do not read existing Markdown as input and do not migrate it. The web viewer is separate.

## Workflow

1. Require a confirmed Wayfinder plan. If the plan is missing, ask for it; do not invent nodes, dependencies, evidence, or paths.
2. Read `ways/ways.json` if it exists. Merge updates by stable node ID. Preserve existing status, evidence, and annotations unless the confirmed plan explicitly supersedes them. New goals and nodes must have globally unique IDs.
3. Write the complete graph to `ways/ways.json`.
4. Run the linter from this skill directory:

   ```sh
   python3 scripts/lint_ways.py ways/ways.json
   ```

   Fix mechanical errors and rerun until it passes. For semantic conflicts—duplicate IDs, contradictory parentage, cycles, or unclear ownership—stop and ask for correction rather than guessing.
5. Only after lint passes, generate Markdown:

   ```sh
   python3 scripts/transform_ways.py ways/ways.json
   ```

   The transformer also lints and refuses to write output when the graph is invalid.
6. Report the JSON path, generated goal directories, node/dependency counts, and any unresolved semantic blockers.

## Canonical JSON model

The file is a single aggregate graph:

- `version`: `1`.
- `goals`: root way IDs.
- `nodes`: an object keyed by globally unique IDs.
- `edges.contains`: explicit containment edges, `from` parent to `to` child.
- `edges.depends_on`: explicit prerequisite edges, `from` dependent to `to` prerequisite.

Every node has `type` (`way` or `task`), `title`, `description`, `parent`, `children`, `purpose`, `current_state`, `expected_result_state`, `hypothesis`, and `assumptions`. Use `null` parent and an empty or populated `children` list as appropriate.

A way additionally has:

- `position`: presentation position (`0` for a root; child positions follow the source tree).
- `file`: Markdown path relative to its goal directory. Root ways use `0-goal.md`.
- Root ways also have `directory`: the relative numbered goal directory under `ways/`.
- `success`, plus optional `scope_status`, `grounding`, `execution`, `context_and_uncertainties`, and `frontmatter` fields.

A task additionally has:

- `task_kind`: exactly one of `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT`.
- `why`, `what`, `expected_result_state`, `how`, `status`, `workdir`, and `done_when`.
- `status`: `ready`, `in-progress`, `waiting`, `blocked`, or `done`.
- `target_repo`: an absolute path required only for `IMPL` tasks.
- Optional `evidence`, `conditions_conflicts`, and `uncertainty` fields.

`workdir` must be absolute and end with the task's stable ID. Preserve ordered `how` steps as a JSON list when order matters. A completed task must retain its evidence; never infer completion from a green command or commit alone.

Containment is duplicated deliberately: `children`, `parent`, and `edges.contains` must agree. This lets the web viewer traverse the tree without reconstructing it. Dependencies are separate from containment and must be acyclic.

## Markdown output

The transformer writes one root file and one group file per way beneath each goal's `directory`, keeping tasks inline in their owning way file. It preserves the current `to-way` concepts: frontmatter, Outcome, Work, inline task fields, root Grounding, Way tree, Execution, context, explicit anchors, relative links, absolute task workspaces, and `IMPL` target repositories. Formatting may be normalized; information and relationships may not be lost.

## Completion criterion

`ways/ways.json` is valid under `scripts/lint_ways.py`; every node appears exactly once with matching parent/children and explicit containment; every dependency points to existing nodes and has no cycle; stable IDs and completed evidence are preserved on updates; and `scripts/transform_ways.py` successfully generates the Markdown documents from JSON without using existing Markdown as input.
