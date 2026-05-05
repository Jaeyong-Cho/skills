# Documentation Mode

Output file: `.aeo/src/docs/<slug>.md`

Structure documentation around the three AEO layers:

```markdown
# <Title>

## Why — Axiology
<values, goals, success criteria, what must never happen>

## How — Epistemology
<methods, workflows, decision logic, composable units>

## What — Ontology
<entities, their properties, relationships, invariants>
```

Include a Mermaid diagram if the relationships between components benefit from visual explanation.

Add the file as a nested entry in `.aeo/src/SUMMARY.md` under `Documentation`.
