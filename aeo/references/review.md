# Code Review Mode

Output: `.aeo/src/reviews/<ID>-<slug>.md`

## ID assignment

```bash
ls .aeo/src/reviews/*.md 2>/dev/null | wc -l
```

Zero-padded 4-digit format: `0001`, `0002`, etc.

## What to write

There is no fixed template — structure the review around what the code actually reveals. The goal is to identify whether the three layers are cleanly separated and whether the ontological objects are well-designed for their concern.

Questions to answer through the review:

**Layer separation** — Is value logic (Axiology) explicit and separate? Is the method/aspect (Epistemology) composable and swappable? Are entities (Ontology) stable and invariant across the aspects that use them?

**Ontology quality** — Is the abstraction level right for the concern? Is each object distinguishable from others? Do objects change shape depending on who uses them (a smell)?

**Aspect leakage** — Are Epistemological views bleeding into Ontological definitions? Does an object carry fields or methods that only make sense from one specific aspect?

**Axiology visibility** — Is selection, evaluation, and validation explicit in code, or hidden in conditionals and magic numbers?

For each finding, explain why it matters — not just which rule it breaks. Include a Mermaid diagram showing the current structure and, if violations exist, the target structure.

## SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./reviews/<ID>-<slug>.md)
```
