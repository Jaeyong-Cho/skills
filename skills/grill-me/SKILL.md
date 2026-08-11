---
name: grill-me
description: Personal grilling engine — interview the user one question at a time from a design-tree frontier; when they can't answer, drop into progressive-disclosure clarification before returning to the question. Invoke as /grill-me, or via dev-grill-me / refact-grill-me's checklists.
disable-model-invocation: true
---

# Grill Me

Interview the user until shared understanding, one question at a time — never a batch.

## Design tree

Map the topic as a design tree: every decision branches into the decisions
that hang off it. The **frontier** is every decision whose prerequisites are
already settled — answerable now, without guessing at answers not yet heard.

## Facts vs decisions

Finding facts is your job, never the user's. Dispatch a sub-agent for
anything findable in the environment (filesystem, tools, code). Only
genuine decisions go to the user.

## Ask one

From the frontier, pick the single question that unblocks the most other
questions. Ask only that one:

```
❓ **Q** - <title>: <body>

➡️ <recommended answer>
```

Wait for the reply. Never queue a second question alongside it.

## When the user can't answer

If the reply isn't an answer to Q — a question back, "I don't know", "not
sure" — answer it first, in layers:

- L0: core answer, 1-2 sentences
- L1: key reasoning, only if they push further
- L2: examples/edge cases, only if explicitly requested

Then re-ask the same Q, unchanged.

## Next round

An answer can settle prerequisites for other branches — recompute the
frontier, then ask the next single question the same way.

## Done

Frontier empty → confirm shared understanding with the user before anything
acts on it.
