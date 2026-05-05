# Documentation Mode

Output directory: `.aeo/src/docs/<slug>/`

## File structure

```
.aeo/src/docs/<slug>/
├── index.md        — overview and links to sections
├── axiology.md     — Why: values, goals, success criteria
├── epistemology.md — How: methods, workflows, decision logic
├── ontology.md     — What: entities, properties, relationships
└── diagram.md      — Mermaid diagram of layer relationships
```

Split further if any file grows long — for example, a complex Epistemology section can become `epistemology/` with sub-pages per workflow.

## index.md

```markdown
# <Title>

Brief description of the subject being documented.

## Sections
- [Axiology — Why](./axiology.md)
- [Epistemology — How](./epistemology.md)
- [Ontology — What](./ontology.md)
- [Diagram](./diagram.md)
```

## diagram.md

Include a Mermaid diagram showing layer relationships and key components. Default to including one — only omit if the subject is trivially simple with no structure worth visualizing.

## SUMMARY.md entries

```markdown
- [Docs: <title>](./docs/<slug>/index.md)
  - [Axiology](./docs/<slug>/axiology.md)
  - [Epistemology](./docs/<slug>/epistemology.md)
  - [Ontology](./docs/<slug>/ontology.md)
  - [Diagram](./docs/<slug>/diagram.md)
```
