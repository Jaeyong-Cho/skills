---
name: aeo
description: |
  Apply the AEO (Axiology–Epistemology–Ontology) software architecture philosophy to any engineering task.
  AEO is a three-layer design lens inspired by OOP and AOP: Axiology defines user value (why), Epistemology defines method and aspect (how), Ontology defines stable domain entities (what).
  Use this skill whenever the user says "aeo", "apply aeo", "use aeo philosophy", or asks for design, review, coding, refactoring, or documentation *with AEO in mind*.
  Also trigger when the user asks to analyze or critique an architecture and the AEO framework would help clarify responsibilities and boundaries.
  Even if the user just says "review this" or "design this" in a context where AEO has been mentioned or is the active working philosophy, apply this skill.
---

# AEO Skill

A program is an automation tool for making decisions to achieve a goal. AEO structures this around three layers:

- **Axiology (Why)** — user value: which features are worth building, which results users need, what a good outcome looks like; the entry point that represents user intent in code
- **Epistemology (How)** — how to meet the need, and which objects to use and from which angle; the composable algorithm that bridges value and entity
- **Ontology (What)** — the stable objects that exist to satisfy the need and the method; invariant across aspects

Design direction: **Axiology → Epistemology → Ontology** (iterative in practice).

In output documents, ADRs, and code labels use plain terms: `[value]`, `[method]`, `[entity]` instead of the philosophical names.

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

```
[uncertain about design?]
        ↓
   aeo-proto  ──→  ADR (created or updated)
                        ↓
[clear on what to build]
        ↓
      aeo    ──→  ADR (written + confirmed)
                        ↓
                   aeo-impl  ──→  TDD implementation
                                        ↓
                              code review confirmed
                                        ↓
                               update documentation
```

1. **Prototype first (optional)** — if the design question is unresolved, use the `aeo-proto` skill. It builds a throwaway prototype and writes a PoC document at `.aeo/src/poc/<ID>-<slug>.md`.
2. **Write an ADR** — read `references/adr.md`. If coming from `aeo-proto`, read the PoC document first — it replaces the grill-me step. Ask the user to confirm before writing any code.
3. **Implement with TDD** — use the `aeo-impl` skill. It reads the confirmed ADR and implements one behavior at a time: RED → GREEN → REFACTOR.
4. **Code review confirmed** — update the documentation. Read `references/docs.md`.

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

After each session, suggest a commit message. Read `references/commit.md` for the format and examples.
