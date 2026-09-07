---
name: ood
description: Design all approved requirement slices as small object-oriented vertical-slice solutions, then write one approved design-and-contract document per slice. Use after req and before to-plan/tdd.
disable-model-invocation: true
---

# OOD

Design the smallest coherent object-oriented solution for the complete approved requirement inventory. The primary output is one design-and-contract document per requirement slice. Process slices independently in dependency order, but validate their shared boundaries as one batch.

OOD does not implement the design or write feature tests. Implementation belongs to `/skill:tdd` and `/skill:do-plan`.

## Input

- The approved requirement inventory and its dependency order from `/skill:req`
- Every confirmed requirement document, including its acceptance criteria and edge cases
- Repository instructions, conventions, existing code, and existing tests

A single requirement document is a valid one-slice batch.

## Output

- One approved design-and-contract brief per requirement document
- One exact design path per slice, defaulting to:

```text
design/<epic>/<slice>.md
```

- Traceability from every requirement and acceptance criterion to Objects, Interfaces, observable behavior, and verification
- Explicit cross-slice dependencies, shared boundaries, non-goals, deferred decisions, and trade-offs

Reuse the target repository's design convention if it has one. Do not create a second design system. Follow `../references/document-style.md`; use the target's metadata convention for each design document.

## Start with Grill Me

Before validating the input batch, gather only the approved requirement and repository context needed to brief the interviewer, then **MUST RUN** `@skills/grill-me`. Keep the session focused on requirement interpretation, object responsibilities, boundaries, contracts, failure handling, and trade-offs. Preserve the approved behavior and scope. If the session finds behavioral ambiguity, stop and return it to `/skill:req`; resolve only design questions that cannot change observable behavior. Continue only after shared understanding is confirmed, carrying forward confirmed decisions, assumptions, deferred topics, and blockers. This is the only design interview and is separate from the batch approval gate below.

## Human checkpoint

Derive the designs from the approved requirements, repository evidence, and existing conventions. After the opening grill, ask only a blocking clarification when its answer would change observable behavior, and use `../references/question-format.md`.

Draft every slice before the approval gate. Present a compact summary, exact paths, cross-slice assumptions, and unresolved decisions. Ask exactly one batch question:

> Do you approve these designs, or should I change anything before writing them to `<design-paths>`?

Do not write any design document, start TDD, or reinterpret silence as approval until the human confirms. If one design changes, update its brief and re-present the affected batch before writing.

## Batch boundaries

- Preserve the requirement inventory, scope, exclusions, edge-case decisions, and deferred topics exactly.
- Design one vertical slice at a time. Do not design a horizontal backend/frontend/database layer.
- A shared Object or Interface is allowed only when the repository or multiple approved slices provide a real shared boundary; record its ownership and all consumers.
- Omit layers that do not exist. Do not invent abstractions for hypothetical substitutions.
- Do not write implementation code, feature tests, migration scripts, or library choices in a design brief.

## Design workflow

### 1. Validate the input batch

1. Read the requirement inventory and every linked requirement document.
2. Check that each accepted slice has one actor, trigger, outcome, boundary, acceptance criteria, and concrete edge-case decisions.
3. Confirm the dependency order and identify shared external boundaries or state. Keep each slice's behavior separate even when implementation may reuse an Object.
4. Inspect repository conventions and existing domain code before naming new Objects or Interfaces.

**Completion criterion:** every design input exists, is approved, is traceable to the inventory, and has no missing or silently widened behavior.

### 2. Design each slice

For each requirement, complete this sequence in order:

> Requirements → Domain Model → Responsibilities → Data Model → APIs → Workflow → Edge Cases → Failure Modes → Trade-offs

1. **Requirements** — list core actions, hard constraints/invariants, actors, acceptance criteria, and explicit non-goals. State what, not how.
2. **Domain model** — name meaningful entities, value objects, and external collaborators. Do not create an Object merely because the workflow has a step.
3. **Responsibilities** — assign each state, rule, and transition to one cohesive owner. For every non-obvious assignment, state why it belongs there.
4. **Data model** — identify owned state and invariants. Keep data ownership singular.
5. **Interfaces and contracts** — define the smallest intent-revealing operation at each applicable boundary: inputs, outputs, errors, side effects, allowed transitions, dependency seams, and external-to-internal translation.
6. **Workflow** — trace the normal call sequence from the user-facing entrypoint through Objects and Interfaces to dependencies and the observable result. Do not leak database, HTTP, SDK, or filesystem details into the domain narrative.
7. **Edge cases** — apply the fixed checklist below to the actual APIs.
8. **Failure modes** — decide what stops, retries, rolls back, waits, alerts, or is explicitly out of scope.
9. **Trade-offs** — state the simplest option, what it gives up, and the condition that justifies changing it. Check scale only when relevant.

Use `../references/abstraction-levels.md` for L1/L2/L3 ownership and `../references/deep-modules.md` for boundary shape. Prefer the smallest design that satisfies the requirement.

**Completion criterion:** the slice's external boundary, Objects, responsibilities, owned data, Interfaces, workflow, failures, edge cases, and trade-offs are all explicit and traceable to its requirement.

### 3. Check edge cases mechanically

An edge case is real only when it names a concrete input, state, or call sequence. For every candidate:

1. Name the trigger.
2. Mark it `in scope`, `out of scope`, or `deferred with a condition`.
3. If in scope, decide the observable behavior and verification.
4. If deferred, state the condition that reopens it.
5. If there is no concrete trigger, record it once and move on.

Apply this checklist once per slice against the actual designed APIs:

- boundary values: zero, one, maximum, empty, and negative where meaningful;
- allowed state transitions, including duplicate calls;
- concurrency only when the system is actually concurrent;
- failure of each named dependency once;
- invalid or adversarial input at every trust boundary.

Do not use the checklist to invent unlimited hypothetical failures. Requirements decide scope; OOD decides mechanics.

**Completion criterion:** every in-scope edge case has a decided behavior and verification, and every out-of-scope/deferred case has a reason or reopening condition.

### 4. Cross-slice and contract review

Before the human checkpoint, validate the batch:

- every acceptance criterion maps to an observable external result and one responsible Object/Interface;
- every user-facing path reaches its real external boundary and does not stop at an internal API;
- every applicable boundary is present: CLI/API/UI/job, application, domain, persistence, and external service;
- each boundary has the smallest practical contract, with no interface created only for imagined substitution;
- L1 intent, L2 business rules, and L3 mechanisms do not leak into one another;
- shared Objects, state, and Interfaces have one owner and named consumers;
- non-goals, deferred decisions, and assumptions are visible;
- the designs do not introduce a product policy absent from the requirements.

**Completion criterion:** the full batch is internally consistent, every slice is independently understandable, shared boundaries are justified, and no requirement or edge case is unowned.

### 5. Approve and write the design documents

After the batch review, show:

- one summary and exact path per slice;
- the cross-slice dependency/shared-boundary map;
- open assumptions and deferred decisions;
- any requirement-to-design traceability gaps.

Use the batch approval question from the Human checkpoint. After approval:

1. Write one design document to `design/<epic>/<slice>.md` for every approved slice, or the repository's equivalent.
2. Preserve the exact requirement path, acceptance criteria, edge-case table, and deferred topics in each design document.
3. Add the boundary map, Objects, responsibilities, data model, Interfaces, workflow, failure modes, trade-offs, and traceability table.
4. Link each design document back to its requirement and forward to its plan path when the target convention permits it.
5. Do not write production code or feature tests.

**Completion criterion:** every approved slice has exactly one written design document at its confirmed path, all documents preserve scope and edge cases, indexes/links are synchronized where the repository requires them, and no implementation code was written.

## Design document shape

Use this structure for every slice:

```markdown
# [Slice]

- Requirement: [exact requirement path]
- Design: [exact design path]
- Plan: [pending plan path]

## Requirements
[Core actions, invariants, acceptance criteria, non-goals]

## Objects
[Entities, value objects, collaborators, ownership]

## Responsibilities
[Owner -> behavior/state, with reasons for non-obvious assignments]

## Data model
[Owned state and invariants]

## Boundary map
| Layer | Boundary | Caller/user | Inputs | Observable outputs/errors | Side effects |
|---|---|---|---|---|---|

## Interfaces and contracts
### External interface
[Exact invocation/request, validation, output, errors, side effects, human verification]

### Internal interfaces
| Object/boundary | Caller | Signature/shape | Inputs | Outputs/errors | Side effects | Dependencies/test seams |
|---|---|---|---|---|---|---|

## Workflow
[User -> external interface -> Objects -> internal Interfaces -> dependencies -> result]

## Traceability
| Acceptance criterion | Observable result | Object/interface responsible | Verification |
|---|---|---|---|

## Edge cases
| Case | Concrete trigger | Scope | Decision | Verification |
|---|---|---|---|---|

## Failure modes
[Stop/retry/rollback/wait/alert decisions]

## Trade-offs
[Chosen simple option, cost, upgrade condition]
```

## Handoff

Pass the complete design inventory and all design paths to `/skill:to-plan`. That skill writes one TDD implementation plan per slice. `/skill:tdd` then executes one behavior at a time from those approved plans; it must not pull deferred topics back into the design.

## Completion criterion

OOD is complete only when the complete approved requirement inventory has one human-approved design document per slice, every in-scope behavior and edge case has an owner, every applicable boundary and contract is explicit, cross-slice sharing is justified, no implementation code or feature test was written, and the exact design paths are ready for planning.
