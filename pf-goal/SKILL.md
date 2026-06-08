---
name: pf-goal
description: |
  Grill the user to clarify a goal, then write a single goal.md file under docs/<id>-<slug>/goal.md. Goals are end-to-end: given a concrete input, the system should produce a specific output.
  Use when the user wants to define, write, or specify a goal. Triggers: "pf-goal", "define a goal", "write a goal", "specify goal", "new goal", "create goal".
---

# Goal

A goal is end-to-end: given a concrete input, the system produces a specific output. Not "improve the internals" — a real, evaluatable outcome.

When writing markdown: using Mermaid diagrams is recommended.

## Step 1: Read existing goals

```bash
ls docs/ 2>/dev/null
```

Show existing goals (id-slug, one-line description) so the user can see what's already defined.

## Step 2: Grill

Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: reach a concrete, evaluatable goal with clear input and expected output.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

Goal scoping rules:
- Too broad: "make the system better" — no clear convergence
- Too narrow: "fix one line" — not worth a goal
- Right: evaluatable, converges toward a clear output

## Step 3: Write goal.md

Assign `id` = count of existing `docs/` directories + 1 (zero-padded to 4 digits: `0001`, `0002`, …). Derive slug from the goal name (lowercase, hyphens, max 30 chars).

```bash
mkdir -p docs/<id>-<slug>
```

Write `docs/<id>-<slug>/goal.md`:

```markdown
# <Goal name>

## Description
<what we're trying to achieve>

## Input
<concrete, reproducible input>

## Expected output
<what should come out>

## History
- YYYY-MM-DD: created
```

## Step 4: Confirm

Show the written file path and content. Ask the user to confirm or adjust.
