---
name: ood
description: Turn a defined requirement set into a bounded vertical-slice object-oriented design by settling the domain model, responsibilities, data model, APIs, user-facing boundaries, internal boundaries, workflow, edge cases, failures, and trade-offs before implementation. Use between define-req and define-contract when behavior has meaningful state or responsibilities.
disable-model-invocation: true
---

# OOD

Design the smallest coherent object-oriented solution without writing implementation code.

## Input

- A completed requirement set from `/skill:define-req`
- The selected scope or first executable slice
- Repository conventions and existing domain code, if available

## Output

A design brief covering the domain model, responsibility owners, data model, every applicable boundary in the vertical slice, workflow, bounded edge cases, failure modes, trade-offs, and the contract-set handoff. It is input to `/skill:define-contract`. At completion, propose an exact path in the current directory, such as `./<slice-slug>-design.md`, and ask the human to confirm before writing it. Do not create a design/ directory by default.

## Human checkpoint

Do not conduct another design interview. Derive the design from the approved requirement, repository evidence, and existing conventions. Ask one focused clarification only when an unresolved decision would change observable behavior; otherwise choose the simplest compatible design and mark any assumption explicitly.

Present the completed design brief for confirmation before handing it to `/skill:define-contract`.

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
- Treat one requirement as a vertical slice, not only an internal API. Enumerate every real boundary needed for its outcome: user-facing entrypoint (CLI, HTTP, UI, or job trigger) and the applicable application, domain, persistence, and external-service boundaries. Omit layers that do not exist; do not invent abstractions.
- Design the user-facing boundary first when one exists, then trace its input, observable output, errors, and side effects through the internal boundaries. The slice is incomplete if a user-visible requirement stops at an internal API.

## Design sequence

1. **Requirements** — list core actions, hard constraints/invariants, relevant actors, and explicit non-goals. A requirement should say what, not how.
2. **Domain model** — name the meaningful entities, value objects, and external collaborators. Do not create an object merely because there is a pipeline stage.
3. **Responsibilities** — assign each rule, state, and transition to one owner. For every non-obvious assignment, answer: “Why here and not elsewhere?”
4. **Data model** — identify the state each owner needs and its invariants. Keep data ownership singular.
5. **APIs** — define the smallest intent-revealing public operations and their inputs, outputs, errors, and allowed state transitions at each applicable boundary.
6. **Workflow** — describe the normal call sequence from the user-facing entrypoint through the internal APIs and dependencies, without leaking database, HTTP, SDK, or filesystem details into the domain narrative.
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

## Boundary map
| Layer | Boundary | Caller/user | Inputs | Observable outputs/errors | Side effects |
|---|---|---|---|---|---|
| [CLI/API/application/domain/dependency] | [name] | [caller] | [shape] | [result] | [effect] |

## APIs
[Intent-revealing operations, inputs, outputs, errors, allowed transitions for every applicable boundary]

## Workflow
[Normal call sequence from the external entrypoint through internal boundaries]

## Edge cases
| Case | Concrete trigger | Scope | Decision | Verification |
|---|---|---|---|---|
| [case] | [input/state/call sequence] | in/out/deferred | [behavior or condition] | [test/check] |

## Failure modes
[Stop/retry/rollback/wait/alert decisions]

## Trade-offs
[Chosen simple option, cost, upgrade condition]

## Contract-set handoff
[The complete set of applicable boundaries, with the user-facing boundary first and the primary public boundary identified for `/skill:define-contract`]
```

## Completion criterion

The design follows all nine steps, every in-scope core action and invariant has an owner and observable behavior, every applicable boundary in the vertical slice is identified, no user-facing path stops at an internal API, edge cases were checked mechanically, and non-goals and deferred decisions are explicit. The contract-set handoff is small enough to define, test, and implement.
