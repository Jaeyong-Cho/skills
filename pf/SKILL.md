---
name: pf
description: |
  Apply the VAO (Value–Aspect–Object) software architecture philosophy to any engineering task.
  VAO is a three-layer design lens inspired by OOP and AOP: Value defines user value (why), Aspect defines aspect (how), Object defines stable domain objects (what).
  Use this skill whenever the user says "pf", "apply pf", "use pf philosophy", or asks for design, review, coding, refactoring, or documentation *with VAO in mind*.
  Also trigger when the user asks to analyze or critique an architecture and the VAO framework would help clarify responsibilities and boundaries.
  Even if the user just says "review this" or "design this" in a context where pf has been mentioned or is the active working philosophy, apply this skill.
---

Read `references/caveman.md` and apply caveman style throughout — including in all output documents.

# VAO Skill

Program = automation tool for making decisions to achieve goal. VAO structures this around three layers:

- **Value (Why)** — user value: which features worth building, which results users need, what good outcome looks like; entry point representing user intent in code
- **Aspect (How)** — how to meet need, which objects to use and from which angle; composable algorithm bridging value and object
- **Object (What)** — stable objects that exist to satisfy need and aspect; invariant across aspects

Design direction: **Value → Aspect → Object** (iterative in practice).

In output documents, ADRs, and code labels use plain terms: `[value]`, `[aspect]`, `[object]` instead of philosophical names.

For layer details including OOP/AOP origin, object sizing by concern, and aspect thinking, read `references/layers.md`.

---

## Before Doing Anything

Check for today's journal context:

```bash
[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null
```

If today.md found, read it to understand user's current focus, active goals, any blockers. Use to orient work — not to override task, but to connect design to user's broader context.

Check whether VAO book exists:

```bash
ls .pf/book.toml 2>/dev/null
```

If does **not** exist: use `pf-init` skill to initialize book first, then proceed.

---

## Write an ADR

Read `references/deep-modules.md`, `references/aop.md`, `references/adr.md`, `references/views.md`. Run `grill-me` skill. If user provided scenario, use as starting context. If coming from `pf-proto`, read PoC document first and use its findings as starting context instead.

When referencing existing source code, always cite exact `file:line` so user can navigate directly.

## Mermaid Diagrams

Use Mermaid diagrams anywhere visual explanation clearer than prose — layer relationships, aspect interactions, data flow, before/after refactoring, entity relationships, decision logic, anything. Diagram communicates structure faster than prose and is primary way VAO outputs make architecture visible. Place diagrams wherever they help, use as many as needed.

Keep each diagram focused on one context. If diagram getting large, split it — one diagram per concern more readable than one covering everything. Diagram that needs scrolling or squinting has already failed.

For multi-line text inside node labels, use `<br/>` — not `\n`. `\n` does not render in Mermaid node labels.

```
A["line one<br/>line two"]
```

After finishing, build the book:

```bash
cd .pf && mdbook build 2>&1
```

Fix all errors before reporting to user.

## Commit Message

After each session, suggest commit message. Read `references/commit.md` for format and examples.
