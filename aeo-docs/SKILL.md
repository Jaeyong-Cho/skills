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

Write from high-level to detailed — value first, then method, then entity.

**01-value.md** — What is valuable about this feature:
- The user need it serves
- What success looks like
- What must never happen (invariants from the user's perspective)

**02-method.md** — How it works:
- Workflows and decision logic
- Composable strategies and entry points
- Mermaid diagrams for flows and interactions

**03-entity.md** — Which objects are used:
- Entities, their properties and behaviors
- Relationships and aggregate boundaries
- Mermaid diagrams for entity relationships

Each section describes what **is**, not what **was decided**. Write in present tense.

Example (checkout feature):
- `01-value.md`: "Users can complete a purchase without creating an account. Guest checkout must never silently drop items from the cart."
- `02-method.md`: "The checkout flow is a linear state machine: cart → address → payment → confirmation. Each step validates before advancing."
- `03-entity.md`: "`Order` owns `LineItem[]` and holds a `status` invariant — once `confirmed`, items cannot be removed."

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
