# Implementation and Refactoring Mode

**Always write the plan file and get confirmation before touching any code.**

---

## Implementation

Output: `.aeo/src/impl/<ID>-<slug>.md`

### ID assignment

```bash
ls .aeo/src/impl/*.md 2>/dev/null | wc -l
```

Zero-padded 4-digit format: `0001`, `0002`, etc.

### What to write

There is no fixed template — write what is actually needed for the implementation to be unambiguous. Think through:

**What exists (Ontology)** — Which entities need to be created or used? Is the abstraction level right for this concern? Are they stable enough to be shared across multiple aspects?

**Which aspect (Epistemology)** — From what angle are the objects being used? What algorithm makes the decision? How do the components interact to produce the outcome?

**What value (Axiology)** — What does success look like? What selection or evaluation logic is needed?

Include a Mermaid diagram showing the target layer structure. This is the most important part of the plan — it makes the intended separation visible before any code is written.

List the files to create and which layer each belongs to.

After writing the plan, ask:

> "Here's the implementation plan. Does this look right? I'll write the code once you confirm."

Do not write source code before the user confirms.

### SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./impl/<ID>-<slug>.md)
```

---

## Refactoring

Output: `.aeo/src/refact/<ID>-<slug>.md`

### ID assignment

```bash
ls .aeo/src/refact/*.md 2>/dev/null | wc -l
```

### What to write

There is no fixed template. Identify the violations, explain why they are problems in terms of the AEO philosophy, and describe the target structure.

Key questions to answer:

- Which Ontological objects are being shaped by a specific aspect? (leakage)
- Where is Axiology implicit rather than encoded?
- Which Epistemological units are not composable or swappable?
- Is any object's abstraction level mismatched to the concern?

Include a before/after Mermaid diagram — this is the clearest way to communicate the intended restructuring. Required, do not skip.

After writing the plan, ask:

> "Here's the refactoring plan. Does this look right? I'll apply the changes once you confirm."

Do not modify source code before the user confirms.

### SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./refact/<ID>-<slug>.md)
```
