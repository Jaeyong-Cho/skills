---
name: aeo-docs
description: |
  Write or update the AEO project documentation after an ADR is implemented. Documents the current state of the system — what is valuable, how it works, which objects are used — organized from high-level to detailed.
  Triggers: "aeo-docs", "update the docs", "write documentation", "document this", after code review is confirmed and an ADR exists.
---

# AEO Documentation

Documentation describes the **current state of the system**, not the history of decisions (that is what ADRs are for). Update after code review is confirmed — never before.

Read `../aeo/references/docs.md` for the full structure, file templates, and SUMMARY.md format.

---

## Step 1: Identify the ADR

If the user names an ADR (e.g. "adr-001", "0001", "auth-flow"), find it:

```bash
ls .aeo/src/adr/ | grep 0001
```

If no ADR is specified, list available ADRs and ask which one to document.

Read the ADR. Focus on: what was actually built, the user stories, and the entities involved.

---

## Step 2: Determine scope

Check what already exists:

```bash
ls .aeo/src/docs/
```

Decide:
- **New chapter** — this ADR introduces a topic not yet documented
- **Update existing chapter** — this ADR changes or extends an existing topic

If updating, read the existing section files first so you don't overwrite content that is still accurate.

---

## Step 3: Write the documentation

The three sections (`value`, `method`, `entity`) are written in parallel — each covers the same feature from a different angle. Within **each section**, order content from broad scope to narrow: start with the overall picture, then zoom into specifics.

**01-value.md** — What is valuable:
- Start with the broad user goal this feature serves
- Then narrow to specific success criteria and edge-case constraints

**02-method.md** — How it works:
- Start with the overall workflow or entry point
- Then narrow to specific decision logic, strategies, and flows
- Mermaid diagrams for flows and interactions

**03-entity.md** — Which objects are used:
- Start with the aggregate or top-level entity
- Then narrow to properties, behaviors, relationships, and invariants
- Mermaid diagrams for entity relationships

For all Mermaid diagrams: use `<br/>` for multi-line node labels, not `\n`.

Each section describes what **is**, not what **was decided**. Write in present tense.

Example (checkout feature, narrow-down order within each section):
- `01-value.md`: "Users can complete a purchase. → Guest checkout is supported. → Items must never be silently dropped."
- `02-method.md`: "Checkout is a linear flow. → Each step validates before advancing. → Payment step retries on transient failure."
- `03-entity.md`: "`Order` owns `LineItem[]`. → `LineItem` holds quantity and price snapshot. → Once `confirmed`, items cannot be removed."

---

## Step 4: Update index and SUMMARY.md

- Update or create the chapter `index.md`
- Update `docs/index.md` chapter list if this is a new chapter
- Add entries to `.aeo/src/SUMMARY.md`

Then build:

```bash
cd .aeo && mdbook build 2>&1
```

Fix all errors before reporting to the user.

---

## Step 5: Done

Show the user which files were created or updated. Suggest a commit message using `../aeo/references/commit.md`.
