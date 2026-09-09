---
name: ood
description: Design all approved requirement slices as small object-oriented vertical-slice solutions, then write one approved design-and-contract document per slice. Use after req and before to-plan.
disable-model-invocation: true
---

# OOD

First explore the existing codebase, then design the smallest coherent object-oriented solution for the complete approved requirement inventory. During design, explicitly choose whether each affected area is reused, modified, created, deleted, or left unchanged. The primary output is one design-and-contract document per requirement slice. Process slices independently in dependency order, but validate their shared component responsibilities and interfaces as one batch.

OOD does not implement the design or write feature tests. Implementation belongs to `/skill:do-plan`.

Use specific names:
- **Entry point:** where a user or system starts the flow, such as a Save button, CLI command, API endpoint, or job trigger.
- **Component interface:** how a caller uses a component, such as `save(snapshot)`; its contract defines inputs, results, errors, and side effects. An API is a programmatic interface, not necessarily an HTTP endpoint.
- **Responsibility:** the behavior and state a component owns. Describing an interface does not require creating a new interface type or layer.
- **Scope:** the behavior included in or excluded from a requirement slice.

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
- An evidence-based existing-codebase assessment and a reuse/modify/create/delete/unchanged decision for every affected area
- Explicit cross-slice dependencies, shared component responsibilities and interfaces, non-goals, deferred decisions, and trade-offs

Reuse the target repository's design convention if it has one. Do not create a second design system. Follow `../references/document-style.md`; use the target's metadata convention for each design document.

## Start with repository exploration

Before naming new Objects, explore the existing codebase for the selected requirement slices:

1. Read repository instructions, relevant requirement documents, current design conventions, source files, tests, build configuration, and commands.
2. Trace the current behavior from its public entry point through the relevant domain and infrastructure components and their interfaces.
3. Find callers, owned state, existing Objects, Interfaces, utilities, tests, and dead or duplicated paths that may be affected.
4. Record exact file/path evidence and list candidate areas that could be reused, modified, created, deleted, or left unchanged.
5. Do not select an action during exploration. Exploration records facts and options; design makes the selection.

**Completion criterion:** the relevant current flow, entry points, component interfaces, tests, callers, and candidate existing components are documented with evidence before design decisions are made.

## Human checkpoint

Derive the designs from the approved requirements, repository evidence, and existing conventions. Ask only a blocking clarification when its answer would change observable behavior, and use `../references/question-format.md`.

Draft every slice before the approval gate. Present a compact summary, exact paths, cross-slice assumptions, and unresolved decisions. Ask exactly one batch question:

> Do you approve these designs, or should I change anything before writing them to `<design-paths>`?

Do not write any design document, start implementation or testing, or reinterpret silence as approval until the human confirms. If one design changes, update its brief and re-present the affected batch before writing.

## Scope and design constraints

- Preserve the requirement inventory, scope, exclusions, edge-case decisions, and deferred topics exactly.
- Design one vertical slice at a time. Do not design a horizontal backend/frontend/database layer.
- A shared Object or Interface is allowed only when the repository or multiple approved slices have a concrete shared responsibility or interaction; record its ownership and all consumers.
- Explore existing code before proposing a new Object, Interface, file, or layer.
- In the design, classify every affected existing area as **reuse**, **modify**, **create**, **delete**, or **unchanged**, with evidence and a reason. Do not make this selection during exploration.
- Prefer reuse or modification when it satisfies the approved behavior; create only when no suitable existing area exists; delete only when the area is dead, duplicated, or made unnecessary and its callers/tests are accounted for.
- Omit layers that do not exist. Do not invent abstractions for hypothetical substitutions.
- Do not write implementation code, feature tests, migration scripts, or library choices in a design brief.

## Design workflow

### 1. Validate the input batch

1. Read the requirement inventory and every linked requirement document.
2. Check that each accepted slice has one actor, trigger, outcome, explicit flow start/end, acceptance criteria, and concrete edge-case decisions.
3. Confirm the dependency order and identify shared external interfaces, dependencies, or state. Keep each slice's behavior separate even when implementation may reuse an Object.
4. Inspect repository conventions and existing domain code before naming new Objects or Interfaces.

**Completion criterion:** every design input exists, is approved, is traceable to the inventory, and has no missing or silently widened behavior.

### 2. Design each slice

For each requirement, complete this sequence in order:

> Existing Code Assessment → Reuse/Modify/Create/Delete Selection → Requirements → Domain Model → Responsibilities → Data Model → APIs → Workflow → Edge Cases → Failure Modes → Trade-offs

1. **Existing code assessment** — summarize the explored current flow, affected files/components, callers, tests, and constraints with exact evidence. This is fact-finding, not a commitment.
2. **Selection** — choose one action for every affected existing area: reuse, modify, create, delete, or unchanged. Explain why the selected action is the smallest coherent fit and name the behavior/tests affected. A new Object or Interface must have a concrete responsibility; a deletion must account for callers and replacement behavior.
3. **Requirements** — list core actions, hard constraints/invariants, actors, acceptance criteria, and explicit non-goals. State what, not how.
3. **Domain model** — name meaningful entities, value objects, and external collaborators. Do not create an Object merely because the workflow has a step.
4. **Responsibilities** — assign each state, rule, and transition to one cohesive owner. For every non-obvious assignment, state why it belongs there.
5. **Data model** — identify owned state and invariants. Keep data ownership singular.
6. **Interfaces and contracts** — define the smallest intent-revealing operation at each applicable component interface: inputs, outputs, errors, side effects, allowed transitions, dependency seams, and external-to-internal translation.
7. **Workflow** — trace the normal call sequence from the user-facing entrypoint through Objects and Interfaces to dependencies and the observable result. Do not leak database, HTTP, SDK, or filesystem details into the domain narrative.
8. **Edge cases** — apply the fixed checklist below to the actual APIs.
9. **Failure modes** — decide what stops, retries, rolls back, waits, alerts, or is explicitly out of scope.
10. **Trade-offs** — state the simplest option, what it gives up, and the condition that justifies changing it. Check scale only when relevant.

Use `../references/abstraction-levels.md` for L1/L2/L3 ownership, `../references/deep-modules.md` for small interfaces that hide implementation complexity, and `../references/testing-guidelines.md` to choose the lowest-cost sufficient verification level. Prefer the smallest design that satisfies the requirement.

**Completion criterion:** the slice's public entry points and observable outcomes, Objects, responsibilities, owned data, Interfaces, workflow, failures, edge cases, and trade-offs are all explicit and traceable to its requirement.

### 3. Check edge cases mechanically

An edge case is real only when it names a concrete input, state, or call sequence. For every candidate:

1. Name the trigger.
2. Mark it `in scope`, `out of scope`, or `deferred with a condition`.
3. If in scope, decide the observable behavior and verification.
4. If deferred, state the condition that reopens it.
5. If there is no concrete trigger, record it once and move on.

Apply this checklist once per slice against the actual designed APIs:

- input limits and special values: zero, one, maximum, empty, and negative where meaningful;
- allowed state transitions, including duplicate calls;
- concurrency only when the system is actually concurrent;
- failure of each named dependency once;
- invalid or adversarial input wherever data from a less-trusted caller or system enters a trusted component.

Do not use the checklist to invent unlimited hypothetical failures. Requirements decide scope; OOD decides mechanics.

**Completion criterion:** every in-scope edge case has a decided behavior and verification, and every out-of-scope/deferred case has a reason or reopening condition.

### 4. Cross-slice and contract review

Before the human checkpoint, validate the batch:

- every acceptance criterion maps to an observable external result and one responsible Object/Interface;
- every user-facing path reaches its observable outcome, including required external effects, and does not stop at an internal API;
- every applicable entry point and component interaction is present: CLI/API/UI/job, application, domain, persistence, and external service;
- each interface has the smallest practical contract, with no interface created only for imagined substitution;
- L1 intent, L2 business rules, and L3 mechanisms do not leak into one another;
- shared Objects, state, and Interfaces have one owner and named consumers;
- non-goals, deferred decisions, and assumptions are visible;
- the designs do not introduce a product policy absent from the requirements.

**Completion criterion:** the full batch is internally consistent, every slice is independently understandable, shared component responsibilities and interfaces are justified, and no requirement or edge case is unowned.

### 5. Approve and write the design documents

After the batch review, show:

- one summary and exact path per slice;
- the existing-code assessment and reuse/modify/create/delete/unchanged selection map;
- the cross-slice dependency and shared-interface map;
- open assumptions and deferred decisions;
- any requirement-to-design traceability gaps.

Use the batch approval question from the Human checkpoint. After approval:

1. Write one design document to `design/<epic>/<slice>.md` for every approved slice, or the repository's equivalent.
2. Preserve the exact requirement path, acceptance criteria, edge-case table, and deferred topics in each design document.
3. Add the entry point and component interface map, Objects, responsibilities, data model, Interfaces, workflow, failure modes, trade-offs, and traceability table.
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

## Existing code assessment and selection
[Relevant current flow and exact evidence]

| Existing area | Evidence | Decision: reuse / modify / create / delete / unchanged | Reason | Affected tests or behavior |
|---|---|---|---|---|

## Objects
[Entities, value objects, collaborators, ownership]

## Responsibilities
[Owner -> behavior/state, with reasons for non-obvious assignments]

## Data model
[Owned state and invariants]

## Entry points and component interfaces
| Layer | Entry point or component operation | Caller/user | Inputs | Observable outputs/errors | Side effects |
|---|---|---|---|---|---|

## Interfaces and contracts
### External interface
[Exact invocation/request, validation, output, errors, side effects, human verification]

### Internal interfaces
| Component/interface | Caller | Signature/shape | Inputs | Outputs/errors | Side effects | Dependencies/test seams |
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

Pass the complete design inventory and all design paths to `/skill:to-plan`. That skill writes one implementation plan per slice with verification selected under `../references/testing-guidelines.md`, which `/skill:do-plan` executes without pulling deferred topics back into the design.

## Completion criterion

OOD is complete only when the complete approved requirement inventory has one human-approved design document per slice, every in-scope behavior and edge case has an owner, every applicable entry point, component interface, and contract is explicit, cross-slice sharing is justified, no implementation code or feature test was written, and the exact design paths are ready for planning.
