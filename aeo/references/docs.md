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

Include a Mermaid diagram showing the relationships between the three layers and their key components. A diagram is the default — only omit one if the subject is genuinely too simple to have any structure worth visualizing.

Add the file as a nested entry in `.aeo/src/SUMMARY.md` under `Documentation`.
