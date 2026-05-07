# Data Structure Design Philosophy

Used by **sophist-srs** (before creating SAD), **sophist-sad** (before creating SDD), and **sophist-sdd** (when specifying functions) to guide data structure thinking.

---

## The core question

Before designing any component or function, ask:

> **What are the independent objects, and what does this software produce from them?**

An **independent object** is a data entity that has meaning on its own — it does not need another object to exist or be understood. Once you have identified the independent objects, everything else follows:

1. **Independent objects** — entities that stand alone (`User`, `Order`, `Report`)
2. **Relations** — how objects reference, contain, or depend on each other
3. **Output** — what the program produces: a new object, a transformed object, or a structured collection of objects

---

## Design the output first

The output data structure is the most important design decision. It determines what consumers (other components, users, other programs) can do with the result. Design it before designing the transformation that produces it.

### Steps

**1. Name the output object**

Give the output a concrete type name. If you cannot name it, the design is not ready.

- Good: `ParsedConfig`, `ValidationResult`, `UserSummary`
- Not ready: "returns the data", "returns a dict", "returns some info"

**2. Define its fields from the independent objects**

The output object's fields come from the independent objects and their relations:

- A field that **is** an independent object → embed or reference it directly
- A field that **relates** two independent objects → make the relation explicit (e.g. `order.user_id`, not a raw string)
- A field that is derived from an object → name what it is derived from in the SDD description

**3. Define what is NOT in the output**

Explicitly state what the output excludes. This prevents scope creep and tells the caller what they must get elsewhere.

**4. Define the error output**

An error is also an output object. Name it: what fields does it carry? What does the caller need to know to handle it?

---

## Applying it at each layer

### At SAD (architecture)

For each component, design its output object before writing the Interface:

- What is the **name** of what this component produces?
- Which **independent objects** are embedded in it?
- Which **relations** does it express?
- What does a **failed** output look like — is it a separate error object, or does the success object carry a status field?

The output object definition becomes the `## Interface` return type. The component's `## Responsibility` is the transformation that produces it.

### At SDD (detailed design)

For each function, design the output object before writing the Signature:

- What is the **exact type** of the return value? Name every field.
- Are any fields themselves objects with their own structure? Name those too.
- What does the function return on **each error path** — the same type with an error field, or a distinct error type?

The `## Signature` encodes the output type. The `## Algorithm` describes how each step contributes to constructing it. The `## Variables` names intermediate objects that the final output is assembled from.

---

## Signal: when the design is wrong

- Output type cannot be named → not ready to implement; add a `### Review needed`
- Output contains a raw primitive where a named object would carry more meaning → promote the primitive to an object
- Two functions produce outputs of the same shape but different names → consider a shared output type
- A component's output must be unpacked by the caller to get the real object inside → the component is wrapping unnecessarily; return the inner object directly
- Error output is undocumented → every function must name its error output explicitly
