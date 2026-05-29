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
Check journal: `[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null` — use to orient work to user's current focus and goals.
Check VAO book: `ls .pf/book.toml 2>/dev/null` — not found → run `pf-init` first, then proceed.

# VAO Skill

Program = automation tool for making decisions to achieve goal. VAO structures this around three layers:

- **Value (Why)** — user value: which features worth building, which results users need, what good outcome looks like; entry point representing user intent in code
- **Aspect (How)** — how to meet need, which objects to use and from which angle; composable algorithm bridging value and object
- **Object (What)** — stable objects that exist to satisfy need and aspect; invariant across aspects

Design direction: **Value → Aspect → Object** (iterative in practice).

In output documents, ADRs, and code labels use plain terms: `[value]`, `[aspect]`, `[object]` instead of philosophical names.

For layer details including OOP/AOP origin, object sizing by concern, and aspect thinking, read `references/layers.md`.

## Write an ADR

Read `references/deep-modules.md`, `references/layers.md`, `references/adr.md`, `references/views.md`.

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: reach a clear VAO design for the ADR. Starting context: the user's scenario, or PoC findings if coming from `pf-proto`.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

When referencing existing source code, cite exact `file:line`.

## Mermaid Diagrams

Use Mermaid diagrams anywhere visual explanation clearer than prose — layer relationships, aspect interactions, data flow, before/after refactoring, entity relationships, decision logic. Diagram communicates structure faster than prose; use as many as needed.

Keep each diagram focused on one context. Split large diagrams — one per concern is more readable. For multi-line text in node labels use `<br/>` not `\n`:

```
A["line one<br/>line two"]
```

After finishing, build: `cd .pf && mdbook build 2>&1` — fix all errors before reporting.

## Commit Message

Suggest commit message after each session. Read `references/commit.md` for format.
