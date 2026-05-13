# Documentation

The documentation is the living documentation of the system — updated after each confirmed implementation, not per-decision. It describes the current state of the system, not the history of decisions (that is what ADRs are for).

Output: `.pf/src/docs/`

## Structure

```
.pf/src/docs/
├── index.md              — introduction and chapter links
├── value/
│   ├── index.md          — chapter intro: what user goals the system serves
│   ├── 01-<component>.md — value for component 1
│   ├── 02-<component>.md — value for component 2
│   └── ...
├── aspect/
│   ├── index.md          — chapter intro: how the system works end-to-end
│   ├── 01-<component>.md — aspect for component 1
│   └── ...
└── object/
    ├── index.md          — chapter intro: which objects exist and what they own
    ├── 01-<component>.md — object for component 1
    └── ...
```

Number component files so they sort correctly in the sidebar. Use kebab-case for all names.

Each layer chapter covers **every component** from that single angle:
- **Value** — user needs, goals, success criteria, what must never happen
- **Aspect** — workflows, decision logic, composable strategies, entry points
- **Object** — entities, properties, behaviors, relationships, invariants

---

## docs/index.md

```markdown
# Documentation

This manual documents the current system design using the AEO framework.

## Chapters

- [Value — Why](./value/index.md)
- [Aspect — How](./aspect/index.md)
- [Object — What](./object/index.md)
```

## Layer index.md

```markdown
# Value

One paragraph on what this chapter covers — the user goals and outcomes the system exists to deliver.

## Components

- [Component 1](./01-<component>.md)
- [Component 2](./02-<component>.md)
```

(Same pattern for `aspect/index.md` and `object/index.md`.)

## Component files

Within each component file, order content from **broad scope to narrow** — start with the overall picture, then zoom into specifics.

**value/<component>.md** — user needs this component serves, what success looks like, what must never happen. Start with the overall goal, narrow to specific constraints.

**aspect/<component>.md** — how this component's need is met: start with the overall workflow, then narrow to decision logic and composable strategies. Include Mermaid diagrams for flows and interactions.

**object/<component>.md** — the objects that exist for this component: start with the top-level aggregate, then narrow to properties, behaviors, relationships, and invariants. Include Mermaid diagrams for object relationships.

---

## When to update

Update the manual **after** a code review is confirmed — not before. The manual reflects what is actually in the code, not what was planned. If an ADR was partially implemented or changed during implementation, the manual should reflect what was actually built.

When updating:
- Find the component file in each layer (or create one if this component is new)
- Update only the sections that changed
- Keep language describing the current system, not the history of changes

## Adding a new component

Create a numbered file in each of the three layer directories and update each layer's `index.md` and `SUMMARY.md`.

## SUMMARY.md entries

```markdown
- [Documentation](./docs/index.md)
  - [Value](./docs/value/index.md)
    - [Component 1](./docs/value/01-<component>.md)
    - [Component 2](./docs/value/02-<component>.md)
  - [Aspect](./docs/aspect/index.md)
    - [Component 1](./docs/aspect/01-<component>.md)
    - [Component 2](./docs/aspect/02-<component>.md)
  - [Object](./docs/object/index.md)
    - [Component 1](./docs/object/01-<component>.md)
    - [Component 2](./docs/object/02-<component>.md)
```
