# Concrete current and expected states

These are **fictional authoring examples**, not observations or evidence. In real graphs, use the confirmed plan and inspected artifacts. Each section below is the Markdown string stored in the named JSON field; both fields need their own fenced block.

## Goal or way: show the topology

### `current_state`

Illustrative baseline: the file can be read, but no navigation connects the graph to its details.

```text
ways.json -> JSON text
             |
             +-> manually find node IDs
             +-> manually follow prerequisites
```

### `expected_result_state`

Expected reading experience: selecting a way reveals its work without losing access to the goal.

```text
ways.json -> local server -> React viewer
                            +-- full graph
                            +-- selected way -> task dependencies
                            +-- selected node -> Markdown details
```

## Implementation task: show a code-level change

### `current_state`

Illustrative baseline: parsing accepts a document without checking graph relationships.

```javascript
const graph = JSON.parse(await readFile(file, 'utf8'));
return graph; // Dangling prerequisites are not checked.
```

### `expected_result_state`

Expected implementation: a parsed graph reaches the reader only after validation. Invalid relationships produce an explicit error.

```javascript
const graph = JSON.parse(await readFile(file, 'utf8'));
validateGraph(graph); // Throws for missing nodes or cycles.
return graph;
```

## Checkout task: show commands and observable output

### `current_state`

Illustrative baseline, not a real command run: the API returns unvalidated input.

```console
$ curl -i http://127.0.0.1:4317/api/graph
HTTP/1.1 200 OK
{"graph":{"version":99}}
```

### `expected_result_state`

Expected transcript when the input has an unsupported version. This is an acceptance example, not a passing test record.

```console
$ curl -i http://127.0.0.1:4317/api/graph
HTTP/1.1 422 Unprocessable Entity
{"error":"Cannot load graph: Graph version must be 1"}
```

## Explore task: keep an unknown baseline honest

### `current_state`

The confirmed plan does not establish whether the sidebar can render fenced blocks. No browser inspection has been recorded.

```text
Markdown input:          fenced code + ASCII diagram
Code block rendering:   unknown
Whitespace preservation: unknown
Evidence:               not collected
```

### `expected_result_state`

Expected inspection record: record an actual observation for each case, including a screenshot or reproducible failure. Passing is not assumed.

```text
Case          Observation to record       Evidence to attach
Code block    rendered / not rendered     screenshot or failure
ASCII diagram aligned / misaligned       screenshot or failure
```

## JSON encoding

Use Markdown strings, not an object with separate `text` and `example` fields. A minimal illustrative pair looks like this (a fragment, not a complete graph):

```json
{
  "current_state": "Illustrative baseline: no nodes are selected.\n\n```json\n{\"selectedId\": null}\n```",
  "expected_result_state": "Expected state after selecting task T1.\n\n```json\n{\"selectedId\": \"T1\"}\n```"
}
```

The linter checks non-empty, closed fences in both fields, including backtick or tilde fences. It cannot establish that examples are truthful or useful: that remains an authoring requirement. Examples do not replace `evidence`, `done_when`, or an explicit status update.
