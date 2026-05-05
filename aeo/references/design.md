# Design / Architecture Mode

Output directory: `.aeo/src/design/<slug>/`

## File structure

Create one file per concern — never put everything in one file:

```
.aeo/src/design/<slug>/
├── index.md        — overview: purpose, design direction, links to sub-pages
├── axiology.md     — values, success criteria, what must never happen
├── epistemology.md — methods, workflows, decision logic
├── ontology.md     — stable entities, properties, relationships
└── diagram.md      — Mermaid architecture diagram(s)
```

## Process

1. **Axiology first** — what outcomes matter? what does success look like? what must never happen?
2. **Epistemology second** — what algorithms, workflows, or decision processes realize those values?
3. **Ontology last** — what stable entities do the methods operate on?
4. Draw the architecture diagram showing layer relationships and component structure.
5. Call out any leakage between layers.

## index.md

```markdown
# Design: <title>

Brief description of the system and its purpose.

## Design direction
Axiology → Epistemology → Ontology

## Sections
- [Axiology](./axiology.md)
- [Epistemology](./epistemology.md)
- [Ontology](./ontology.md)
- [Architecture Diagram](./diagram.md)

## Layer violations / risks
<any cross-layer leakage identified>
```

## axiology.md

```markdown
# Axiology — Value

## Value Definition
<what matters and how much>

## Value Evaluation
<how results are measured>

## Value Validation
<minimum acceptable thresholds>

## Value Selection
<how the best option is chosen>
```

## epistemology.md

```markdown
# Epistemology — Method

## Workflow
<step-by-step process>

## Decision logic
<how choices are made>

## Composable units
<strategies, policies, pipelines and how they can be swapped>
```

## ontology.md

```markdown
# Ontology — Entities

## <Entity Name>
**Properties**: ...
**Behaviors**: ...
**Relationships**: ...
**Invariant**: <what stays the same regardless of which Epistemology uses it>
```

## diagram.md

```markdown
# Architecture Diagram

\`\`\`mermaid
graph TD
    subgraph Axiology
        A1[Value Definition] --> A2[Value Evaluation]
        A2 --> A3[Value Validation]
        A3 --> A4[Value Selection]
    end
    subgraph Epistemology
        E1[Algorithm / Workflow]
        E2[Strategy / Policy]
    end
    subgraph Ontology
        O1[Entity A]
        O2[Entity B]
    end
    A4 -->|selects| E1
    E1 -->|uses| O1
    E1 -->|uses| O2
    E2 -->|uses| O1
\`\`\`
```

Adapt all nodes to the actual system.

## SUMMARY.md entries

Add a nested chapter group under `Design`:

```markdown
- [Design: <title>](./design/<slug>/index.md)
  - [Axiology](./design/<slug>/axiology.md)
  - [Epistemology](./design/<slug>/epistemology.md)
  - [Ontology](./design/<slug>/ontology.md)
  - [Diagram](./design/<slug>/diagram.md)
```
