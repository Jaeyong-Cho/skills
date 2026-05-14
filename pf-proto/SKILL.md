---
name: pf-proto
description: |
  Build a throwaway prototype to validate a design question, then write a Proof of Concept (PoC) document. Use when the user wants to explore or validate a design before committing to an ADR.
  Triggers: "pf-proto", "prototype this", "let's prototype", "explore this idea", "validate this design", "I want to try something before deciding".
---

Read `../pf/references/caveman.md` and apply caveman style throughout — including in all output documents.

# VAO Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

PoC documents are stored at `.pf/src/poc/<ID>-<slug>.md`.

Assign ID with:
```bash
ls .pf/src/poc/*.md 2>/dev/null | wc -l
```
Zero-padded 4-digit format: `0001`, `0002`, etc.

---

## Step 1: Sharpen the question (interactive)

If the user provided a scenario with the command, use it as the starting material. Do not ask the user to write the question themselves. Instead, lead an interactive narrowing:

1. **Draft a question** from the user's scenario — propose it out loud
2. **Ask one thing** to make it sharper: scope, assumption, success condition
3. **Revise** based on the answer — repeat until the question is crisp and testable

A good question is specific enough that a prototype can answer it with a yes/no or a clear winner:
- "Does this cart state model handle concurrent modifications correctly?"
- "Which of these three checkout layouts do users find clearest?"
- "Can we derive the invoice total from order events alone, without storing it?"

**One PoC = one question.** If the question still covers multiple independent unknowns after narrowing, propose splitting into separate PoCs.

Once agreed, determine the prototype type:
- **Logic question** (state transitions, business rules, data shape) → read `references/proto-logic.md`
- **UI question** (layout, interaction, design direction) → read `references/proto-ui.md`

---

## Step 2: Build the prototype

1. **Throwaway from day one, clearly marked as such.** All prototype code lives in `proto/<slug>/` at the project root — never next to production modules. This keeps throwaway code isolated and easy to delete wholesale.
2. **One command to run.** Whatever the project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, etc. The user must be able to start it without thinking.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is checking, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype runnable, no abstractions. The point is to learn something fast and then delete it.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Delete or absorb when done.** When the prototype has answered its question, either delete it or fold the validated decision into the real code — don't leave it rotting in the repo.

---

## Step 3: Write the PoC document

Read `references/poc-template.md` for the document structure.

Write `.pf/src/poc/<ID>-<slug>.md` with sections: What was built, Findings, Architecture (fill the VAO layers — value, aspect, object — from the prototype findings), User feedback (leave blank for now), Decisions, Open questions, Out of scope.

Add to `.pf/src/SUMMARY.md`:
```markdown
  - [[<ID>] <title>](./poc/<ID>-<slug>.md)
```

Use Mermaid diagrams wherever a visual makes findings clearer — state transitions, data flow, before/after comparisons. Keep each diagram focused on one context. Use `<br/>` for multi-line node labels, not `\n`.

Show the document to the user, then ask: **what did you observe while running it?** — reactions, surprises, things that felt wrong, anything that didn't match expectations.

Update the User feedback section verbatim based on the response. Do not paraphrase.

---

## Step 4: Interview

Run the `grill-me` skill. Cover what worked, what didn't, what was surprising, what felt wrong, and any open concerns. As the interview surfaces new information, update the PoC document:

- **User feedback** — capture interview responses verbatim, not paraphrased
- **Findings / Architecture / Open questions** — update if the interview changes or adds to them

---

## Step 5: Hand off to pf

Suggest a commit message using `../pf/references/commit.md`.

Then tell the user:

> "PoC written at `.pf/src/poc/<ID>-<slug>.md`. Use `/pf` to turn this into an ADR — the Architecture sketch and PoC findings will be the starting context for grill-me."

