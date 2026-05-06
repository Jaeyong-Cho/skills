# AEO Layers in Detail

## Origin

AEO is a software design philosophy inspired by OOP and AOP. A program is an automation tool for making decisions to achieve a goal. Designing it well requires three kinds of thinking:

1. **What is the user goal worth automating?** → value layer
2. **What algorithm and objects realize that goal?** → method layer
3. **What stable objects does the system operate on?** → entity layer

This leads to two types of classes: **entity objects** (what exists) and **aspect objects** (how things are viewed and used to achieve a goal). The value layer sits above both, determining which user goals are worth pursuing.

---

## Entity layer — Existence (What)

Entity objects are the things that must exist to satisfy both the user need and the method. They are not an arbitrary catalog of domain things — they are the objects that the method selects and uses, shaped to serve the concerns that the value layer defines.

An entity object is not just a data container. It defines the full identity of a domain target:

- **Properties** — the state it holds
- **Actions** — what it can do (methods, commands, transitions)
- **Behaviors** — how it responds to events or conditions
- **Relationships** — how it connects to other entities

A class that only holds data with no actions or behaviors is a data bag, not an entity object. If the logic that belongs to an entity is scattered across service or method-layer classes instead, that is a leakage smell — the entity is too thin.

**The key design question**: What distinguishes this object from others, and is it the right abstraction for the concern being served?

**The key design constraint**: Size must match the concern.

- If the concern is `DNA`, defining an `Atom` object is reasonable.
- If the concern is `Animal`, `Atom` is too small — define `Arm`, `Head`, `Body` instead.
- The object must not be too large (covering things outside the concern) or too small (forcing callers to reconstruct meaning).

**The invariance principle**: An entity object must remain the same regardless of which aspect is looking at it. If the object changes shape for a specific use case, it has leaked into the method layer.

Entity objects are the stable foundation. Multiple method-layer components can use the same entity from different angles without the entity knowing or caring.

---

## Method layer — Algorithm / Aspect (How)

The method layer has two responsibilities:

1. **How to meet the need** — the algorithm, workflow, or strategy that realizes the user goal
2. **Which objects to use and how to see them** — from what angle are the entity objects viewed? What subset of their properties matters here?

This is where AOP thinking enters: different aspects see the same entity differently, use only some of its properties, and combine entities in different ways. The method layer decides which entities are needed and how to compose them to produce the desired outcome.

- An aspect does not need to use all entity objects.
- An aspect may use only some properties of an entity, not the whole thing.
- The same entity may look very different across aspects — this is correct, not a problem.

Structure the method layer into composable units — strategies, workflows, pipelines — so that methods can be swapped without changing the entities or the value definition.

---

## Value layer — User Value (Why)

The value layer encodes **what the end user needs** from this software. It answers: which features are worth building? Which results do users actually need? What does a good outcome look like from their perspective?

This is the purpose layer — it exists to represent the user's goals, not the system's internals. In code it is the entry point: the use-case, command, or application service that says "the user needs X." Everything below it (method, entity) exists to serve what the value layer defines.

The value layer encodes:
- Which user needs are worth satisfying (feature selection)
- What a successful result looks like (evaluation)
- What must never happen (validation)
- Which method should deliver the result

Because the value layer represents user intent, it delegates the *how* to the method layer. Keep it explicit in logic — if the user's need only lives in a comment or a ticket, it has not been encoded in the value layer yet.

---

## How the Three Relate

```
value layer   →  defines what is worth doing (user need)
    ↓
method layer  →  defines how to do it, from which aspect
    ↓
entity layer  →  defines what exists to operate on
```

- The method layer uses entities to realize the value.
- The value layer influences the method layer through selection, evaluation, and validation.
- Entities remain stable — they are not shaped by any single method or value concern.

**Design order**: define value first → design methods second → define/refine entities last. In practice this is iterative, but the conceptual direction stays the same.

---

## Common Design Smells

| Smell | Likely cause |
|---|---|
| Selection logic duplicated across callers | Value layer not extracted |
| Entity changes shape for different callers | Entity layer polluted by method concerns |
| Algorithm hard-coded with magic thresholds | Value mixed into method layer |
| God object that evaluates, executes, and models | No layer separation |
| Object too large — covers multiple concerns | Abstraction level mismatched to concern |
| Object too small — callers must reconstruct meaning | Abstraction level too fine-grained |
| User need only in docs, not in code | Value layer implicit rather than encoded |
