# Code Review Mode

Output: a single file `.aeo/src/reviews/<slug>.md`

## File structure

```markdown
# Review: <title>

Brief description of what was reviewed.

**Verdict**: clean / minor violations / significant violations

## Layer Classification

| Code / Module | Layer | Notes |
|---------------|-------|-------|
| ...           | Axiology | ... |
| ...           | Epistemology | ... |
| ...           | Ontology | ... |

## Findings

### [Layer] <Issue title>
**Why it matters**: ...
**Suggested fix**: ...

### [Layer] <Issue title>
...

## Structure Diagram

### Current
```mermaid
...
```

### Target
```mermaid
...
```

## Summary
<overall assessment — what's working, what needs attention>
```

Include the before/after diagram for every review — even clean code benefits from a diagram confirming correct layer boundaries. If no violations exist, a single diagram showing the clean structure is sufficient.

## SUMMARY.md entry

```markdown
  - [<title>](./reviews/<slug>.md)
```
