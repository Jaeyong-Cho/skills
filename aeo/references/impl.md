# Implementation and Refactoring Mode

**Always write a plan and get confirmation before touching any code.**

---

## Implementation

Output directory: `.aeo/src/impl/<slug>/`

### File structure

```
.aeo/src/impl/<slug>/
├── index.md     — overview: what is being built, links to sub-pages
├── plan.md      — step-by-step implementation steps and files to create
├── layers.md    — AEO layer mapping for each component
└── diagram.md   — Mermaid diagram of the target layer structure (required)
```

### index.md

```markdown
# Implementation: <title>

Brief description of what is being implemented.

## Sections
- [Plan](./plan.md)
- [Layer Mapping](./layers.md)
- [Diagram](./diagram.md)
```

### plan.md

```markdown
# Implementation Plan

## Steps
1. ...
2. ...

## Files to create
| File | Layer | Purpose |
|------|-------|---------|
```

### layers.md

```markdown
# AEO Layer Mapping

| Component | Layer | Reason |
|-----------|-------|--------|
```

### diagram.md

Include a Mermaid diagram showing the target layer structure. Required — do not skip even for small implementations.

```markdown
# Architecture Diagram

\`\`\`mermaid
graph TD
    ...
\`\`\`
```

### Confirmation gate

After writing all plan files, ask:

> "Here's the implementation plan. Does this look right? I'll write the code once you confirm."

Do not write source code before the user confirms.

### SUMMARY.md entries

```markdown
- [Impl: <title>](./impl/<slug>/index.md)
  - [Plan](./impl/<slug>/plan.md)
  - [Layer Mapping](./impl/<slug>/layers.md)
  - [Diagram](./impl/<slug>/diagram.md)
```

---

## Refactoring

Output directory: `.aeo/src/refact/<slug>/`

### File structure

```
.aeo/src/refact/<slug>/
├── index.md      — overview: what is being refactored, links to sub-pages
├── violations.md — current layer violations found in the code
├── plan.md       — step-by-step refactoring steps and files to modify
└── diagram.md    — Mermaid before/after diagram (required)
```

### violations.md

```markdown
# Current Layer Violations

| Location | Violation | Layer |
|----------|-----------|-------|
```

### plan.md

```markdown
# Refactoring Plan

## Steps
1. Extract Axiology: ...
2. Extract Epistemology: ...
3. Stabilize Ontology: ...

## Files to modify
| File | Change |
|------|--------|
```

### diagram.md

Before/after Mermaid diagram is the most important part of a refactoring plan — it makes the intent unambiguous. Required.

```markdown
# Structure Diagram

## Before (tangled)
\`\`\`mermaid
...
\`\`\`

## After (separated)
\`\`\`mermaid
...
\`\`\`
```

### Confirmation gate

After writing all plan files, ask:

> "Here's the refactoring plan. Does this look right? I'll apply the changes once you confirm."

Do not modify source code before the user confirms.

### SUMMARY.md entries

```markdown
- [Refact: <title>](./refact/<slug>/index.md)
  - [Violations](./refact/<slug>/violations.md)
  - [Plan](./refact/<slug>/plan.md)
  - [Diagram](./refact/<slug>/diagram.md)
```
