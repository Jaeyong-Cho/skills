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
3. Write the complete graph to `ways/ways.json`. For every goal, way, and task, write `current_state` and `expected_result_state` as Markdown strings with a short explanation and at least one concrete, non-empty fenced code block in each field (see State examples below).
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

## State examples (required)

Both `current_state` and `expected_result_state` **must include a non-empty, closed fenced code block**. Prose alone, inline code, or an empty fence is not sufficient. This applies to root goals, child ways, and tasks of every kind.

- Start with a short explanation, then show the state concretely: code, an ASCII diagram, commands and their output, a file tree, a request/response, or representative data. Choose the format that makes the difference observable; do not force source code onto non-coding work.
- Use an appropriate fence language, such as `text` for diagrams, `bash` for commands, `console` for transcripts, or `json`/`python`/`javascript` for data or code. Preserve line breaks and diagram alignment inside the JSON string using `\n` escapes.
- `current_state` describes what is known now, not a to-do list. Ground examples in the confirmed plan or observed artifacts. If the baseline is unknown, state that explicitly and show the unknowns in a `text` block; a proposed inspection command is not observed output.
- `expected_result_state` shows the target state after the work: the intended structure, changed code, response, or observable output. Label predicted output as **expected**, never as an actual execution result or completion evidence.
- Make the before/after pair comparable and specific to the node. A command alone does not show a state: include the relevant existing/expected output or describe the artifact it produces. Avoid generic examples such as `before -> after`, `works`, or repeated boilerplate across unrelated nodes.
- Preserve authored statuses and evidence. Examples illustrate states; they do not prove execution or authorize marking a task done. Fictional demonstration data must be labeled as fictional.

See [state examples](examples/state-examples.md) for diagrams, code, command transcripts, and an explicit unknown baseline. The linter enforces the structural requirement; the author must check relevance and factual grounding. Existing graphs with prose-only state fields need grounded examples before they can pass lint or be transformed; do not invent observations to silence an error.

## Markdown output

The transformer writes one root file and one group file per way beneath each goal's `directory`, keeping tasks inline in their owning way file. It preserves the current `to-way` concepts: frontmatter, Outcome, Work, inline task fields, root Grounding, Way tree, Execution, context, explicit anchors, relative links, absolute task workspaces, and `IMPL` target repositories. Formatting may be normalized; information and relationships may not be lost. Keep state fences inside their labeled Markdown fields, preserving code line breaks and ASCII alignment; do not flatten them into inline code.

## Completion criterion

`ways/ways.json` is valid under `scripts/lint_ways.py`; every node's current and expected state includes a grounded or explicitly illustrative fenced example; every node appears exactly once with matching parent/children and explicit containment; every dependency points to existing nodes and has no cycle; stable IDs and completed evidence are preserved on updates; and `scripts/transform_ways.py` successfully generates the Markdown documents from JSON without using existing Markdown as input.
