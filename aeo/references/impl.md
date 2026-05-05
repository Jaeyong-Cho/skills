# Implementation and Refactoring Mode

**Always write a plan and get confirmation before touching any code.**

---

## Implementation

Output file: `.aeo/src/impl/<slug>.md`

### Step 1 — Write the plan

Include a Mermaid diagram in every plan — it is the clearest way to show which components belong to which layer and how they relate. Do not skip the diagram even for small implementations.

```markdown
# Implementation Plan: <title>

## AEO Layer Mapping
| Component | Layer | Reason |
|-----------|-------|--------|

## Architecture Diagram
<mermaid diagram showing target layer structure — required>

## Steps
1. ...
2. ...

## Files to create
| File | Layer | Purpose |
|------|-------|---------|
```

### Step 2 — Ask for confirmation

> "Here's the implementation plan. Does this look right? I'll write the code once you confirm."

### Step 3 — Execute after confirmation

Write code following the layer separation:
- Axiology components: value definitions, scorers, validators, selectors — dedicated modules/classes
- Epistemology components: algorithms, pipelines, strategies — composable and swappable
- Ontology components: domain models — stable, free of method-specific assumptions

Add the plan file as a nested entry in `.aeo/src/SUMMARY.md` under `Implementation Plans`.

---

## Refactoring

Output file: `.aeo/src/refact/<slug>.md`

### Step 1 — Write the plan

Include a before/after Mermaid diagram showing the current tangled structure and the target separated structure. This is the most important part of a refactoring plan — it makes the intent unambiguous.

```markdown
# Refactoring Plan: <title>

## Current Layer Violations
| Location | Violation | Layer |
|----------|-----------|-------|

## Target Structure
<mermaid diagram: before (tangled) → after (separated) — required>

## Steps
1. Extract Axiology: ...
2. Extract Epistemology: ...
3. Stabilize Ontology: ...

## Files to modify
| File | Change |
|------|--------|
```

### Step 2 — Ask for confirmation

> "Here's the refactoring plan. Does this look right? I'll apply the changes once you confirm."

### Step 3 — Execute after confirmation

Apply changes layer by layer. Don't modify behavior — only separate concerns.

Add the plan file as a nested entry in `.aeo/src/SUMMARY.md` under `Refactoring Plans`.
