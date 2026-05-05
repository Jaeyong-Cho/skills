---
name: aeo
description: |
  Apply the AEO (Axiology–Epistemology–Ontology) software architecture philosophy to any engineering task.
  AEO is a three-layer design lens: Axiology defines value (why), Epistemology defines method (how), Ontology defines stable entities (what).
  Use this skill whenever the user says "aeo", "apply aeo", "use aeo philosophy", or asks for design, review, coding, refactoring, or documentation *with AEO in mind*.
  Also trigger when the user asks to analyze or critique an architecture and the AEO framework would help clarify responsibilities and boundaries.
  Even if the user just says "review this" or "design this" in a context where AEO has been mentioned or is the active working philosophy, apply this skill.
---

# AEO Skill

Apply the **Axiology → Epistemology → Ontology** philosophy to software tasks. The three layers answer:

- **Axiology (Value / Why)** — what outcomes matter and how to evaluate them
- **Epistemology (Method / How)** — how to achieve those outcomes: algorithms, workflows, decisions
- **Ontology (Existence / What)** — what stable entities must exist for the system to function

Design direction: Axiology first → Epistemology second → Ontology last (but iteration is expected).

---

## The Three Layers in Detail

### Axiology — Value
Axiology does not execute behavior. It governs which behavior gets chosen and whether results are acceptable.

Four components:
| Component | Role |
|---|---|
| **Value Definition** | What matters and how much (weights, priorities) |
| **Value Evaluation** | Measures how good a result is |
| **Value Validation** | Enforces minimum acceptable thresholds |
| **Value Selection** | Picks the best option among candidates |

Design signal: if code is choosing between options, scoring outputs, or enforcing thresholds — that's Axiology. Keep it explicit and encoded in logic, not buried in comments or implicit in control flow.

### Epistemology — Method
Epistemology executes behavior using Ontological objects to realize Axiological goals.

Characteristics:
- Algorithms, decision trees, workflows, interaction patterns
- Composable and replaceable units (strategies, policies, pipelines)
- Does not define what is valuable — it receives that from Axiology
- Does not define what exists — it uses what Ontology provides

Design signal: if code describes *how* to do something step-by-step, it belongs here. Structure it so the method can be swapped without changing the value layer or the entity layer.

### Ontology — Existence
Ontology defines stable entities: their properties, behaviors, and relationships.

Key principle: an Ontological object stays the same across different perspectives. If an entity changes shape depending on *who* is using it, it's leaking Epistemology or Axiology into Ontology — a design smell.

Design signal: domain models, core data structures, entity types. They should be usable by multiple Epistemologies without modification.

---

## Modes of Operation

Adapt your output based on what the user asks. Common modes:

### Design / Architecture
1. **Axiology first** — identify the values: what outcomes matter? what does success look like? what must never happen?
2. **Epistemology second** — design the methods: what algorithms, workflows, or decision processes realize those values?
3. **Ontology last** — identify the stable entities the methods will operate on.
4. Present each layer clearly. Call out any leakage between layers (e.g., Ontology shaped by a single use case).

### Code Review
For each piece of code, identify which layer it belongs to and flag violations:
- Axiology mixed into Epistemology (e.g., scoring logic tangled with execution logic)
- Ontology shaped by a specific Epistemology (entity changes shape for one caller)
- Missing Axiology (selection/evaluation done implicitly, not explicitly)
- Monolithic code where all three layers are entangled

Structure feedback as: **[Layer] Issue → Why it matters → Suggested fix**

### Coding / Implementation
When writing code, label your design decisions by layer:
- Separate value logic (Axiology) from execution logic (Epistemology) from entity definitions (Ontology)
- Axiology components: value definitions, scorers, validators, selectors — keep these in dedicated modules/classes
- Epistemology components: algorithms, pipelines, strategies — make them swappable
- Ontology components: domain models — keep them stable and free of method-specific assumptions

### Refactoring
Identify layer violations in existing code, then propose targeted separations:
1. Extract Axiology (value, scoring, thresholds, selection) into explicit components
2. Extract Epistemology (algorithms, workflows) into composable units
3. Stabilize Ontology by removing method-specific fields or behaviors from entities

### Documentation
Structure documentation around the three layers:
- **Why** section: values, goals, success criteria (Axiology)
- **How** section: methods, workflows, decision logic (Epistemology)
- **What** section: entities, their properties and relationships (Ontology)

---

## Common Design Smells

| Smell | Likely cause |
|---|---|
| Selection logic duplicated across callers | Axiology not extracted |
| Entity has different shapes for different callers | Ontology polluted by Epistemology |
| Algorithm hard-coded with magic thresholds | Axiology mixed into Epistemology |
| "God object" that evaluates, executes, and models | No layer separation at all |
| Value only in docs, not in code | Axiology implicit rather than encoded |

---

## Output Principles

- Always name which layer you're discussing
- When identifying violations, explain *why* it's a problem (not just which rule it breaks)
- Be concrete: show the code change or the structure, not just the concept
- Adapt verbosity to the task: a quick review note doesn't need full layer breakdowns; a full architecture session does
- If layers are cleanly separated already, say so — don't invent problems
