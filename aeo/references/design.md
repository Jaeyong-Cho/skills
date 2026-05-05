# Design / Architecture Mode

Output file: `.aeo/src/design/<slug>.md`

## Process

1. **Axiology first** — what outcomes matter? what does success look like? what must never happen?
2. **Epistemology second** — what algorithms, workflows, or decision processes realize those values?
3. **Ontology last** — what stable entities do the methods operate on?
4. Include a Mermaid diagram showing the layer relationships and component structure.
5. Call out any leakage between layers.

## Mermaid diagram template

Adapt the nodes to the actual system. Always include this in design outputs.

````markdown
```mermaid
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
```
````

## Output structure

```markdown
# Design: <title>

## Axiology
<values, success criteria, what must never happen>

## Epistemology
<methods, workflows, decision logic>

## Ontology
<stable entities and their relationships>

## Architecture Diagram
<mermaid diagram>

## Layer Violations / Risks
<any leakage or design smells identified>
```

Add the file as a nested entry in `.aeo/src/SUMMARY.md` under `Design`.
