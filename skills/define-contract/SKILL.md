---
name: define-contract
description: "Define the smallest executable contract for one selected requirement after its OOD responsibilities are settled: a function, CLI command, API, or job-stage boundary with explicit inputs, outputs, errors, and side effects. Use after define-req or ood and before writing the test."
disable-model-invocation: true
---

# Define Contract

Turn one approved requirement into a concrete boundary that the test and implementation can share.

## Input

- One selected requirement from `/skill:define-req`
- The applicable responsibility and API decisions from `/skill:ood`
- Existing repository conventions

## Output

One written executable contract in the codebase: a function, command, API, or job-stage boundary with explicit inputs, outputs, errors, side effects, and dependency seams, but no feature behavior. It is input to `/skill:tdd`. Confirm the exact code path before writing and report it at completion.

## Rules

- Start from one selected requirement from `/skill:define-req`, using the responsibility and API decisions from `/skill:ood` when that design step applies; do not combine it with sibling requirements.
- Inspect the repository and reuse its conventions before creating a new boundary.
- Define the smallest useful contract: inputs, output, errors, side effects, and dependency seams.
- An interface means a practical boundary (function, command, API, or stage), not automatically an abstract type.
- Create an abstract interface only when there is a real substitution boundary or multiple implementations.
- Do not implement behavior and do not write the feature test here.

## Human checkpoint

Derive the contract from the approved requirement, applicable OOD decisions, repository evidence, and existing conventions. Before writing it, show the candidate boundary in plain language and ask once:

> “Is this the one behavior and boundary you want to test and implement now?”

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
2. Find the natural location and neighboring conventions in the repository.
3. State the contract in plain language:
   - trigger/caller
   - inputs and preconditions
   - output or state change
   - errors and failure behavior
   - side effects and dependencies
4. Write the smallest signature, schema, CLI shape, or job-stage contract needed by the requirement. Add only compile/type information and documentation necessary to make the boundary unambiguous.
5. Check that every acceptance criterion can be observed through this boundary.
6. Report any unresolved contract question instead of inventing policy.

## Output

```markdown
## Contract
Boundary: [function | command | API | job stage]
Signature/shape: [exact shape]
Inputs: [types and preconditions]
Output: [type and observable result]
Errors: [failure outcomes]
Side effects: [writes, calls, state changes]
Dependencies: [real services and test seams]
Next skill: `/skill:tdd`
```

## Completion criterion

The contract is written in the codebase's normal location, has no production behavior, maps to one requirement, assigns a clear responsibility, keeps the interface narrow, and makes the test's inputs and expected observable result unambiguous.
