# AEO Layers in Detail

## Origin

AEO is a software design philosophy inspired by OOP and AOP. A program is an automation tool for making decisions to achieve a goal. Designing it well requires three kinds of thinking:

1. **What is the user goal worth automating?** → value layer
2. **What algorithm and objects realize that goal?** → aspect layer
3. **What stable objects does the system operate on?** → object layer

This leads to two types of classes: **domain objects** (what exists) and **aspect objects** (how things are viewed and used to achieve a goal). The value layer sits above both, determining which user goals are worth pursuing.

---

## Ontology (Object layer) — Existence (What)

Domain objects are the things that must exist to satisfy both the user need and the aspect. They are not an arbitrary catalog of domain things — they are the objects that the aspect selects and uses, shaped to serve the concerns that the value layer defines.

A domain object is not just a data container. It defines the full identity of a domain target:

- **Properties** — the state it holds
- **Actions** — what it can do (methods, commands, transitions)
- **Behaviors** — how it responds to events or conditions
- **Relationships** — how it connects to other objects

A class that only holds data with no actions or behaviors is a data bag, not a domain object. If the logic that belongs to an object is scattered across service or aspect-layer classes instead, that is a leakage smell — the object is too thin.

**The key design question**: What distinguishes this object from others, and is it the right abstraction for the concern being served?

**The key design constraint**: Size must match the concern.

- If the concern is `DNA`, defining an `Atom` object is reasonable.
- If the concern is `Animal`, `Atom` is too small — define `Arm`, `Head`, `Body` instead.
- The object must not be too large (covering things outside the concern) or too small (forcing callers to reconstruct meaning).

**The invariance principle**: A domain object must remain the same regardless of which aspect is looking at it. If the object changes shape for a specific use case, it has leaked into the aspect layer.

Domain objects are the stable foundation. Multiple aspect-layer components can use the same object from different angles without the object knowing or caring.

### Relationships

For each relationship, decide: cardinality, ownership (who controls the lifecycle), navigability (which direction), and aggregate boundary (what changes atomically together). View-specific joins belong in the aspect layer, not the object.

---

## Epistemology (Aspect layer) — Algorithm / Aspect (How)

The aspect layer has two responsibilities:

1. **How to meet the need** — the algorithm, workflow, or strategy that realizes the user goal
2. **Which objects to use and how to see them** — from what angle are the domain objects viewed? What subset of their properties matters here?

This is where AOP thinking enters: different aspects see the same object differently, use only some of its properties, and combine objects in different ways. The aspect layer decides which objects are needed and how to compose them to produce the desired outcome.

- An aspect does not need to use all domain objects.
- An aspect may use only some properties of an object, not the whole thing.
- The same object may look very different across aspects — this is correct, not a problem.

Structure the aspect layer into composable units — strategies, workflows, pipelines — so that aspects can be swapped without changing the objects or the value definition.

---

## Axiology (Value layer) — User Value (Why)

The value layer encodes **what the end user needs** from this software. It answers: which features are worth building? Which results do users actually need? What does a good outcome look like from their perspective?

This is the purpose layer — it exists to represent the user's goals, not the system's internals. In code it is the entry point: the use-case, command, or application service that says "the user needs X." Everything below it (aspect, object) exists to serve what the value layer defines.

The value layer encodes:
- Which user needs are worth satisfying (feature selection)
- What a successful result looks like (evaluation)
- What must never happen (validation)
- Which aspect should deliver the result

Because the value layer represents user intent, it delegates the *how* to the aspect layer. Keep it explicit in logic — if the user's need only lives in a comment or a ticket, it has not been encoded in the value layer yet.

---

## How the Three Relate

```
value layer   →  defines what is worth doing (user need)
    ↓
aspect layer  →  defines how to do it, from which aspect
    ↓
object layer  →  defines what exists to operate on
```

- The aspect layer uses objects to realize the value.
- The value layer influences the aspect layer through selection, evaluation, and validation.
- Objects remain stable — they are not shaped by any single aspect or value concern.

**Design order**: define value first → design aspects second → define/refine objects last. In practice this is iterative, but the conceptual direction stays the same.

---

## Common Design Smells

| Smell | Likely cause |
|---|---|
| Selection logic duplicated across callers | Value layer not extracted |
| Object changes shape for different callers | Object layer polluted by aspect concerns |
| Algorithm hard-coded with magic thresholds | Value mixed into aspect layer |
| God object that evaluates, executes, and models | No layer separation |
| Object too large — covers multiple concerns | Abstraction level mismatched to concern |
| Object too small — callers must reconstruct meaning | Abstraction level too fine-grained |
| User need only in docs, not in code | Value layer implicit rather than encoded |
