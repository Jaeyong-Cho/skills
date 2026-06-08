---
name: pf-proto
description: |
  Build a throwaway single-file CLI tool to prove a concept or answer a design question fast. Grills the user to isolate the question, then writes the smallest possible runnable proof — no tests, no abstractions, no polish.
  Use when the user wants to sanity-check a data model, state machine, algorithm, or API shape before committing. Triggers: "pf-proto", "prototype this", "prove this works", "quick proof", "sanity check this", "try this out", "let me play with it", "proof of concept".
---

# Prototype

A prototype is **throwaway code that answers one question**. The question decides everything.

## Step 1: Grill

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: isolate the exact question the prototype must answer — no more, no less.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

## Step 2: State the question

Write the question in one sentence at the top of the prototype file as a comment:

```
# PROTOTYPE — Does X state model handle the case where Y then Z?
# Delete or absorb when answered.
```

If the question can't be stated in one sentence, the scope is too broad — go back and narrow it.

## Step 3: Build

**One file. One entry point. One command to run.**

- Use the project's language and tooling — don't add a new runtime or package manager
- Separate pure logic from the CLI shell: logic in a function/class that could be lifted into real code later; shell just calls it and prints output
- No tests, no error handling beyond what makes it runnable, no abstractions
- No persistence unless the question is specifically about persistence
- Surface state fully after every action — print the whole relevant state, not just what changed
- Mark it clearly as a prototype (`PROTOTYPE` in the filename or path)

Add a run command to the project's existing task runner, or put the command in a comment at the top of the file.

## Step 4: Run and verify

Run the prototype. Drive it through the cases that motivated the question — especially the edge cases that were hard to reason about on paper. If it exposes a flaw in the idea, that's success.

## Step 5: Capture the answer

State what the prototype proved or disproved. Write it as a one-paragraph finding:

```
# Answer: X state model works for Y and Z, but breaks when W.
# Decision: use approach A instead.
```

Save this to a `NOTES.md` next to the prototype, a commit message, or an ADR — somewhere durable. Then either delete the prototype or fold the validated logic into the real code. Don't leave it rotting.
