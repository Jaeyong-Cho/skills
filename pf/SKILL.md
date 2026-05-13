---
name: pf
description: |
  Apply the VAO (Value–Aspect–Object) software architecture philosophy to any engineering task.
  VAO is a three-layer design lens inspired by OOP and AOP: Value defines user value (why), Aspect defines aspect (how), Object defines stable domain objects (what).
  Use this skill whenever the user says "pf", "apply pf", "use pf philosophy", or asks for design, review, coding, refactoring, or documentation *with VAO in mind*.
  Also trigger when the user asks to analyze or critique an architecture and the VAO framework would help clarify responsibilities and boundaries.
  Even if the user just says "review this" or "design this" in a context where pf has been mentioned or is the active working philosophy, apply this skill.
---

> Use `/caveman` for compressed output during this session.

# VAO Skill

A program is an automation tool for making decisions to achieve a goal. VAO structures this around three layers:

- **Value (Why)** — user value: which features are worth building, which results users need, what a good outcome looks like; the entry point that represents user intent in code
- **Aspect (How)** — how to meet the need, and which objects to use and from which angle; the composable algorithm that bridges value and object
- **Object (What)** — the stable objects that exist to satisfy the need and the aspect; invariant across aspects

Design direction: **Value → Aspect → Object** (iterative in practice).

In output documents, ADRs, and code labels use plain terms: `[value]`, `[aspect]`, `[object]` instead of the philosophical names.

For layer details including the OOP/AOP origin, object sizing by concern, and aspect thinking, read `references/layers.md`.

---

## Before Doing Anything

Check whether the VAO book exists:

```bash
ls .pf/book.toml 2>/dev/null
```

If it does **not** exist: use the `pf-init` skill to initialize the book first, then proceed.

---

## Workflow

```
[uncertain about design?]
        ↓
   pf-proto  ──→  PoC document
                        ↓
[clear on what to build]
        ↓
      pf  ──→  ADR (written + confirmed)
                        ↓
                   pf-impl  ──→  TDD implementation
                                        ↓
                              code review confirmed
                                        ↓
                               pf-docs  ──→  documentation updated
```

1. **Prototype first (optional)** — if the design question is unresolved, use the `pf-proto` skill. It builds a throwaway prototype and writes a PoC document at `.pf/src/poc/<ID>-<slug>.md`.
2. **Write an ADR** — read `references/deep-modules.md` and `references/adr.md`. Run the `grill-me` skill. If the user provided a scenario with the command, use it as the starting context. If coming from `pf-proto`, read the PoC document first and use its findings and open questions as the starting context instead. Ask the user to confirm before writing any code.
3. **Implement with TDD** — use the `pf-impl` skill. It reads the confirmed ADR and implements one behavior at a time: RED → GREEN → REFACTOR.
4. **Code review confirmed** — use the `pf-docs` skill to update the documentation.

For VAO layer details, read `references/layers.md`.

## Mermaid Diagrams

Use Mermaid diagrams anywhere a visual explanation is clearer than prose — layer relationships, aspect interactions, data flow, before/after refactoring, entity relationships, decision logic, anything. A diagram communicates structure faster than prose and is the primary way VAO outputs make architecture visible. Place diagrams wherever they help, use as many as needed, and never restrict them to specific sections.

Keep each diagram focused on one context. If a diagram is getting large, split it — one diagram per concern is more readable than one diagram trying to show everything. A diagram that needs scrolling or squinting has already failed its purpose.

For multi-line text inside node labels, use `<br/>` — not `\n`. `\n` does not render in Mermaid node labels.

```
A["line one<br/>line two"]
```

After finishing, build the book:

```bash
cd .pf && mdbook build 2>&1
```

Fix all errors before reporting to the user.

## Commit Message

After each session, suggest a commit message. Read `references/commit.md` for the format and examples.

