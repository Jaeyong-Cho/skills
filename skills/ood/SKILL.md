---
name: ood
description: "Turn one defined requirement into a complete vertical-slice object-oriented design and executable contract set: settle the Objects, Interfaces, user-facing boundary, workflow, edge cases, failures, and trade-offs before implementation. Use after req and before tdd."
disable-model-invocation: true
---

# OOD

Design the smallest coherent object-oriented solution and its complete boundary contracts. OOD must not implement the design directly: produce only the design-and-contract brief; implementation belongs to `/skill:tdd` and later implementation work. Do not write implementation code or feature tests.

## Input

- A completed requirement set from `/skill:req`
- The selected scope or first executable slice
- Repository conventions and existing domain code, if available

## Output

One design-and-contract brief covering the Objects, responsibility owners, data model, every applicable boundary in the vertical slice, exact Interfaces, end-to-end workflow, bounded edge cases, failure modes, trade-offs, and human verification. It is input to `/skill:tdd`. At completion, propose an exact path in the current directory, such as `./<slice-slug>-design.md`, and ask the human to confirm before writing it. Do not create a design/ directory by default.

## Human checkpoint

Do not conduct another design interview. Derive the design from the approved requirement, repository evidence, and existing conventions. Ask one focused clarification only when an unresolved decision would change observable behavior; otherwise choose the simplest compatible design and mark any assumption explicitly.

Present the completed design and contract brief for confirmation before writing it. Ask for one confirmation only; do not split OOD and contract design into separate checkpoints.

## Source process

Follow this order and settle each step in one or two sentences before moving on:

> Requirements → Domain Model → Responsibilities → Data Model → APIs → Workflow → Edge Cases → Failure Modes → Trade-offs

Do not jump straight from requirements to workflow. That invents entities and fields mid-design.

## Rules

- Start from the requirement set produced by `/skill:req`.
- Preserve the user's behavior and constraints; do not invent product policy.
- Assign each state and behavior to one cohesive owner. Ask why it belongs there rather than elsewhere.
- Separate intent, domain rules, and technical mechanisms. Use `../references/abstraction-levels.md` and `../references/deep-modules.md`.
- Prefer the smallest design that satisfies the requirements. Do not add classes, interfaces, services, or patterns for hypothetical future flexibility.
- Keep non-goals explicit.
- Defer mechanics until the data model and APIs exist; do not decide implementation details prematurely.
- Inspect repository conventions and existing code before defining new Objects or Interfaces.
- Treat one requirement as a vertical slice, not only an internal API. Enumerate every real boundary needed for its outcome: user-facing entrypoint (CLI, HTTP, UI, or job trigger) and the applicable application, domain, persistence, and external-service boundaries. Omit layers that do not exist; do not invent abstractions.
- Design the user-facing boundary first when one exists, then trace its input, observable output, errors, and side effects through the internal boundaries. The slice is incomplete if a user-visible requirement stops at an internal API.
- Define the smallest practical Interface at every applicable boundary. For a CLI, specify the command, arguments/options, stdout/stderr, exit codes, side effects, and an exact human verification command. Do not create abstract types without a real substitution boundary or multiple implementations.
- Do not implement behavior or write the feature test. Define only the signatures, schemas, boundary shapes, observable results, dependency seams, and documentation needed to make the slice unambiguous.

## Design sequence

1. **Requirements** — list core actions, hard constraints/invariants, relevant actors, and explicit non-goals. A requirement should say what, not how.
2. **Domain model** — name the meaningful entities, value objects, and external collaborators. Do not create an object merely because there is a pipeline stage.
3. **Responsibilities** — assign each rule, state, and transition to one owner. For every non-obvious assignment, answer: “Why here and not elsewhere?”
4. **Data model** — identify the state each owner needs and its invariants. Keep data ownership singular.
5. **Interfaces and contracts** — define the smallest intent-revealing operation or boundary shape at every applicable layer, including inputs, outputs, errors, side effects, allowed state transitions, dependency seams, and external-to-internal translation.
6. **Workflow** — describe the normal call sequence from the user-facing entrypoint through the designed Objects and Interfaces to dependencies, without leaking database, HTTP, SDK, or filesystem details into the domain narrative.
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

## Objects
[Entities, value objects, collaborators, and each responsibility owner]

## Responsibilities
[Owner -> behavior/state, with reasons for non-obvious assignments]

## Data model
[Owned state and invariants]

## Boundary map
| Layer | Boundary | Caller/user | Inputs | Observable outputs/errors | Side effects |
|---|---|---|---|---|---|
| [CLI/API/application/domain/dependency] | [name] | [caller] | [shape] | [result] | [effect] |

## Interfaces and contracts
### External interface
Boundary: [CLI | HTTP API | UI action | job trigger | none]
Invocation/request shape: [exact command, arguments/options, request, or trigger]
Inputs/preconditions: [shape and validation]
Output: [stdout/response/state/result]
Errors: [stderr/response, exit codes, failure outcomes]
Side effects: [writes, calls, state changes]
Human verification: [exact command or observable check]

### Internal interfaces
| Object/boundary | Caller | Signature/shape | Inputs | Outputs/errors | Side effects | Dependencies/test seams |
|---|---|---|---|---|---|---|
| [application/domain/persistence/dependency] | [caller] | [exact shape] | [inputs] | [results] | [effects] | [seams] |

## Workflow
[Explicit sequence: user -> external interface -> Objects -> internal Interfaces -> dependencies -> observable result]

## Traceability
| Acceptance criterion | Observable at external interface | Object/interface responsible |
|---|---|---|
| [criterion] | [how] | [where] |

## Edge cases
| Case | Concrete trigger | Scope | Decision | Verification |
|---|---|---|---|---|
| [case] | [input/state/call sequence] | in/out/deferred | [behavior or condition] | [test/check] |

## Failure modes
[Stop/retry/rollback/wait/alert decisions]

## Trade-offs
[Chosen simple option, cost, upgrade condition]

Next skill: `/skill:tdd`
```

## Completion criterion

The design follows all nine steps, every in-scope core action and invariant has an owner and observable behavior, every applicable boundary in the vertical slice is identified, every Object and Interface needed for the outcome is explicit, the workflow connects the external interface to the designed Objects and internal Interfaces, no user-facing path stops at an internal API, edge cases were checked mechanically, non-goals and deferred decisions are explicit, and the contract is small enough to test and implement.
