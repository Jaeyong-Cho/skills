---
name: aeo-proto
description: |
  Build a throwaway prototype to validate a design question, then write a Proof of Concept (PoC) document. Use when the user wants to explore or validate a design before committing to an ADR.
  Triggers: "aeo-proto", "prototype this", "let's prototype", "explore this idea", "validate this design", "I want to try something before deciding".
---

# AEO Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

PoC documents are stored at `.aeo/src/poc/<ID>-<slug>.md`.

Assign ID with:
```bash
ls .aeo/src/poc/*.md 2>/dev/null | wc -l
```
Zero-padded 4-digit format: `0001`, `0002`, etc.

---

## Step 1: Identify the question

Ask the user: **what specific question does this prototype need to answer?**

Good prototype questions:
- "Does this cart state model handle concurrent modifications correctly?"
- "Which of these three checkout layouts do users find clearest?"
- "Can we derive the invoice total from order events alone, without storing it?"

The question determines the prototype type:
- **Logic question** (state transitions, business rules, data shape) → read `references/proto-logic.md`
- **UI question** (layout, interaction, design direction) → read `references/proto-ui.md`

---

## Step 2: Build the prototype

1. **Throwaway from day one, and clearly marked as such.** Locate it near where it will be used — name it so a casual reader sees it's a prototype, not production.
2. **One command to run.** Use the project's existing task runner.
3. **No persistence by default.** State lives in memory. If testing persistence, use a scratch DB or local file named "PROTOTYPE — wipe me".
4. **Skip the polish.** No tests, no error handling beyond runnable, no abstractions.
5. **Surface the state.** After every action (logic) or variant switch (UI), show the full relevant state.
6. **Delete when done.** Once findings are written, delete the prototype code.

---

## Step 3: Write the PoC document

Write `.aeo/src/poc/<ID>-<slug>.md`:

```markdown
# [ID] Title

**Date:** YYYY-MM-DD
**Question:** <the specific question this prototype answered>
**Type:** Logic | UI

## What was built

Brief description of the prototype.

## Findings

What the prototype revealed — validated, invalidated, and surprising.

## Decisions

Concrete decisions this prototype enables:
- Interfaces, data shapes, or workflows that are now clear
- Options that were ruled out and why

## Open questions

What remains unresolved — to be explored in the ADR grill-me.

## Out of scope

What was deliberately not tested.
```

Add to `.aeo/src/SUMMARY.md`:
```markdown
  - [[<ID>] <title>](./poc/<ID>-<slug>.md)
```

---

## Mermaid Diagrams

Use Mermaid diagrams in the PoC document wherever a visual makes findings clearer — state transitions, data flow, before/after comparisons, decision trees. A diagram communicates structure faster than prose.

Keep each diagram focused on one context. If it's getting large, split it — one diagram per concern.

For multi-line text inside node labels, use `<br/>` — not `\n`.

```
A["line one<br/>line two"]
```

---

## Step 4: Hand off to aeo

Once the PoC document is written, tell the user:

> "PoC written at `.aeo/src/poc/<ID>-<slug>.md`. Use `/aeo` to turn this into an ADR — the PoC findings will replace the grill-me step."
