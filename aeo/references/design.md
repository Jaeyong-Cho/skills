# Design / Architecture Mode

Output: a single file `.aeo/src/design/<slug>.md`

## File structure

```markdown
# Design: <title>

Brief description of the system and its purpose.

## Axiology — Value

### Value Definition
<what matters and how much>

### Value Evaluation
<how results are measured>

### Value Validation
<minimum acceptable thresholds>

### Value Selection
<how the best option is chosen>

## Epistemology — Method

### Workflow
<step-by-step process>

### Decision Logic
<how choices are made>

### Composable Units
<strategies, policies, pipelines and how they can be swapped>

## Ontology — Entities

### <Entity Name>
**Properties**: ...
**Behaviors**: ...
**Relationships**: ...
**Invariant**: <what stays the same regardless of which Epistemology uses it>

## Architecture Diagram

```mermaid
graph TD
    subgraph Axiology
        ...
    end
    subgraph Epistemology
        ...
    end
    subgraph Ontology
        ...
    end
```

## Layer Violations / Risks
<any cross-layer leakage identified — omit section if none>
```

## SUMMARY.md entry

Add a single line under `Design`:

```markdown
  - [<title>](./design/<slug>.md)
```
