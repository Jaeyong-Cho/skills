---
name: planning
description: Planning skill. Grills to resolve architecture, test plan, and action sequence, then writes an ADR. Use when invoked as /planning.
disable-model-invocation: true
---

# Planning

Read all files in `source-of-truth/wiki/` for direction and context.
Read `../references/meta-pattern.md`, `../references/deep-modules.md`, `../references/tdd.md`, `../references/tdd-tests.md`.

Use the grilling skill to resolve every branch of the plan:

1. **Architecture** — how to structure the implementation? Apply meta-pattern (Abstractness/Subdomain/Sharding axes) and deep-module principles (hide complexity, widen interfaces).
2. **Design** — what are the key modules, contracts, and data flows?
3. **Test plan** — what tests prove this works? Apply TDD: what is the smallest failing test, what does green look like?
4. **Evaluation criteria** — how do we know the result is good? Make it checkable.
5. **Action sequence** — ordered atomic steps to implement. Each step: one concern, one logical unit, describable without "and".

Grill until every branch is resolved and the user confirms. Completion criterion: action sequence is fully ordered with no ambiguous steps, user confirmed.

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a kebab-case slug from the topic.

Write `source-of-truth/adr/{timestamp}-{slug}.md`:

```markdown
# ADR: {Title}

**Date:** {YYYY-MM-DD}

## Context
{What the direction is and what problem it solves}

## Decision
{What was decided and the key architectural choices}

## Design
{Module structure, contracts, data flows}

## Action Sequence
1. {First atomic step}
2. {Second atomic step}
...

## Test Plan
- {Test}: {what it verifies}
...

## Evaluation Criteria
{Checkable conditions that define success}
```

`mkdir -p source-of-truth/adr` if needed. Tell the user the file path. Next step: `/action`.
