# AEO Layers in Detail

## Origin

AEO is a software design philosophy inspired by OOP and AOP. A program is an automation tool for making decisions to achieve a goal. Designing it well requires two kinds of thinking:

1. **What algorithm makes the decision?** → Epistemology
2. **What data (objects) does the decision operate on?** → Ontology
3. **What is the goal worth automating?** → Axiology

This leads to two types of classes: **Ontological objects** (what exists) and **Aspect objects** (how things are viewed and used to achieve a goal). Axiology sits above both, determining which goals are worth pursuing.

---

## Ontology — Existence (What)

Ontological objects are the things that must exist to satisfy both the Axiological need and the Epistemological method. They are not an arbitrary catalog of domain entities — they are the objects that Epistemology selects and uses, shaped to serve the concerns that Axiology defines.

An Ontological object defines: properties, actions, behaviors, and relationships for a target in the problem domain.

**The key design question**: What distinguishes this object from others, and is it the right abstraction for the concern being served?

**The key design constraint**: Size must match the concern.

- If the concern is `DNA`, defining an `Atom` object is reasonable.
- If the concern is `Animal`, `Atom` is too small — define `Arm`, `Head`, `Body` instead.
- The object must not be too large (covering things outside the concern) or too small (forcing callers to reconstruct meaning).

**The invariance principle**: An Ontological object must remain the same regardless of which aspect is looking at it. If the object changes shape for a specific use case, it has leaked into Epistemology.

Ontological objects are the stable foundation. Multiple Epistemologies can use the same object from different angles without the object knowing or caring.

---

## Epistemology — Method / Aspect (How)

Epistemology has two responsibilities:

1. **How to meet the need** — the algorithm, workflow, or strategy that realizes the Axiological goal
2. **Which objects to use and how to see them** — from what angle are the Ontological objects viewed? What subset of their properties matters here?

This is where AOP thinking enters: different aspects see the same object differently, use only some of its properties, and combine objects in different ways. Epistemology decides which Ontological objects are needed and how to compose them to produce the desired outcome.

- An aspect does not need to use all Ontological objects.
- An aspect may use only some properties of an object, not the whole thing.
- The same object may look very different across aspects — this is correct, not a problem.

Structure Epistemology into composable units — strategies, workflows, pipelines — so that methods can be swapped without changing the entities or the value definition.

---

## Axiology — User Value (Why)

Axiology is the layer that encodes **what the end user needs** from this software. It answers: which features are worth building? Which results do users actually need? What does a good outcome look like from their perspective?

This is the purpose layer — it exists to represent the user's goals, not the system's internals. In code it is the entry point: the use-case, command, or application service that says "the user needs X." Everything below it (Epistemology, Ontology) exists to serve what Axiology defines.

Axiology encodes:
- Which user needs are worth satisfying (feature selection)
- What a successful result looks like (evaluation)
- What must never happen (validation)
- Which method (Epistemology) should deliver the result

Because Axiology represents user intent, it delegates the *how* to Epistemology. Keep it explicit in logic — if the user's need only lives in a comment or a ticket, it has not been encoded in Axiology yet.

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
