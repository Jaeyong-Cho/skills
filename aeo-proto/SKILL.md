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

**One PoC = one question.** If the user's question contains multiple independent unknowns, split into separate PoCs. A sign of too-broad scope: answering one part doesn't help decide the other.

Good prototype questions:
- "Does this cart state model handle concurrent modifications correctly?"
- "Which of these three checkout layouts do users find clearest?"
- "Can we derive the invoice total from order events alone, without storing it?"

The question determines the prototype type:
- **Logic question** (state transitions, business rules, data shape) → read `references/proto-logic.md`
- **UI question** (layout, interaction, design direction) → read `references/proto-ui.md`

---

## Step 2: Build the prototype

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious — but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **One command to run.** Whatever the project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, etc. The user must be able to start it without thinking.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is checking, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype runnable, no abstractions. The point is to learn something fast and then delete it.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Delete or absorb when done.** When the prototype has answered its question, either delete it or fold the validated decision into the real code — don't leave it rotting in the repo.

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

> "PoC written at `.aeo/src/poc/<ID>-<slug>.md`. Use `/aeo` to turn this into an ADR — the PoC findings and open questions will be the starting context for grill-me."
