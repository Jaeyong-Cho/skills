# AEO Layers in Detail

## Axiology — Value (Why)

Axiology does not execute behavior. It governs which behavior gets chosen and whether results are acceptable.

Four components:

| Component | Role |
|---|---|
| **Value Definition** | What matters and how much (weights, priorities) |
| **Value Evaluation** | Measures how good a result is |
| **Value Validation** | Enforces minimum acceptable thresholds |
| **Value Selection** | Picks the best option among candidates |

Design signal: if code is choosing between options, scoring outputs, or enforcing thresholds — that's Axiology. Keep it explicit and encoded in logic, not buried in comments or implicit in control flow.

## Epistemology — Method (How)

Epistemology executes behavior using Ontological objects to realize Axiological goals.

- Algorithms, decision trees, workflows, interaction patterns
- Composable and replaceable units (strategies, policies, pipelines)
- Does not define what is valuable — it receives that from Axiology
- Does not define what exists — it uses what Ontology provides

Design signal: if code describes *how* to do something step-by-step, it belongs here. Structure it so the method can be swapped without changing the value or entity layer.

## Ontology — Existence (What)

Ontology defines stable entities: their properties, behaviors, and relationships.

Key principle: an Ontological object stays the same across different perspectives. If an entity changes shape depending on *who* is using it, it's leaking Epistemology or Axiology into Ontology.

Design signal: domain models, core data structures, entity types. They should be usable by multiple Epistemologies without modification.

## Common Design Smells

| Smell | Likely cause |
|---|---|
| Selection logic duplicated across callers | Axiology not extracted |
| Entity has different shapes for different callers | Ontology polluted by Epistemology |
| Algorithm hard-coded with magic thresholds | Axiology mixed into Epistemology |
| "God object" that evaluates, executes, and models | No layer separation at all |
| Value only in docs, not in code | Axiology implicit rather than encoded |
