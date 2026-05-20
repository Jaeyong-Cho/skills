# VAO Layers in Detail

## Origin

VAO = software design philosophy inspired by OOP and AOP. Program = automation tool for making decisions to achieve goal. Designing it well requires three kinds of thinking:

1. **What is user goal worth automating?** → value layer
2. **What algorithm and objects realize that goal?** → aspect layer
3. **What stable objects does system operate on?** → object layer

Two types of classes: **domain objects** (what exists) and **aspect objects** (how things are viewed and used to achieve goal). Value layer sits above both, determining which user goals are worth pursuing.

---

## Value layer — User Value (Why)

Value layer encodes **what end user needs** from software. Answers: which features worth building? Which results do users actually need? What does good outcome look like from their perspective?

Purpose layer — exists to represent user's goals, not system's internals. In code it is entry point: use-case, command, or application service that says "user needs X." Everything below it (aspect, object) exists to serve what value layer defines.

Value layer encodes:
- Which user needs are worth satisfying (feature selection)
- What successful result looks like (evaluation)
- What must never happen (validation)
- Which aspect should deliver result

Value layer represents user intent, delegates *how* to aspect layer. Keep explicit in logic — if user's need only lives in comment or ticket, it has not been encoded in value layer yet.

---

## Aspect layer — Algorithm / Aspect (How)

Aspect layer has two responsibilities:

1. **How to meet need** — algorithm, workflow, or strategy that realizes user goal
2. **Which objects to use and how to see them** — from what angle are domain objects viewed? What subset of properties matters here?

AOP thinking: different aspects see same object differently, use only some properties, combine objects in different ways. Aspect layer decides which objects needed and how to compose them to produce desired outcome.

- Aspect does not need to use all domain objects.
- Aspect may use only some properties of object, not whole thing.
- Same object may look very different across aspects — correct, not problem.

For cross-cutting concern design with code examples, read `references/aop.md`.

Structure aspect layer into composable units — strategies, workflows, pipelines — so aspects can be swapped without changing objects or value definition.

---

## Object layer — Existence (What)

Domain objects = things that must exist to satisfy both user need and aspect. Not arbitrary catalog of domain things — objects that aspect selects and uses, shaped to serve concerns value layer defines.

Domain object is not data container. Defines full identity of domain target:

- **Properties** — state it holds
- **Actions** — what it can do (methods, commands, transitions)
- **Behaviors** — how it responds to events or conditions
- **Relationships** — how it connects to other objects

Class that only holds data with no actions or behaviors is data bag, not domain object. If logic that belongs to object is scattered across service or aspect-layer classes, that is leakage smell — object is too thin.

**Key design question**: What distinguishes this object from others, and is it right abstraction for concern being served?

**Key design constraint**: Size must match concern.

- If concern is `DNA`, defining `Atom` object is reasonable.
- If concern is `Animal`, `Atom` is too small — define `Arm`, `Head`, `Body` instead.
- Object must not be too large (covering things outside concern) or too small (forcing callers to reconstruct meaning).

**Invariance principle**: Domain object must remain same regardless of which aspect is looking at it. If object changes shape for specific use case, it has leaked into aspect layer.

Domain objects are stable foundation. Multiple aspect-layer components can use same object from different angles without object knowing or caring.

### Relationships

For each relationship, decide: cardinality, ownership (who controls lifecycle), navigability (which direction), and aggregate boundary (what changes atomically together). View-specific joins belong in aspect layer, not object.

---

## How the Three Relate

```
value layer   →  defines what is worth doing (user need)
    ↓
aspect layer  →  defines how to do it, from which aspect
    ↓
object layer  →  defines what exists to operate on
```

- Aspect layer uses objects to realize value.
- Value layer influences aspect layer through selection, evaluation, and validation.
- Objects remain stable — not shaped by any single aspect or value concern.

**Design order**: define value first → design aspects second → define/refine objects last. Iterative in practice, but conceptual direction stays same.

---

## Common Design Smells

| Smell | Likely cause |
|---|---|
| Selection logic duplicated across callers | Value layer not extracted |
| Algorithm hard-coded with magic thresholds | Value mixed into aspect layer |
| God object that evaluates, executes, and models | No layer separation |
| Object too large — covers multiple concerns | Abstraction level mismatched to concern |
| Object too small — callers must reconstruct meaning | Abstraction level too fine-grained |
| User need only in docs, not in code | Value layer implicit rather than encoded |
