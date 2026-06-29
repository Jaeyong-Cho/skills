---
name: planning
description: Planning skill. Grills to resolve architecture, test plan, and action sequence, then writes an ADR. Use when invoked as /planning.
disable-model-invocation: true
---

# Planning

Read all files in `source-of-truth/direction/` for the committed direction. Read `source-of-truth/wiki/` for broader context. Also read `source-of-truth/adr/` — if an existing ADR covers the same topic, read it and revise it rather than creating a new one.

Use this for new plans or to replan after a fix reveals new design needs.
Read `../references/meta-pattern.md`, `../references/deep-modules.md`, `../references/tdd.md`, `../references/tdd-tests.md`, `../references/tdd-mocking.md`, `../references/test-loop.md`.

Run a `/grilling` skill to resolve every branch of the plan:

1. **Architecture** — how to structure the implementation? Apply meta-pattern (Abstractness/Subdomain/Sharding axes) and deep-module principles (hide complexity, widen interfaces).
2. **Design** — what are the key modules, contracts, and data flows?
3. **Observability** — which debugging information is needed for handling issue? how to verify the logic is working well or not? which informations need to see to judge this plan is working well? how to detect known unknown or unknown unknown ambiguous and concern point? (e.g. "use assert to detect concern point" or "write debugging data to the json in data directory")
4. **Test-loop design** — first check if an existing test-loop already covers the needed behaviors; if so, reuse or extend it rather than creating a new one. Only design a new loop if the existing one cannot cover the scenarios. Apply `test-loop.md`: what is the clean state (what to reset before each run)? what environment setup is needed? what specific behaviors does the loop exercise — name each scenario? what are the expected outputs per scenario?
5. **Test plan** — what tests prove this works? Apply TDD: what is the smallest failing test, what does green look like?
6. **Evaluation criteria** — how do we know the result is good? Make it checkable. how to human know if the changes is working well at the real working system with real data? how to  which one need to see for verify? how to observe it? how to judge the plan is working well? (e.g. "the user can do X in Y seconds", "see the data and check all of them has property P", "the system can handle N requests per second", "If log A -> log B and data X -> Y -> Z is shown, then it is working well" or "All of the unmatched is zero, then it is working well"). Make it checkable.
7. **Action sequence** — ordered atomic steps to implement. Each step: one concern, one logical unit, describable without "and".


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

## Test-Loop Design
- **Clean state:** {what to reset before each run}
- **Environment setup:** {env vars, seed data, config}
- **Behaviors:**
  - {Scenario name}: {inputs} → {expected output}
  ...

## Test Plan
- {Test}: {what it verifies}
...

## Evaluation Criteria
{Checkable conditions that define success}
```

`mkdir -p source-of-truth/adr` if needed. Tell the user the file path. Next step: `/action`.

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `source-of-truth/wiki/` at any time.

**DO NOT START IMPLEMENT**
