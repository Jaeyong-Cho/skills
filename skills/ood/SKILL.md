---
name: ood
description: Turn a defined requirement set into a bounded object-oriented design by settling the domain model, responsibilities, data model, APIs, workflow, edge cases, failures, and trade-offs before implementation. Use between define-req and define-contract when behavior has meaningful state or responsibilities.
disable-model-invocation: true
---

# OOD

Design the smallest coherent object-oriented solution without writing implementation code.

## Input

- A completed requirement set from `/skill:define-req`
- The selected scope or first executable slice
- Repository conventions and existing domain code, if available

## Output

A design brief covering the domain model, responsibility owners, data model, APIs, workflow, bounded edge cases, failure modes, trade-offs, and the first contract. It is input to `/skill:define-contract`.

## Human interview

MUST RUN `/skill:grill-me` using `../references/human-checkpoint.md`. Scope the grill to OOD decisions for this selected slice only: domain model, responsibility ownership, data invariants, APIs, relevant edge cases, failures, and trade-offs. Do not let it interview implementation details or unrelated features.

Ask about, in order:

1. Which domain concept or state is actually in scope?
2. Who owns each behavior and why does it belong there?
3. What state and invariant must be protected?
4. What public operation should a caller use?
5. Which edge case or failure decision changes the design?

Confirm the design brief before handing it to `/skill:define-contract`.

## Source process

Follow this order and settle each step in one or two sentences before moving on:

> Requirements → Domain Model → Responsibilities → Data Model → APIs → Workflow → Edge Cases → Failure Modes → Trade-offs

Do not jump straight from requirements to workflow. That invents entities and fields mid-design.

## Rules

- Start from the requirement set produced by `/skill:define-req`.
- Preserve the user's behavior and constraints; do not invent product policy.
- Assign each state and behavior to one cohesive owner. Ask why it belongs there rather than elsewhere.
- Separate intent, domain rules, and technical mechanisms. Use `../references/abstraction-levels.md` and `../references/deep-modules.md`.
- Prefer the smallest design that satisfies the requirements. Do not add classes, interfaces, services, or patterns for hypothetical future flexibility.
- Keep non-goals explicit.
- Defer mechanics until the data model and APIs exist; do not decide implementation details prematurely.

## Design sequence

1. **Requirements** — list core actions, hard constraints/invariants, relevant actors, and explicit non-goals. A requirement should say what, not how.
2. **Domain model** — name the meaningful entities, value objects, and external collaborators. Do not create an object merely because there is a pipeline stage.
3. **Responsibilities** — assign each rule, state, and transition to one owner. For every non-obvious assignment, answer: “Why here and not elsewhere?”
4. **Data model** — identify the state each owner needs and its invariants. Keep data ownership singular.
5. **APIs** — define the smallest intent-revealing public operations and their inputs, outputs, errors, and allowed state transitions.
6. **Workflow** — describe the normal call sequence using the APIs, without leaking database, HTTP, SDK, or filesystem details into the domain narrative.
7. **Edge cases** — walk this fixed checklist against the actual APIs:
   - boundary values: zero, one, maximum, empty, negative where meaningful
   - state transitions the APIs allow, including duplicate calls
   - concurrency, only when the system is actually concurrent
   - failure of each named dependency once
   - invalid or adversarial input at every trust boundary
8. **Failure modes** — decide what stops, retries, rolls back, waits, alerts, or is explicitly out of scope. Every in-scope API behavior must be decided.
9. **Trade-offs** — state the simplest option, what it gives up, and the condition that would justify changing it. Check 10x/100x scale only when relevant.

## Edge-case boundary rule

An edge case is real only when you can name the concrete input, state, or call sequence that triggers it.

For every candidate case:

1. Name the concrete trigger.
2. Mark it **in scope**, **out of scope**, or **deferred with a condition**.
3. If it is in scope, decide the behavior and how it will be verified.
4. If it is deferred, state the condition that brings it into scope.
5. If it has no concrete trigger, record it once and move on.

Use this fixed checklist, once against the actual APIs:

- boundary values: zero, one, maximum, empty, negative where meaningful
- state transitions the APIs allow, including duplicate calls
- concurrency, only when the system is actually concurrent
- failure of each named dependency once
- invalid or adversarial input at every trust boundary

At requirements time, decide whether a case belongs in scope. After the data model and APIs exist, decide its mechanics. Do not make the checklist an invitation to imagine unlimited failures.

The goal is not exhaustive imagination. The goal is no undecided behavior inside the stated scope.

## Output

```markdown
## Requirements
[Core actions, invariants, non-goals]

## Domain model
[Entities, value objects, collaborators]

## Responsibilities
[Owner -> behavior/state, with reasons for non-obvious assignments]

## Data model
[Owned state and invariants]

## APIs
[Intent-revealing operations, inputs, outputs, errors, allowed transitions]

## Workflow
[Normal call sequence at the appropriate abstraction level]

## Edge cases
| Case | Concrete trigger | Scope | Decision | Verification |
|---|---|---|---|---|
| [case] | [input/state/call sequence] | in/out/deferred | [behavior or condition] | [test/check] |

## Failure modes
[Stop/retry/rollback/wait/alert decisions]

## Trade-offs
[Chosen simple option, cost, upgrade condition]

## First contract
[The smallest API or boundary to take to `/skill:define-contract`]
```

## Completion criterion

The design follows all nine steps, every in-scope core action and invariant has an owner and observable behavior, edge cases were checked mechanically, non-goals and deferred decisions are explicit, and the first contract is small enough to test and implement.
