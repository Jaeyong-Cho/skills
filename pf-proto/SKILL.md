---
name: pf-proto
description: |
  Build a throwaway prototype to prove a concept or answer a design question fast. Routes between two branches — a CLI/terminal app for logic and state questions, or UI variations for layout and design questions. Grills the user to isolate the question, then builds the smallest possible runnable proof — no tests, no abstractions, no polish.
  Use when the user wants to sanity-check a data model, state machine, algorithm, API shape, or UI layout before committing. Triggers: "pf-proto", "prototype this", "prove this works", "quick proof", "sanity check this", "try this out", "let me play with it", "proof of concept", "mock up this UI".
---

# Prototype

A prototype is **throwaway code that answers one question**. The question decides the shape.

## Step 1: Grill

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: isolate the exact question the prototype must answer — no more, no less.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

## Step 2: Pick a branch

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that pushes the model through cases that are hard to reason about on paper.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL param and a floating bottom bar.

If ambiguous and the user isn't reachable, default to whichever fits the surrounding code (backend module → logic; page or component → UI) and state the assumption.
