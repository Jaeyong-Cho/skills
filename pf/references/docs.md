# Documentation

Documentation is living documentation of system — updated after each confirmed implementation, not per-decision. Describes current state of system, not history of decisions (that is what ADRs are for).

Output: `.pf/src/docs/`

## Structure

```
.pf/src/docs/
├── index.md                  — introduction and chapter links
├── value/
│   ├── index.md              — chapter intro: what user goals system serves
│   ├── 01-<entry-point>.md   — one file per value entry point / command / use case
│   └── ...
├── aspect/
│   ├── index.md              — chapter intro: how system works end-to-end
│   ├── 01-<concern>.md       — one file per concern handler (auth, billing, etc.)
│   └── ...
└── object/
    ├── index.md              — chapter intro: which objects exist and what they own
    ├── 01-<entity>.md        — one file per domain entity / aggregate
    └── ...
```

Number files so they sort correctly in sidebar. Use kebab-case for all names. One file per individual entity — not one file per component covering multiple entities.

Each file covers one entity from its layer's angle:
- **Value** — user need this entry point serves: what it does, success criteria, what must never happen
- **Aspect** — how concern is handled: algorithm, workflow, which objects used and from what angle
- **Object** — entity's full identity: properties, actions, behaviors, relationships, invariants

---

## docs/index.md

```markdown
# Documentation

This manual documents the current system design using the VAO framework.

## Chapters

- [Value — Why](./value/index.md)
- [Aspect — How](./aspect/index.md)
- [Object — What](./object/index.md)
```

## Layer index.md

```markdown
# Value

One paragraph on what this chapter covers — user goals and outcomes system exists to deliver.

## Components

- [Component 1](./01-<component>.md)
- [Component 2](./02-<component>.md)
```

(Same pattern for `aspect/index.md` and `object/index.md`.)

## Entity files

Within each file, order content from **broad scope to narrow** — start with overall picture, then zoom into specifics.

**value/<entry-point>.md** — user need this entry point serves, what success looks like, what must never happen. Start with overall goal, narrow to specific constraints.

**aspect/<concern>.md** — how concern is handled: start with overall workflow, then narrow to decision logic and composable strategies. Include Mermaid diagrams for flows and interactions.

**object/<entity>.md** — entity's full identity: start with top-level role, then narrow to properties, behaviors, relationships, and invariants. Include Mermaid diagrams for relationships.

---

## When to update

Update manual **after** code review is confirmed — not before. Manual reflects what is actually in code, not what was planned. If ADR was partially implemented or changed during implementation, manual should reflect what was actually built.

When updating:
- Find component file in each layer (or create one if component is new)
- Update only sections that changed
- Keep language describing current system, not history of changes

## Adding a new component

Create numbered file in each of three layer directories and update each layer's `index.md` and `SUMMARY.md`.

## SUMMARY.md entries

```markdown
- [Documentation](./docs/index.md)
  - [Value](./docs/value/index.md)
    - [Login Command](./docs/value/01-login-command.md)
    - [Checkout Command](./docs/value/02-checkout-command.md)
  - [Aspect](./docs/aspect/index.md)
    - [Auth Aspect](./docs/aspect/01-auth-aspect.md)
    - [Billing Aspect](./docs/aspect/02-billing-aspect.md)
  - [Object](./docs/object/index.md)
    - [User](./docs/object/01-user.md)
    - [Order](./docs/object/02-order.md)
    - [Line Item](./docs/object/03-line-item.md)
```
