---
name: grill-me
description: Personal grilling engine — interview the user one question at a time from a design-tree frontier; when they can't answer, drop into progressive-disclosure clarification before returning to the question. Invoke as /grill-me, or via dev-grill-me / refact-grill-me's checklists.
disable-model-invocation: true
---

# Grill Me

**One question per message. Always.** A caller's checklist (e.g.
`dev-grill-me`'s list of topics) is the backlog to eventually cover, not a
batch to ask together — surface it one item at a time regardless of how
many items the checklist has.

## Design tree

Map the topic as a design tree: every decision branches into the decisions
that hang off it. The **frontier** is every decision whose prerequisites are
already settled — answerable now, without guessing at answers not yet heard.
Build this silently; do not narrate the tree or list its branches to the
user.

## Facts vs decisions

Finding facts is your job, never the user's. Dispatch a sub-agent for
anything findable in the environment (filesystem, tools, code). Only
genuine decisions go to the user.

## Ask one

From the frontier, pick the single question that unblocks the most other
questions. Your reply contains exactly one `❓` block — never `Q1`/`Q2`,
never a numbered list, never two questions stacked in one message:

```
❓ **Q** - <title>: <body>

➡️ <recommended answer>
```

End your turn immediately after the recommended answer. Do not draft or
preview the next question in the same reply. Wait for the user's reply.

## When the user can't answer

If the reply isn't an answer to Q — a question back, "I don't know", "not
sure" — answer it first, in layers:

- L0: core answer, 1-2 sentences
- L1: key reasoning, only if they push further
- L2: examples/edge cases, only if explicitly requested

When the user can answer, re-ask the same Q, unchanged — still one question,
one message.

## Next question

An answer can settle prerequisites for other branches — recompute the
frontier silently, then ask the next single question the same way. This is
still one question per message, not a new round of several.

## Done

Frontier empty → confirm shared understanding with the user before anything
acts on it.
