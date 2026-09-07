---
name: to-way
description: Record a complete Wayfinder route graph, including intent, nodes, edges, conditions, validation, and skill handoffs, in Markdown and JSON. Invoke as /to-way.
disable-model-invocation: true
---

# To-Way

Turn one complete Wayfinder result into a concise, reusable route graph containing the user's intent, goal, every branch, each checkpoint, and all actionable tasks or experiments. Write the same graph in human-readable Markdown and machine-readable JSON; do not design or implement the solution.

## Why this exists

A flat Wayfinder result hides the route structure. `to-way` preserves node IDs, directed edges, dependencies, conditions, validation signals, and skill handoffs so a later script can render and traverse every path.

## Workflow

1. **Gather the route graph.** Use the complete Wayfinder result from this session or from a supplied source. Record the user's intent, goal, relevant constraints, every node, every edge, all branch conditions, validation signals, and skill handoffs. Record each node with one concise description. Completion criterion: every node and edge in the source is included with its original ID.
2. **Keep the graph boundary.** Do not select, rank, discard, merge, or invent branches; rerun the decision; add deeper work; or turn the record into a design or implementation plan. If no Wayfinder result is available, tell the user to run `/wayfinder` first. If graph data is incomplete, do not fill it from assumptions. Preserve `/wayfinder` as the recommendation for any node that is not actionable.
3. **Explain each node and route.** Give every node one concise description. Write it in a grill-me style: explain why it matters, include relevant grounding or uncertainty, and give a concrete example. For every actionable leaf, include the action, validation signal, and skill handoff in that same description. Do not add separate node fields or justify a node with unrelated future benefits.
4. **Follow document style.** Read `../references/document-style.md` and `../references/document-style/understanding-and-structure.md`. Keep the conclusion before supporting details and use short, concrete language.
5. **Confirm the location.** If this session has not already confirmed a destination, ask one `❓`/`➡️` question using `../references/question-format.md`. Recommend `./ways/` in the current directory. Once confirmed, create `./ways/{nn}-{slug}/`, write its aggregate graph to `graph.json`, and write one `<node-id>.md` file per node; update an existing same-goal directory instead of creating a duplicate.
6. **Validate and write the graph** with this structure:

   - Confirm node IDs and edge IDs are unique.
   - Confirm every edge endpoint refers to an existing node.
   - Confirm the goal is the root, its children are high-level ways, and each branch descends to detailed low-level tasks.
   - Confirm every terminal node is actionable or an explicitly deferred blocker.
   - Confirm the aggregate JSON and every node Markdown file contain the same node description and attached-edge data, in goal-to-leaf order.

   Each node Markdown file, written to `./ways/{nn}-{slug}/{node-id}.md`:

   ```markdown
   ---
   type: Way Node
   title: <node title>
   description: <one-line explanation of this node>
   tags: [wayfinder, validation, graph]
   timestamp: <ISO 8601 datetime>
   ---

   # <node title>

   ## Node
   - ID: <node-id>
   - Kind: <goal | checkpoint | task | experiment | exploration>
   - Description: <the same concise description from the section above>

   ## Edges
   ### <edge-id> — <from-id> → <to-id>
   - Type: <decomposes | depends_on>
   - Description: <what relationship this edge expresses>
   - Condition: <branch condition, or `None`>

   <Repeat for every edge attached to this node.>
   ```

   Aggregate JSON, written to `./ways/{nn}-{slug}/graph.json`:

   ```json
   {
     "intent": "...",
     "goalId": "goal-1",
     "nodes": [
       {
         "id": "goal-1",
         "kind": "goal",
         "title": "...",
         "description": "..."
       }
     ],
     "edges": [
       {
         "id": "edge-1",
         "from": "goal-1",
         "to": "task-1",
         "type": "decomposes",
         "description": "...",
         "condition": "..."
       }
     ],
     "deferred": []
   }
   ```

   Omit empty optional fields consistently. Preserve node order from the goal through high-level ways to detailed low-level leaves. Completion criterion: the aggregate JSON and every node Markdown file include the complete graph, preserve every source ID, description, and condition, and can be used independently by a human or graph-rendering script.

Tell the user both file paths when done.
