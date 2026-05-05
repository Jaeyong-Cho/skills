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

- **Axiology (Why)** — what goal is worth automating; values, evaluation, validation, selection
- **Epistemology (How)** — the algorithm and aspect through which objects are used to realize the value
- **Ontology (What)** — stable, invariant entities; their properties, behaviors, and relationships

Design direction: **Axiology → Epistemology → Ontology** (iterative in practice).

For layer details including the OOP/AOP origin, object sizing by concern, and aspect thinking, read `references/layers.md`.

---

## Before Doing Anything

Check whether the AEO book exists:

```bash
ls .aeo/book.toml 2>/dev/null
```

If it does **not** exist: read `references/init.md` and initialize the book first, then proceed.

---

## What to Read for Each Task

| Task | Reference file |
|------|---------------|
| Design / Architecture | `references/design.md` |
| Implementation | `references/impl.md` |
| Code Review | `references/review.md` |
| Refactoring | `references/impl.md` |
| Documentation | `references/docs.md` |
| AEO layer details | `references/layers.md` |

Read only the file(s) relevant to the current task.

## Mermaid Diagrams

Use Mermaid diagrams anywhere a visual explanation is clearer than prose — layer relationships, aspect interactions, data flow, before/after refactoring, entity relationships, decision logic, anything. A diagram communicates structure faster than prose and is the primary way AEO outputs make architecture visible. Place diagrams wherever they help, use as many as needed, and never restrict them to specific sections.

After finishing, build the book:

```bash
cd .aeo && mdbook build 2>&1
```

Fix all errors before reporting to the user.
