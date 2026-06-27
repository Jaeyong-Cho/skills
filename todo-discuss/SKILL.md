---
name: todo-discuss
description: Discuss what to do next, decompose complex tasks, and structure todos — then optionally write the result back to TODO.md. Use when user says "what should I do next", "help me plan", "decompose this task", "todo-discuss", "how do I break this down", or invokes /todo-discuss.
---

# Todo Discuss

If `source-of-truth/` exists in the project root, read all files in it. Also read `TODO.md` in the current project root if it exists.

Interview the user relentlessly about their tasks until every item is clear, prioritized, and decomposed into concrete steps. Walk down each branch of the task tree, resolving dependencies one-by-one. For each question, provide your recommended answer.

## What to resolve

**Priority** — what to tackle next given the current state
- If `TODO.md` exists, start there: "Which of these is most important right now?"
- Surface what's blocked, what's urgent, what has dependencies

**Decomposition** — break vague or large tasks into small concrete steps
- Keep asking "what's the first concrete action?" until each step fits in one sitting
- Each final step must be: specific, actionable, independently completable

**Dependencies** — make ordering explicit
- If B can't start until A is done, say so
- Identify what's parallelizable vs. sequential

## How to ask

Ask one question at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list options with your recommended one marked "(Recommended)". For open-ended questions, ask in plain text.

There is no maximum number of questions. Keep going until every task is decomposed and the order is clear. The user can say "wrap up" at any time to get a structured summary and move on.

## Output

When discussion reaches clarity, present the proposed todo list then run `/to-todo` to write it to `TODO.md`.
