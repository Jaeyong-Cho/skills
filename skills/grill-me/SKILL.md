---
name: grill-me
description: Personal grilling engine — interview the user round by round over a design-tree frontier; any question the user can't answer gets progressive-disclosure clarification before being re-asked. Invoke as /grill-me, or via dev-grill-me / refact-grill-me's checklists.
disable-model-invocation: true
---

# Grill Me

Interview the user until shared understanding. Work the design tree in
rounds — a round is every frontier question asked together in one message.

## Design tree

Map the topic as a design tree: every decision branches into the decisions
that hang off it. The **frontier** is every decision whose prerequisites are
already settled — answerable now, without guessing at answers not yet heard.

## Facts vs decisions

Finding facts is your job, never the user's. Dispatch a sub-agent for
anything findable in the environment (filesystem, tools, code). Only
genuine decisions go to the user.

## Ask the round

Ask the whole frontier in one round: number each question and give your
recommended answer.

**MUST NOT** use ask question tool. 

```
❓ **Q1** - <title>: <body>

➡️ <recommended answer>

❓ **Q2** - <title>: <body>

➡️ <recommended answer>
```

Wait for the user's reply before the next round. A question whose answer
depends on another question still open this round belongs to a later round,
not this one.

## When the user can't answer one

If the reply to a given Qn isn't an answer — a question back, "I don't
know", "not sure" — answer that one first, in layers, before moving on to
the rest of the round's replies:

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
