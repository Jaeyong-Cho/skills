---
name: grill-me
description: Personal grilling engine — interview the user round by round over a design-tree frontier; any question the user can't answer gets progressive-disclosure clarification before being re-asked. Invoke as /grill-me, or via dev-grill-me / refact-grill-me's checklists.
disable-model-invocation: false
---

# Grill Me

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The _decisions_ are the user's — put each to them and wait.

## When the user can't answer one

If the reply to a given Qn isn't an answer — a question back, "I don't
know", "not sure" — answer that one first, in layers, before moving on to
the rest of the round's replies with `/progressive` skill:

- L0: core answer, 1-2 sentences
- L1: key reasoning, only if they push further
- L2: examples/edge cases, only if explicitly requested

Re-ask that Qn, unchanged, in the next round alongside whatever else the
frontier opens up. Don't let one unanswered question block recording the
round's other answers.

## Next round

Each round's answers reshape the tree — settled decisions push the frontier
outward and unblock questions that depended on them. Recompute the frontier
and ask the next round.

## Done

The session is done when the frontier is empty: every branch of the design
tree visited, nothing left silently assumed. Do not act on it until the
user confirms shared understanding.
