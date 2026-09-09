---
name: to-way-graph
description: Create or update the authoritative English ways/ways.json graph from a confirmed Wayfinder plan, ask about an optional translated JSON companion, lint the outputs, and generate semantically equivalent English Markdown way documents.
disable-model-invocation: true
---

# To-Way Graph

Turn one confirmed Wayfinder plan into the canonical **English** graph at `ways/ways.json`, then generate the current navigable Markdown layout from that JSON. Always keep the canonical graph's authored prose in English, regardless of the plan's or conversation's language. Offer an additional translated JSON file, such as `ways/ways_ko.json` for Korean; it never replaces `ways.json`. Do not read existing Markdown as input and do not migrate it. The web viewer is separate.

## Workflow

1. Require a confirmed Wayfinder plan. If the plan is missing, ask for it; do not invent nodes, dependencies, evidence, or paths.
2. Unless the user already specified an additional language or explicitly declined one in this request, ask: **“I'll always write `ways.json` in English. Would you also like a translated JSON file? If so, which language? For Korean, I'll also write `ways_ko.json`.”** Wait for the answer; do not infer a translation preference from the language of the conversation. “Korean”, “한국어”, or “ko” selects Korean; “no” or “English only” selects no companion.
3. Read `ways/ways.json` if it exists. Merge updates by stable node ID. Preserve existing status, evidence, and annotations unless the confirmed plan explicitly supersedes them. New goals and nodes must have globally unique IDs. Never merge updates from a translated companion.
4. Write the complete graph to `ways/ways.json` with English authored prose. Translate any existing non-English prose without changing its meaning; preserve verbatim artifacts as described below. For every goal, way, and task, write `current_state` and `expected_result_state` as Markdown strings with a short explanation and at least one concrete, non-empty fenced code block in each field (see State examples below).
5. Run the linter from this skill directory:

   ```sh
   python3 scripts/lint_ways.py ways/ways.json
   ```

   Fix mechanical errors and rerun until it passes. For semantic conflicts—duplicate IDs, contradictory parentage, cycles, or unclear ownership—stop and ask for correction rather than guessing.
6. If the user requested another language, derive a complete translated graph from the just-written English graph using the Language output rules below. For Korean, write `ways/ways_ko.json` as UTF-8 with readable Hangul, then lint it too:

   ```sh
   python3 scripts/lint_ways.py ways/ways_ko.json
   ```

   Review the pair for identical structure, IDs, machine values, and factual meaning. Fix translation or validation errors before reporting success.
7. Only after the requested JSON outputs pass lint, generate Markdown **from the English canonical file only**:

   ```sh
   python3 scripts/transform_ways.py ways/ways.json
   ```

   The transformer also lints and refuses to write output when the graph is invalid.
8. Report the English JSON path, any translated JSON paths and their languages, generated goal directories, node/dependency counts, and any unresolved semantic blockers. If an existing companion was not refreshed because the user declined translation, leave it untouched and explicitly report that it may be stale.

## Language output rules

- `ways/ways.json` is always the authoritative English graph. A Korean request means **both** `ways/ways.json` and `ways/ways_ko.json`, not Korean prose inside `ways.json` and not a renamed replacement. For another requested language, use `ways_<language-code>.json`; clarify the language/code if ambiguous.
- Translate human-readable prose throughout the companion: titles, descriptions, purpose, state explanations, hypotheses, assumptions, success criteria, why/what/how, done criteria, and narrative annotations, including prose nested in lists or objects. Preserve the English graph's facts, uncertainty, expected-versus-observed distinctions, list order, and JSON value types. Do not invent work or infer completion while translating.
- Keep all JSON keys, node IDs, `version`, `goals`, optional `root_ids`, parent/children relationships, edges, positions, `type`, `task_kind`, and `status` identical. Preserve paths (`directory`, `file`, `workdir`, `target_repo`), URLs, link targets, anchors, technical identifiers, and machine-readable metadata. Do not create Korean paths or IDs by translating titles.
- Preserve evidence artifacts and verbatim quotations, commands, executable code, literal data, and recorded output in their original language in **both** files. Surrounding explanations are English in the canonical graph and Korean in the Korean companion. In illustrative state fences, translate only explanatory prose/diagram labels when safe; preserve code, identifiers, alignment, and fence syntax. Every translated state field must still contain a non-empty, closed fence.
- Derive translations anew from the latest canonical graph on each requested update. Never treat a companion as another independently editable source of truth. If an existing companion has independent edits, stop and ask how to reconcile them rather than overwriting those edits silently.
- Do **not** run `transform_ways.py` on a companion with its default output root: identical directory/file paths would overwrite the English Markdown. This workflow generates English Markdown only; translated Markdown is outside this request. The viewer can open `ways/ways_ko.json` directly.
- The linter validates schema and relationships, not language or translation fidelity. Check those during authoring; a passing lint is not proof of a correct translation.

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

Generate Markdown **only from `ways/ways.json` (English)**. Translated companions such as `ways/ways_ko.json` are JSON-only viewer inputs; do not use them to generate or overwrite Markdown.

The transformer writes one root file and one group file per way beneath each goal's `directory`, keeping tasks inline in their owning way file. It preserves the current `to-way` concepts: frontmatter, Outcome, Work, inline task fields, root Grounding, Way tree, Execution, context, explicit anchors, relative links, absolute task workspaces, and `IMPL` target repositories. Formatting may be normalized; information and relationships may not be lost. Keep state fences inside their labeled Markdown fields, preserving code line breaks and ASCII alignment; do not flatten them into inline code.

## Completion criterion

`ways/ways.json` has English authored prose and is valid under `scripts/lint_ways.py`; the user has chosen or declined an additional language; any requested companion (Korean: `ways/ways_ko.json`) also passes lint and preserves the canonical graph's structure, IDs, machine values, evidence, and meaning; every node's current and expected state includes a grounded or explicitly illustrative fenced example; every node appears exactly once with matching parent/children and explicit containment; every dependency points to existing nodes and has no cycle; stable IDs and completed evidence are preserved on updates; and `scripts/transform_ways.py` successfully generates the English Markdown documents from the canonical JSON without using existing Markdown as input.
