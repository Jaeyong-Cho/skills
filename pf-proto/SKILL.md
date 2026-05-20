---
name: pf-proto
description: |
  Build a throwaway prototype to validate a design question, then write a Proof of Concept (PoC) document. Use when the user wants to explore or validate a design before committing to an ADR.
  Triggers: "pf-proto", "prototype this", "let's prototype", "explore this idea", "validate this design", "I want to try something before deciding".
---

Read `../pf/references/caveman.md` and apply caveman style throughout — including in all output documents.

Check for today's journal context:

```bash
[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null
```

If today.md found, read to understand user's current focus, active goals, blockers. Use to orient work — not to override task, but to connect prototype to user's broader context.

# VAO Prototype

Prototype = **throwaway code that answers a question**. Question decides the shape.

PoC documents stored at `.pf/src/poc/<ID>-<slug>.md`.

Assign ID with:
```bash
ls .pf/src/poc/*.md 2>/dev/null | wc -l
```
Zero-padded 4-digit format: `0001`, `0002`, etc.

---

## Step 1: Sharpen the question (interactive)

If user provided scenario with command, use as starting material. Do not ask user to write question themselves. Lead interactive narrowing:

1. **Draft question** from user's scenario — propose it out loud
2. **Ask one thing** to make it sharper: scope, assumption, success condition
3. **Revise** based on answer — repeat until question is crisp and testable

Good question specific enough that prototype can answer it with yes/no or clear winner:
- "Does this cart state model handle concurrent modifications correctly?"
- "Which of these three checkout layouts do users find clearest?"
- "Can we derive invoice total from order events alone, without storing it?"

**One PoC = one question.** If question still covers multiple independent unknowns after narrowing, propose splitting into separate PoCs.

Once agreed, determine prototype type:
- **Logic question** (state transitions, business rules, data shape) → read `references/proto-logic.md`
- **UI question** (layout, interaction, design direction) → read `references/proto-ui.md`

---

## Step 2: Build the prototype

1. **Throwaway from day one, clearly marked as such.** All prototype code lives in `proto/<slug>/` at project root — never next to production modules. Keeps throwaway code isolated and easy to delete wholesale.
2. **One command to run.** Whatever project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, etc. User must be able to start it without thinking.
3. **No persistence by default.** State lives in memory. Persistence is thing prototype is checking, not something it should depend on. If question explicitly involves database, hit scratch DB or local file with clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes prototype runnable, no abstractions. Point is to learn something fast and then delete it.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render full relevant state so user can see what changed.
6. **Delete or absorb when done.** When prototype has answered its question, either delete it or fold validated decision into real code — don't leave it rotting in repo.

---

## Step 3: Write the PoC document

Read `references/poc-template.md` for document structure.

Write `.pf/src/poc/<ID>-<slug>.md` with sections: What was built, Findings, Architecture (fill VAO layers — value, aspect, object — from prototype findings), User feedback (leave blank for now), Decisions, Open questions, Out of scope.

Add to `.pf/src/SUMMARY.md`:
```markdown
  - [[<ID>] <title>](./poc/<ID>-<slug>.md)
```

Use Mermaid diagrams wherever visual makes findings clearer — state transitions, data flow, before/after comparisons. Keep each diagram focused on one context. Use `<br/>` for multi-line node labels, not `\n`.

Show document to user, then ask: **what did you observe while running it?** — reactions, surprises, things that felt wrong, anything that didn't match expectations.

Update User feedback section verbatim based on response. Do not paraphrase.

---

## Step 4: Interview

Run `grill-me` skill. Cover what worked, what didn't, what was surprising, what felt wrong, any open concerns. As interview surfaces new information, update PoC document:

- **User feedback** — capture interview responses verbatim, not paraphrased
- **Findings / Architecture / Open questions** — update if interview changes or adds to them

---

## Step 5: Hand off to pf

Suggest commit message using `../pf/references/commit.md`.

Then tell user:

> "PoC written at `.pf/src/poc/<ID>-<slug>.md`. Use `/pf` to turn this into an ADR — the Architecture sketch and PoC findings will be the starting context for grill-me."
