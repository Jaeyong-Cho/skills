---
name: to-way
description: Record a complete Wayfinder route graph as grouped Markdown files, including intent, nodes, edges, conditions, validation, and skill handoffs. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Turn one complete Wayfinder result into a concise, reusable route graph containing the user's intent, goal, every branch, each checkpoint, and all actionable tasks or experiments. Write one human-readable Markdown file for each node group; do not generate JSON, design, or implement the solution.

## Why this exists

A flat Wayfinder result hides the route structure. `to-way` preserves node IDs, directed edges, dependencies, conditions, validation signals, and skill handoffs so a later script can render and traverse every path.

## Example output

For the goal `Release the feature safely`, `to-way` writes one Markdown file for each node group:

```text
ways/01-release-feature/
├── goal-1.md       # goal-1 and its direct sub-goals
├── way-a.md        # way-a and its direct sub-goals
├── experiment-a.md # actionable leaf group
├── way-b.md        # way-b and its direct sub-goals
└── task-b.md       # actionable leaf group
```

`goal-1.md`:

```markdown
# Group: Release the feature safely

## Goal node
- ID: goal-1
- Kind: goal
- Description: Choose a safe release route. Example: use an experiment when the release risk is unknown.

## Sub-goals
### way-a — Validate release risk
- Kind: checkpoint
- Description: Check unknown risk before release.

### way-b — Use the verified route
- Kind: checkpoint
- Description: Follow existing release evidence.

## Edges
### edge-1 — goal-1 → way-a
- Type: decomposes
- Description: The goal can begin with risk validation.
- Condition: Use when release risk is unknown.

### edge-2 — goal-1 → way-b
- Type: decomposes
- Description: The goal can use an existing verified route.
- Condition: Use when release evidence already exists.
```

Each sub-goal gets its own group file with its direct sub-goals and edges. Leaf groups contain only their actionable node description and attached edges.

## Workflow

1. **Gather the route graph.** Use the complete Wayfinder result from this session or from a supplied source. Record the user's intent, goal, relevant constraints, every node, every edge, all branch conditions, validation signals, and skill handoffs. Record each node with one concise description. Completion criterion: every node and edge in the source is included with its original ID.
2. **Keep the graph boundary.** Do not select, rank, discard, merge, or invent branches; rerun the decision; add deeper work; or turn the record into a design or implementation plan. If no Wayfinder result is available, tell the user to run `/wayfinder` first. If graph data is incomplete, do not fill it from assumptions. Preserve `/wayfinder` as the recommendation for any node that is not actionable.
3. **Explain each node and route.** Give every node one concise description. Write it in a grill-me style: explain why it matters, include relevant grounding or uncertainty, and give a concrete example. For every actionable leaf, include the action, validation signal, and skill handoff in that same description. Do not add separate node fields or justify a node with unrelated future benefits.
4. **Follow document style.** Read `../references/document-style.md` and `../references/document-style/understanding-and-structure.md`. Keep the conclusion before supporting details and use short, concrete language.
5. **Confirm the location.** If this session has not already confirmed a destination, ask one `❓`/`➡️` question using `../references/question-format.md`. Recommend `./ways/` in the current directory. Once confirmed, create `./ways/{nn}-{slug}/` and write one `<node-id>.md` group file per node; update an existing same-goal directory instead of creating a duplicate.
6. **Validate and write the graph** with this structure:

   - Confirm node IDs and edge IDs are unique.
   - Confirm every edge endpoint refers to an existing node.
   - Confirm the goal is the root, its children are high-level ways, and each branch descends to detailed low-level tasks.
   - Confirm every terminal node is actionable or an explicitly deferred blocker.
   - Confirm every node has exactly one group file containing its description and direct subnodes.
   - Confirm every decomposition edge is written in its parent group, and every dependency edge is written with its source node.
   - Confirm every source node and edge appears in the grouped Markdown files, in goal-to-leaf order.

   Each group Markdown file, written to `./ways/{nn}-{slug}/{node-id}.md`:

   ```markdown
   ---
   type: Way Group
   title: <group goal title>
   description: <one-line explanation of this group>
   tags: [wayfinder, validation, graph]
   timestamp: <ISO 8601 datetime>
   ---

   # Group: <group goal title>

   ## Goal node
   - ID: <node-id>
   - Kind: <goal | checkpoint | task | experiment | exploration>
   - Description: <one concise grill-me-style description, including a concrete example when useful>

   ## Sub-goals
   ### <child-node-id> — <child title>
   - Kind: <goal | checkpoint | task | experiment | exploration>
   - Description: <one concise description>

   <Repeat for every direct sub-goal of this group.>

   ## Edges
   ### <edge-id> — <from-id> → <to-id>
   - Type: <decomposes | depends_on>
   - Description: <what relationship this edge expresses>
   - Condition: <branch condition, or `None`>

   <Repeat for every edge owned by this group.>

   ## Child groups
   - `<child-node-id>.md`

   <Repeat for every child group file.>
   ```

   Write one group file for every node, including leaf groups. A decomposition edge belongs to its parent group. A dependency edge belongs to the group of its source node. Child nodes are summarized in their parent group and fully described in their own group file. Completion criterion: grouped Markdown files preserve every source node, description, edge, and condition in goal-to-leaf order and can be used independently by a human or graph-rendering script.

Tell the user the output directory and every group file path when done.
