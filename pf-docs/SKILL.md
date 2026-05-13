---
name: pf-docs
description: |
  Write or update the AEO project documentation after an ADR is implemented. Documents the current state of the system — what is valuable, how it works, which objects are used — organized from high-level to detailed.
  Triggers: "pf-docs", "update the docs", "write documentation", "document this", after code review is confirmed and an ADR exists.
---

> Use `/caveman` for compressed output during this session.

# AEO Documentation

Documentation describes the **current state of the system**, not the history of decisions (that is what ADRs are for). Update after code review is confirmed — never before.

Read `../pf/references/layers.md` to understand the value/aspect/object philosophy, then read `../pf/references/docs.md` for the full structure, file templates, and SUMMARY.md format.

---

## Step 1: Identify the ADR

If the user names an ADR (e.g. "adr-001", "0001", "auth-flow"), find it:

```bash
ls .pf/src/adr/ | grep 0001
```

If no ADR is specified, list available ADRs and ask which one to document.

Read the ADR. Focus on: what was actually built, the user stories, and the entities involved.

---

## Step 2: Determine scope

Check what already exists in the layer directories:

```bash
ls .pf/src/docs/value/ .pf/src/docs/aspect/ .pf/src/docs/object/ 2>/dev/null
```

Decide:
- **New component** — this ADR introduces a component not yet documented; create one numbered file per layer
- **Update existing component** — this ADR changes an existing component; find its file in each layer and update only what changed

If updating, read the existing files first so you don't overwrite content that is still accurate.

---

## Step 3: Write the documentation

Create (or update) one file per layer for the component. Each file covers the **same component from one angle only**. Within each file, order content from broad scope to narrow.

**`value/<N>-<component>.md`** — user need this component serves:
- Start with the broad user goal
- Narrow to specific success criteria and constraints; what must never happen

**`aspect/<N>-<component>.md`** — how this component works:
- Start with the overall workflow or entry point
- Narrow to decision logic, strategies, and flows
- Mermaid diagrams for flows and interactions

**`object/<N>-<component>.md`** — which objects belong to this component:
- Start with the aggregate or top-level object
- Narrow to properties, behaviors, relationships, and invariants
- Mermaid diagrams for object relationships

For all Mermaid diagrams: use `<br/>` for multi-line node labels, not `\n`.

Each file describes what **is**, not what **was decided**. Write in present tense.

Example (checkout component):
- `value/02-checkout.md`: "Users can complete a purchase. → Guest checkout is supported. → Items must never be silently dropped."
- `aspect/02-checkout.md`: "Checkout is a linear flow. → Each step validates before advancing. → Payment step retries on transient failure."
- `object/02-checkout.md`: "`Order` owns `LineItem[]`. → `LineItem` holds quantity and price snapshot. → Once `confirmed`, items cannot be removed."

---

## Step 4: Update indexes and SUMMARY.md

- Update each layer's `index.md` component list (`value/index.md`, `aspect/index.md`, `object/index.md`)
- Update `docs/index.md` if the layer directories are new
- Add entries to `.pf/src/SUMMARY.md`

Then build:

```bash
cd .pf && mdbook build 2>&1
```

Fix all errors before reporting to the user.

---

## Step 5: Done

Show the user which files were created or updated. Suggest a commit message using `../pf/references/commit.md`.

