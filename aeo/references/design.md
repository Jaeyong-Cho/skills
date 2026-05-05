# Design / Architecture Mode

Output: `.aeo/src/design/<ID>-<slug>.md`

## ID assignment

```bash
ls .aeo/src/design/*.md 2>/dev/null | wc -l
```

Zero-padded 4-digit format: `0001`, `0002`, etc.

## What to write

There is no fixed template — let the content determine the structure. Think through the three layers and write what is actually true about the system being designed.

The questions to answer:

**Axiology** — What is this software automating, and why is that valuable? What does success look like? What must never happen? Which behaviors are worth building?

**Epistemology** — From which aspect(s) are the ontological objects being used? What algorithm makes the decision? How do the objects interact to produce the outcome? What strategies or workflows are composable here?

**Ontology** — What entities must exist? What distinguishes each from others? Is the abstraction level right for this concern — not too large, not too small? Are they stable and invariant across the different aspects that will use them?

Also call out any leakage between layers, and include a Mermaid diagram showing the layer structure and relationships between components.

## SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./design/<ID>-<slug>.md)
```
