# Documentation

The documentation is the living documentation of the system — updated after each confirmed implementation, not per-decision. It describes the current state of the system, not the history of decisions (that is what ADRs are for).

Output: `.aeo/src/docs/`

## Structure

```
.aeo/src/docs/
├── index.md              — introduction and table of contents
├── 01-<topic>/
│   ├── index.md          — chapter introduction and section links
│   ├── 01-value.md       — Why: user needs, goals, success criteria
│   ├── 02-method.md      — How: workflows, decision logic, composable units
│   └── 03-entity.md      — What: entities, properties, behaviors, relationships
├── 02-<topic>/
│   └── ...
```

Number chapters and sections so they sort correctly in the sidebar. Use kebab-case for directory and file names.

---

## docs/index.md

```markdown
# Documentation

This manual documents the current system design using the AEO framework.

## Chapters

- [Chapter 1: <Topic>](./01-<topic>/index.md)
- [Chapter 2: <Topic>](./02-<topic>/index.md)
```

## Chapter index.md

```markdown
# Chapter N: <Topic>

One paragraph introducing what this chapter covers and why it matters.

## Sections

- [Value — Why](./01-value.md)
- [Method — How](./02-method.md)
- [Entity — What](./03-entity.md)
```

## Section files

**01-value.md** — user needs this topic serves, what success looks like, what must never happen

**02-method.md** — how the need is met: workflows, decision logic, composable strategies. Include Mermaid diagrams for flows and interactions.

**03-entity.md** — the objects that exist: properties, behaviors, relationships, and invariants. Include Mermaid diagrams for entity relationships.

---

## When to update

Update the manual **after** a code review is confirmed — not before. The manual reflects what is actually in the code, not what was planned. If an ADR was partially implemented or changed during implementation, the manual should reflect what was actually built.

When updating:
- Find the relevant chapter (or create one if this is a new topic)
- Update only the sections that changed
- Keep language describing the current system, not the history of changes

## Adding a new chapter

Create a new numbered chapter directory with its three section files and update both `docs/index.md` and `SUMMARY.md`.

## SUMMARY.md entries

```markdown
- [Documentation](./docs/index.md)
  - [Chapter 1: <Topic>](./docs/01-<topic>/index.md)
    - [Value](./docs/01-<topic>/01-value.md)
    - [Method](./docs/01-<topic>/02-method.md)
    - [Entity](./docs/01-<topic>/03-entity.md)
```
