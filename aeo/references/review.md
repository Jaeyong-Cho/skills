# Code Review Mode

Output directory: `.aeo/src/reviews/<slug>/`

## File structure

```
.aeo/src/reviews/<slug>/
├── index.md     — summary: what was reviewed, overall verdict, link to findings
├── layers.md    — layer classification of the existing code
├── findings.md  — violations found, each with why it matters and suggested fix
└── diagram.md   — Mermaid diagram: current structure vs target structure
```

## index.md

```markdown
# Review: <title>

Brief description of what was reviewed.

## Overall verdict
<clean / minor violations / significant violations>

## Sections
- [Layer Classification](./layers.md)
- [Findings](./findings.md)
- [Diagram](./diagram.md)
```

## layers.md

Map each code section to its AEO layer:

```markdown
# Layer Classification

| Code / Module | Assigned Layer | Notes |
|---------------|---------------|-------|
| ...           | Axiology      | ...   |
| ...           | Epistemology  | ...   |
| ...           | Ontology      | ...   |
```

## findings.md

One section per finding. Structure each as:

```markdown
# Findings

## [Layer] <Issue title>
**Why it matters**: ...
**Suggested fix**: ...

## [Layer] <Issue title>
...
```

If layers are cleanly separated, say so — don't invent problems.

## diagram.md

Show the current structure and the target structure side by side:

```markdown
# Structure Diagram

## Current (tangled)
\`\`\`mermaid
...
\`\`\`

## Target (separated)
\`\`\`mermaid
...
\`\`\`
```

Include this diagram for every review — even clean code benefits from a diagram confirming the correct layer boundaries.

## SUMMARY.md entries

```markdown
- [Review: <title>](./reviews/<slug>/index.md)
  - [Layer Classification](./reviews/<slug>/layers.md)
  - [Findings](./reviews/<slug>/findings.md)
  - [Diagram](./reviews/<slug>/diagram.md)
```
