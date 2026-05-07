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

Read `references/poc-template.md` for the document structure.

Write `.aeo/src/poc/<ID>-<slug>.md` with sections: What was built, Findings, Decisions, Open questions, Out of scope.

Add to `.aeo/src/SUMMARY.md`:
```markdown
  - [[<ID>] <title>](./poc/<ID>-<slug>.md)
```

Use Mermaid diagrams wherever a visual makes findings clearer — state transitions, data flow, before/after comparisons. Keep each diagram focused on one context. Use `<br/>` for multi-line node labels, not `\n`.

---

## Step 4: Hand off to aeo

Once the PoC document is written, tell the user:

> "PoC written at `.aeo/src/poc/<ID>-<slug>.md`. Use `/aeo` to turn this into an ADR — the PoC findings will replace the grill-me step."
