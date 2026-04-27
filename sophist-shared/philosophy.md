# Data Structure Design Philosophy

Used by **sophist-srs** (before creating SAD), **sophist-sad** (before creating SDD), and **sophist-sdd** (when specifying functions) to guide data structure thinking.

---

## The core question

Before designing any component or function, ask:

> **What are the independent objects, and what operations does this software perform on them?**

An **independent object** is a data entity that has meaning on its own — it does not need another object to exist or be understood. Once you have identified the independent objects, everything else follows:

1. **Independent objects** — entities that stand alone (a `User`, an `Order`, a `Report`)
2. **Relations** — how objects reference, contain, or depend on each other
3. **Operations** — a program is a set of transformations: objects in → objects out

---

## Applying it at each layer

### At SAD (architecture)

For each component, ask:

- What objects does this component **own**? (it creates, stores, or is responsible for them)
- What objects does it **receive** as input?
- What objects does it **produce** as output?
- What **relations** between objects does it manage?

The answers directly shape the component's `## Responsibility` and `## Interface`. If a component cannot answer these questions cleanly, it is doing too much — split it.

### At SDD (detailed design)

For each function, ask:

- What is the **input object type**? (what enters the transformation)
- What is the **output object type**? (what the transformation produces)
- What **intermediate objects** does the transformation create or read?

The `## Signature` encodes the input/output types. The `## Algorithm` describes the transformation steps. The `## Variables` names the intermediate objects. If a function's input or output type is unclear, the design is not ready to implement.

---

## Signal: when the design is wrong

- A component that operates on too many unrelated object types → split it
- A function whose output type is not a real object but a side effect → make the side effect's result an object too
- Objects that cannot exist without referencing another object that "owns" them → the owner should be a component, not a caller
- Relations that are implicit (caller must know the internal structure of another component's object) → the component is leaking its data model; add an abstraction layer
