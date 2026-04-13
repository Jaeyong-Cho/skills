# Cascade: SRS → SAD and SIT

When SRS items are marked `reviewed`, create corresponding SAD and SIT items. This connects the "what" (requirements) to the "how" (architecture).

---

## Find next available IDs

```bash
ls book/src/sad/ | grep "^SAD-[0-9]" | sort -t- -k2 -n | tail -1
ls book/src/sit/ | grep "^SIT-[0-9]" | sort -t- -k2 -n | tail -1
```

Note: `SAD-001` is always reserved for the project directory structure item. If it doesn't exist yet, create it first. If it exists, update it to reflect any new directories implied by the new components.

---

## SAD item template

Create `book/src/sad/SAD-{NNN}.md` for each architectural component implied by the reviewed SRS items. Group related SRS items into one SAD component when they naturally belong together (same module, same responsibility). One SAD item can trace to multiple SRS items.

```markdown
# SAD-{NNN}: <component or structure title>

## State
`draft`

## Tags
`#tag1`

## Why
<one sentence — why this component exists and what architectural problem it solves>

## Traces
- ← [SRS-{NNN}](../srs/SRS-{NNN}.md): <which requirement this component satisfies and why this component boundary was chosen>
- → [SDD-{NNN}](../sdd/SDD-{NNN}.md): TBD — SDD items created after SAD review
- → [SIT-{NNN}](../sit/SIT-{NNN}.md): <what integration scenario this test covers>

## Diagram

```mermaid
graph LR
  <CallerComponent> --> SAD-{NNN}["<ComponentName>\n<file path>"]
  SAD-{NNN} --> <DependencyComponent>
```

## Location
`src/<path>/<FileName>.{ext}`

## Responsibility
<single sentence — what this component does and nothing else>

## Dependencies
<other SAD components this depends on, or "none">

## Interface
- `<methodName>(params) → ReturnType` — <one-line description>

> **Review needed** — <question about component boundary, file location, interface, or dependency>
```

Add to `SUMMARY.md` under Architectural Design and add a row to `book/src/sad/index.md`.

---

## SIT item template

Create one `book/src/sit/SIT-{NNN}.md` per SAD item that has meaningful interactions with other components. If a SAD component has no external callers or dependencies, a SIT item may not be needed — use judgment.

```markdown
# SIT-{NNN}: <test title describing the interaction>

## State
`draft`

## Tags
`#tag1`

## Why
<one sentence — what component interaction this test verifies and why this boundary matters>

## Traces
- ← [SAD-{NNN}](../sad/SAD-{NNN}.md): <which interface boundary this test exercises>

## Diagram

```mermaid
sequenceDiagram
  participant <ComponentA>
  participant <ComponentB>
  <ComponentA>->><ComponentB>: <call>
  <ComponentB>-->><ComponentA>: <response>
```

## Components under test
<ComponentA> ↔ <ComponentB>

## Scenario
<what interaction is being verified — the specific call and its expected effect>

## Expected behavior
<specific observable outcome>

> **Review needed** — <question about test boundary, mock strategy, or scenario completeness>
```

Add to `SUMMARY.md` under Integration Tests and add a row to `book/src/sit/index.md`.

---

## After creating SAD and SIT items

1. Add `→ [SAD-{NNN}](../sad/SAD-{NNN}.md): <why>` to the reviewed SRS item's Traces section
2. Update `book/src/sad/index.md` traceability table with new SAD rows
3. Update `book/src/sit/index.md` traceability table with new SIT rows
4. Update `book/src/tags.md` for any new tags used
