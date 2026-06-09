---
name: split-goal
description: Decompose a big goal top-down into atomic sub-goals, grilling the user to clarify scope and constraints first, then writes the result to a markdown file. Splits recursively until each leaf is a single actionable task. Use when user says "split-goal", "break this down", "decompose this goal", "split into sub-goals", or "top-down breakdown".
---

# split-goal

Grill to understand the goal. Decompose top-down until every leaf is a single actionable task. Write to `./goal-<slug>-YYYY-MM-DD.md`.

## Process

1. **Grill** — clarify scope, constraints, and success criteria before decomposing.

   Using the Socratic method — question assumptions, probe deeper, help the user discover the right framing themselves. Purpose: understand the goal well enough to split it correctly.

   Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

   Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

   There is no maximum number of questions. Keep going until the goal is fully understood. User can say "wrap up" to move on at any point.

2. **Decompose** — split the goal top-down. At each level, ask: can this be acted on directly, or does it need splitting? Keep splitting until every leaf is a single actionable task (no further decomposition possible).

3. **Write** — save to `./goal-<slug>-YYYY-MM-DD.md`.

## Output format

```md
# Goal: <goal title> — YYYY-MM-DD

## <Sub-goal 1>
- [ ] <atomic task>
- [ ] <atomic task>

### <Sub-sub-goal if needed>
- [ ] <atomic task>

## <Sub-goal 2>
...
```

- H2 = top-level sub-goals
- H3 = deeper splits if needed
- Leaves = `- [ ]` checkboxes (single actionable tasks)
- Each task should be completable in one sitting without further clarification
