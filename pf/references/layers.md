# VAO Layers in Detail

## Origin

VAO = software design philosophy inspired by OOP and AOP. Three layers, each answering a different question:

| Layer | Question |
|-------|----------|
| **Value** | What user goal is worth automating? |
| **Aspect** | What algorithm realizes that goal, and from which angle? |
| **Object** | What stable domain things does the system operate on? |

Each class belongs to the layer that matches its responsibility. If a class is hard to place, the layer boundary is probably wrong.

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

Aspect layer has two distinct roles — keep them separate in your thinking:

**Algorithm** — the workflow, strategy, or computation that realizes the user goal. What steps, in what order, with what logic. This is the "how."

**Lens** — which domain objects to use and which of their properties matter here. AOP thinking: different aspects see the same object differently. `AuthAspect` reads `user.role`. `BillingAspect` reads `user.plan`. Same object, different angles — correct, not a problem. Aspect does not need to use all objects, or all properties of any object.

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

| Smell | Layer | Likely cause |
|---|---|---|
| Selection logic duplicated across callers | Value | Value layer not extracted |
| Algorithm hard-coded with magic thresholds | Value | Value mixed into aspect layer |
| User need only in docs, not in code | Value | Value layer implicit rather than encoded |
| Aspect with no clear algorithm — just routes calls | Aspect | Aspect is a pass-through, not a real layer |
| Aspect duplicates logic that belongs on the object | Aspect | Object is too thin — logic leaked upward |
| Aspect used as catch-all for unrelated behavior | Aspect | Single responsibility violated — split the aspect |
| God object that evaluates, executes, and models | Object | No layer separation |
| Object too large — covers multiple concerns | Object | Abstraction level mismatched to concern |
| Object too small — callers must reconstruct meaning | Object | Abstraction level too fine-grained |
