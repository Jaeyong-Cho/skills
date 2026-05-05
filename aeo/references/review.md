# Code Review Mode

Output: `.aeo/src/reviews/<ID>-<slug>.md`

## ID assignment

```bash
ls .aeo/src/reviews/*.md 2>/dev/null | wc -l
```

Use zero-padded 4-digit format: `0001`, `0002`, etc.

## File structure

```markdown
# [<ID>] Review: <title>

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

## Current Structure

```mermaid
...
```

## Target Structure

```mermaid
...
```

## Summary
<overall assessment — what's working, what needs attention>
```

Include both diagrams for every review. If no violations exist, a single diagram confirming the correct layer boundaries is sufficient — label it "Structure" instead of "Current / Target".

## SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./reviews/<ID>-<slug>.md)
```
