---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Do not implement anything. Keep discussing until the human is explicitly satisfied with the plan.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.
