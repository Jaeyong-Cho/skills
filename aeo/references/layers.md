# AEO Layers in Detail

## Origin

AEO is a software design philosophy inspired by OOP and AOP. A program is an automation tool for making decisions to achieve a goal. Designing it well requires two kinds of thinking:

1. **What algorithm makes the decision?** → Epistemology
2. **What data (objects) does the decision operate on?** → Ontology
3. **What is the goal worth automating?** → Axiology

This leads to two types of classes: **Ontological objects** (what exists) and **Aspect objects** (how things are viewed and used to achieve a goal). Axiology sits above both, determining which goals are worth pursuing.

---

## Ontology — Existence (What)

An Ontological object defines: properties, actions, behaviors, and relationships for a target in the problem domain.

**The key design question**: What distinguishes this object from others?

**The key design constraint**: Size must match the concern.

- If the concern is `DNA`, defining an `Atom` object is reasonable.
- If the concern is `Animal`, `Atom` is too small — define `Arm`, `Head`, `Body` instead.
- The object must not be too large (covering things outside the concern) or too small (forcing callers to reconstruct meaning).

**The invariance principle**: An Ontological object must remain the same regardless of which aspect is looking at it. If the object changes shape for a specific use case, it is no longer Ontological — it has leaked into Epistemology.

Ontological objects are the stable foundation. Multiple Epistemologies can use the same object from different angles without the object knowing or caring.

---

## Epistemology — Method / Aspect (How)

Epistemology describes how to interpret and use Ontological objects from a specific **aspect** to realize a goal. This is where AOP thinking enters: different aspects see the same objects differently, use only some of their properties, and combine them in different ways.

- An aspect does not need to use all Ontological objects.
- An aspect may use only some properties of an Ontological object, not the whole thing.
- The same Ontological object may be described very differently across aspects (this is normal and correct).

Epistemology answers: **given these objects, how do we combine, sequence, and interpret them to produce the desired outcome?**

Structure Epistemology into composable units — policies, strategies, workflows, pipelines — so that methods can be swapped without changing the entities or the value definition.

---

## Axiology — Value (Why)

Axiology defines what is worth automating. Features are not values themselves — they are means to realize values such as time saving, accuracy, convenience, and stability.

Four components:

| Component | Role |
|---|---|
| **Value Definition** | What matters and how much (weights, priorities) |
| **Value Evaluation** | Measures how good a result is |
| **Value Validation** | Enforces minimum acceptable thresholds |
| **Value Selection** | Picks the best option among candidates |

Axiology does not execute behavior. It governs which Epistemology gets chosen, how results are evaluated, and whether they are acceptable. Keep it explicit and encoded in logic — not buried in comments or implicit in control flow.

---

## How the Three Relate

```
Axiology  →  defines what is worth doing (why)
    ↓
Epistemology  →  defines how to do it, from which aspect (how)
    ↓
Ontology  →  defines what exists to operate on (what)
```

- Epistemology uses Ontology to realize Axiology.
- Axiology influences Epistemology through selection, evaluation, and validation.
- Ontology remains stable — it is not shaped by any single Epistemology or Axiology.

**Design order**: define value first → design methods second → define/refine entities last. In practice this is iterative, but the conceptual direction stays the same.

---

## Common Design Smells

| Smell | Likely cause |
|---|---|
| Selection logic duplicated across callers | Axiology not extracted |
| Entity changes shape for different callers | Ontology polluted by Epistemology |
| Algorithm hard-coded with magic thresholds | Axiology mixed into Epistemology |
| God object that evaluates, executes, and models | No layer separation |
| Object too large — covers multiple concerns | Abstraction level mismatched to concern |
| Object too small — callers must reconstruct meaning | Abstraction level too fine-grained |
| Value only in docs, not in code | Axiology implicit rather than encoded |
