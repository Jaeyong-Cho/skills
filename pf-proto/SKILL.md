---
name: pf-proto
description: |
  Build a throwaway prototype to validate a design question, then write a Proof of Concept (PoC) document. Use when the user wants to explore or validate a design before committing to an ADR.
  Triggers: "pf-proto", "prototype this", "let's prototype", "explore this idea", "validate this design", "I want to try something before deciding".
---


# VAO Prototype

Prototype = **throwaway code that answers a question**. Question decides the shape.

PoC documents stored at `.pf/src/poc/<ID>-<slug>.md`. Assign ID: `ls .pf/src/poc/*.md 2>/dev/null | wc -l` — zero-padded 4-digit: `0001`, `0002`, etc.

## Step 1: Sharpen the question (interactive)

Use user's scenario as starting material. Lead interactive narrowing:
1. **Draft question** from scenario — propose it out loud
2. **Ask one thing** to make it sharper: scope, assumption, success condition
3. **Revise** based on answer — repeat until crisp and testable

Good question specific enough to answer with yes/no or clear winner:
- "Does this cart state model handle concurrent modifications correctly?"
- "Can we derive invoice total from order events alone, without storing it?"

**One PoC = one question.** If question covers multiple independent unknowns, propose splitting.

Once agreed, determine prototype type:
- **Logic question** (state, business rules, data shape) → read `references/proto-logic.md`
- **UI question** (layout, interaction, direction) → read `references/proto-ui.md`

## Step 2: Build the prototype

1. **Throwaway from day one.** Code lives in `proto/<slug>/` at project root — never next to production modules.
2. **One command to run.** Whatever task runner the project uses — user must start it without thinking.
3. **No persistence by default.** State in memory. If question involves DB, use scratch DB with "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond runnable, no abstractions. Learn fast, delete after.
5. **Surface the state.** After every action or variant switch, print or render full relevant state.
6. **Delete or absorb when done.** Answer the question, then delete or fold decision into real code.

## Step 3: Write the PoC document

Read `references/poc-template.md` for structure.

Write `.pf/src/poc/<ID>-<slug>.md`: What was built, Findings, Architecture (VAO layers from prototype findings), User feedback (blank for now), Decisions, Open questions, Out of scope.

Add to `.pf/src/SUMMARY.md`:
```markdown
  - [[<ID>] <title>](./poc/<ID>-<slug>.md)
```

Use Mermaid diagrams where visual makes findings clearer. Use `<br/>` for multi-line node labels, not `\n`.

Show document to user, then ask: **what did you observe while running it?** — reactions, surprises, anything that didn't match expectations. Update User feedback verbatim — do not paraphrase.

## Step 4: Interview

Run `grill-me` skill. Cover what worked, what didn't, surprises, open concerns. Update PoC as interview surfaces new information — User feedback verbatim, Findings/Architecture/Open questions if they change.

## Step 5: Hand off to pf

Suggest commit message using `../pf/references/commit.md`.

Tell user: "PoC at `.pf/src/poc/<ID>-<slug>.md`. Use `/pf` to turn into ADR — Architecture sketch and PoC findings will be starting context for grill-me."
