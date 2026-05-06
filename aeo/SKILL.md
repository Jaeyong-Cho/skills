---
name: aeo
description: |
  Apply the AEO (Axiology–Epistemology–Ontology) software architecture philosophy to any engineering task.
  AEO is a three-layer design lens inspired by OOP and AOP: Axiology defines value (why), Epistemology defines method and aspect (how), Ontology defines stable invariant entities (what).
  Use this skill whenever the user says "aeo", "apply aeo", "use aeo philosophy", or asks for design, review, coding, refactoring, or documentation *with AEO in mind*.
  Also trigger when the user asks to analyze or critique an architecture and the AEO framework would help clarify responsibilities and boundaries.
  Even if the user just says "review this" or "design this" in a context where AEO has been mentioned or is the active working philosophy, apply this skill.
---

# AEO Skill

A program is an automation tool for making decisions to achieve a goal. AEO structures this around three layers:

- **Value layer (Why)** — user value: which features are worth building, which results users need, what a good outcome looks like; the entry point that represents user intent in code
- **Method layer (How)** — how to meet the need, and which objects to use and from which angle; the composable algorithm that bridges value and entity
- **Entity layer (What)** — the stable objects that exist to satisfy the need and the method; invariant across aspects

Design direction: **value → method → entity** (iterative in practice).

In all documents, ADRs, and code labels always use `[value]`, `[method]`, `[entity]`.

For layer details including the OOP/AOP origin, object sizing by concern, and aspect thinking, read `references/layers.md`.

---

## Before Doing Anything

Check whether the AEO book exists:

```bash
ls .aeo/book.toml 2>/dev/null
```

If it does **not** exist: read `references/init.md` and initialize the book first, then proceed.

---

## Workflow

Every task follows this sequence:

1. **Write an ADR** — read `references/adr.md`. All decisions (new feature, refactoring, architecture change) are ADRs. Ask the user to confirm before writing any code.
2. **Implement** — write code according to the step-by-step plan in the ADR.
3. **Code review confirmed** — update the software manual. Read `references/docs.md`.

For AEO layer details, read `references/layers.md`.

## Mermaid Diagrams

Use Mermaid diagrams anywhere a visual explanation is clearer than prose — layer relationships, aspect interactions, data flow, before/after refactoring, entity relationships, decision logic, anything. A diagram communicates structure faster than prose and is the primary way AEO outputs make architecture visible. Place diagrams wherever they help, use as many as needed, and never restrict them to specific sections.

Keep each diagram focused on one context. If a diagram is getting large, split it — one diagram per concern is more readable than one diagram trying to show everything. A diagram that needs scrolling or squinting has already failed its purpose.

For multi-line text inside node labels, use `<br/>` — not `\n`. `\n` does not render in Mermaid node labels.

```
A["line one<br/>line two"]
```

After finishing, build the book:

```bash
cd .aeo && mdbook build 2>&1
```

Fix all errors before reporting to the user.

## Commit Message

After each session, show the user a recommended commit message in this format:

```
<type>(aeo): <short description>

Why: <what value or goal this addresses>
What: <what entities or artifacts were created or changed>
How: <what method or approach was applied>
```

Where `<type>` is one of: `feat` (new design/impl/review/docs), `refact` (refactoring plan), `fix` (correction to existing content). The subject line should name the specific artifact produced (e.g. `add design 0001 auth-flow`, `add review 0003 payment-service`).
