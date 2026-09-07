---
name: wayfinder
description: Use a concise grill-me interview to understand intent, then map every validation-first route from a goal to actionable tasks and experiments. Invoke as /wayfinder.
disable-model-invocation: true
---

# Wayfinder

Understand the user's intent, then map every materially different route from one goal to its smallest actionable tasks or experiments. Return a concise, validation-first graph without designing or implementing production work.

## Why this exists

A flat list hides dependencies and conditional routes. Wayfinder makes the goal, decomposition checkpoints, experiments, and branch conditions explicit so a later tool can render and traverse the graph.

## MANDATORY Grill-Me Usage

Always invoke `@skills/grill-me` before producing any output. Start by understanding the user's intent, desired outcome, and success signal; keep the interview concise and ask only questions that can change the route, branch condition, dependency, or validation.

Pass the interviewer:

- the user's intent
- the goal and starting context
- constraints relevant to reaching the goal
- any known uncertainty or decision that may create branches

Do not ask about unrelated project context or implementation details. If intent, goal, or a blocking constraint is missing, ask only for that missing input through `@skills/grill-me`.

If `@skills/grill-me` cannot be invoked, stop and report the blocker. Do not produce a route from assumptions.

## Wayfinding Principles

Prefer ways that provide:

- fast feedback
- a small and reversible experiment
- cheap exploration of the key uncertainty
- clear tests or observable signals
- a short feedback loop
- a clear transition into production requirements, design, and implementation

Use prototypes, spikes, thin vertical slices, test doubles, simulations, exploratory scripts, user interviews, measurements, or other low-cost validation methods when appropriate.

Do not choose the cheapest experiment when safety, compliance, data integrity, or irreversible production impact requires stronger validation.

## Decomposition Rules

- Handle one goal per invocation.
- Make the goal the root node. Its immediate children are high-level ways; recursively decompose each way into smaller branches and low-level actionable tasks.
- Keep the hierarchy ordered from the goal through high-level checkpoints to detailed leaves. Continue until a node is the smallest executable task or experiment with a clear validation signal.
- Include every materially different route; do not rank, select, merge, or invent artificial alternatives.
- Represent a decision or checkpoint as a node and its outcomes or dependencies as directed edges.
- Put branch conditions on edges. If uncertainty needs evidence, add an actionable `experiment` or `exploration` node instead of guessing.
- Give every node and edge a stable unique ID. Use hierarchy edges for decomposition and dependency edges for prerequisites; shared dependencies may connect branches.

## Skill Handoff

For every actionable leaf, recommend one existing skill that can execute or validate it. Use the available skill catalog and never invent a skill name. Choose the skill that fits the leaf's abstraction level and give a short reason.

A node is actionable only when it names a concrete next move and an observable result. If a leaf is not actionable, recommend `/wayfinder` instead of a downstream skill.

## Output Format

Return one concise graph result in this order:

```markdown
## Intent
[The user's intended outcome and success signal]

## Goal
- ID: [goal-node-id]
- Title: [goal]

## Route summary
[Briefly explain how the branches descend from the goal and where their conditions or experiments lead.]

## Nodes
### [node-id] — [title]
- Kind: [goal | checkpoint | task | experiment | exploration]
- Description: [one concise grill-me-style explanation containing why it matters, relevant grounding or uncertainty, and a concrete example; for an actionable leaf, include the action, validation signal, and skill handoff]

[Repeat for every node.]

## Edges
### [edge-id] — [from-id] → [to-id]
- Type: [decomposes | depends_on]
- Description: [what relationship this edge expresses]
- Condition: [branch condition, or `None`]

[Repeat for every edge.]
```

Include every branch and actionable leaf, in top-down order from the goal to the detailed low-level tasks. Keep `experiment` and `exploration` nodes actionable by naming the smallest test and its supporting or rejecting signal. Recommend one existing skill for each actionable leaf; recommend `/wayfinder` only when the leaf is not yet actionable. The result must be complete enough for `@skills/to-way` to write one Markdown group for every node, with the same node and edge IDs.
