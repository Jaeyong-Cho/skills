---
name: define-contract
description: "Define the complete executable contract set for one selected requirement after its OOD responsibilities are settled: its user-facing boundary plus every applicable internal boundary, with explicit inputs, outputs, errors, and side effects. Use after define-req or ood and before writing the test."
disable-model-invocation: true
---

# Define Contract

Turn one approved requirement into a complete vertical-slice contract set that the test and implementation can share.

## Input

- One selected requirement from `/skill:define-req`
- The applicable responsibility and API decisions from `/skill:ood`
- Existing repository conventions

## Output

One written executable contract set in the codebase for one requirement: the user-facing boundary (when one exists) plus every applicable internal boundary—such as application, domain, persistence, or external-service seams—with explicit inputs, outputs, errors, side effects, and dependency seams, but no feature behavior. It is input to `/skill:tdd`; identify the primary public boundary that TDD will exercise. Confirm the exact code paths before writing and report them at completion.

## Rules

- Start from one selected requirement from `/skill:define-req`, using the responsibility and API decisions from `/skill:ood` when that design step applies; do not combine it with sibling requirements.
- Treat the requirement as one vertical slice. Enumerate every real boundary needed to deliver its outcome: start with the user-facing CLI, HTTP, UI, or job entrypoint when present, then cover the applicable application, domain, persistence, and external-service boundaries. Omit layers that do not exist; do not invent abstractions.
- Inspect the repository and reuse its conventions before creating new boundaries.
- Define the smallest useful contract for each applicable boundary: inputs, output, errors, side effects, and dependency seams. The outer boundary must be concrete enough for a human to invoke or inspect—for a CLI, specify the command, arguments/options, stdout/stderr, exit codes, and a manual verification command.
- An interface means a practical boundary (function, command, API, or stage), not automatically an abstract type.
- Create an abstract interface only when there is a real substitution boundary or multiple implementations.
- Do not implement behavior and do not write the feature test here.

## Human checkpoint

Derive the contract from the approved requirement, applicable OOD decisions, repository evidence, and existing conventions. Before writing it, show the candidate contract set in plain language, including the outer/user-facing boundary and its internal path, and ask once:

> “Is this the one behavior and complete boundary set you want to test and implement now?”

Ask one focused clarification only when the requirement or design leaves the actor, input, output, error, or side effect unresolved. Confirm the contract before editing the codebase.

## OOD check

Read `../references/abstraction-levels.md` and `../references/deep-modules.md` before defining the boundary.

- Classify the boundary as intent/orchestration, domain behavior, or mechanism.
- Give each meaningful responsibility one cohesive owner; do not create a class merely because a stage exists.
- Keep the contract narrow and hide implementation complexity behind it.
- Higher-level code may depend on a capability contract, but domain code must not depend directly on a concrete database, HTTP client, SDK, or filesystem implementation.
- Treat public/private access and abstraction level as separate decisions.

## Workflow

1. Read the requirement card and its acceptance criteria.
2. Find the natural locations and neighboring conventions in the repository.
3. Map the complete contract set in plain language, starting at the outer boundary:
   - trigger/caller
   - inputs and preconditions
   - output or state change
   - errors and failure behavior
   - side effects and dependencies
   - translation between external and internal shapes
4. Write the smallest signature, schema, CLI shape, or job-stage contract needed at each applicable boundary. For a CLI, include a concrete human invocation and expected observable result. Add only compile/type information and documentation necessary to make each boundary unambiguous.
5. Check that every acceptance criterion is observable through the primary public boundary and traceable to the internal boundaries.
6. Report any unresolved contract question instead of inventing policy.

## Output

```markdown
## Contract set
Requirement: [one selected requirement]
Primary public boundary: [CLI | HTTP API | UI action | job trigger | internal API]

### External contract
Boundary: [exact user-facing boundary, or “none”]
Invocation/request shape: [exact command, arguments/options, request, or trigger]
Inputs/preconditions: [shape and validation]
Output: [stdout/response/state/result]
Errors: [stderr/response, exit codes, failure outcomes]
Side effects: [writes, calls, state changes]
Human verification: [exact command or observable check, when applicable]

### Internal boundary contracts
| Boundary | Caller | Signature/shape | Inputs | Outputs/errors | Side effects | Dependencies/test seams |
|---|---|---|---|---|---|---|
| [application/domain/persistence/dependency] | [caller] | [exact shape] | [inputs] | [results] | [effects] | [seams] |

### Traceability
| Acceptance criterion | Observable at public boundary | Internal boundary(s) |
|---|---|---|
| [criterion] | [how] | [where] |

Next skill: `/skill:tdd`
```

## Completion criterion

The contract set is written in the codebase's normal location, has no production behavior, maps to exactly one requirement, includes every applicable boundary in that vertical slice, starts with a concrete user-facing contract when one exists, assigns each responsibility clearly, keeps every interface narrow, and makes both human verification and automated test inputs and expected observable results unambiguous.
