---
name: define-req
description: Turn a vague request into a small set of executable, testable requirements with observable acceptance criteria, dependencies, failure behavior, and a safe next action. Use when a request is broad, ambiguous, or needs clarification before implementation.
disable-model-invocation: true
---

# Define Requirements

Turn a request into requirements that a person or agent can execute and verify without guessing.

## Input

- A user's vague request, goal, or problem description
- Available repository, documents, and constraints when they exist

## Output

A requirement set containing a coherent scope, related requirements, acceptance criteria, dependencies, failure behavior, explicit non-goals, a first executable slice, and one next action. It is the input to `/skill:ood` or `/skill:define-contract`.

## Rules

- Do not force the request into one requirement. Preserve related requirements when they belong to the same requested outcome.
- Split independent outcomes when they need different acceptance criteria, dependencies, or execution boundaries.
- Specify **what** must happen, not an implementation design.
- Ask only questions whose answers can change scope, acceptance, risk, or verification.
- Inspect the repository or documents before asking for facts that can be found there.
- If an answer requires running something to know, run a small experiment instead of guessing.
- Do not implement unless the user explicitly asks for implementation.
- For stateful or domain behavior, identify the likely owner of the state or rule without forcing a class design into the requirement.
- Keep execution order separate from responsibility: a pipeline stage is not automatically a domain object.
- Include core actions, hard constraints/invariants, and explicit non-goals; do not turn implementation details into requirements.
- Bound the scope to one understandable topic or category: related actors, purpose, state, and acceptance criteria should belong together.
- Do not measure scope quality by sentence count or requirement count. Split only when the request contains unrelated topics, different purposes, or a real execution boundary.

## Workflow

1. State the desired outcome in the user's words.
2. Identify the actors or systems, triggers, value, inputs, outputs, constraints, and failure concerns.
3. Bound the scope before decomposing it:
   - one understandable topic or category
   - one coherent purpose and context
   - one change boundary, unless related requirements must be delivered together
   - core verbs/actions and hard invariants
   - explicit non-goals
   If the request mixes unrelated topics or purposes, ask one scope question or split it at that real boundary.
4. Group the request into the smallest coherent requirements. Each requirement should have one primary observable outcome; do not split merely to make a longer checklist.
5. For each requirement, write:

   > When **[trigger]**, **[actor/system]** shall **[action]** so that **[observable value]**.

6. Check the minimum contract for every requirement:
   - actor or system
   - trigger
   - inputs and preconditions
   - observable output or state change
   - failure behavior
   - verification method
7. Check the OOD implications without designing the solution:
   - Which behavior or state has a clear owner?
   - Is the requirement mixing intent, business rules, and technical mechanisms?
   - Is a proposed boundary needed for a real responsibility or only for future flexibility?
8. Run a bounded requirements edge-case scan: boundary values, allowed state transitions, concurrency if relevant, named dependency failures, and invalid input at trust boundaries. Record scope decisions now; leave mechanics for OOD design.
9. Classify the next move:
   - **Act directly** when the change is small, isolated, reversible, and easy to verify.
   - **Run a spike** when the unknown is factual or environment-specific.
   - **Think/design first** when the change affects production data, rollback, security, shared contracts, or other irreversible behavior.
10. Ask the single highest-impact unanswered question. Repeat only until the next action is safe, testable, and reversible. State low-risk assumptions instead of conducting an endless interview.
11. Produce the requirement set below. If several requirements are present, identify which one is the first executable slice.

## Requirement set

Use the following as a stable handoff schema. Keep the field names, but repeat or omit requirement and acceptance-criteria rows as needed; do not invent empty requirements.

```markdown
## Desired outcome
[What the user wants to change or obtain]

## Requirements

### R{id}: [short name]
When [trigger], [actor/system] shall [one primary action] so that [observable value].

[Repeat for each related requirement]

## Scope
- Human-readable scope: [one topic/category, its purpose, and its boundary in plain language]
- In scope: [requirements covered by this slice]
- Out of scope: [explicitly excluded work]

## Preconditions and dependencies
- [required state, data, tool, or service]

## Acceptance criteria
| Requirement | Category | Given | When | Then | Verification |
|---|---|---|---|---|---|
| R1 | Normal | ... | ... | ... | ... |
| R1 | Exception/Boundary | ... | ... | ... | ... |

## Failure behavior
[What stops, retries, rolls back, or gets reported. Use “not specified” rather than inventing policy.]

## First executable slice
[The first requirement to take through contract -> red test -> implementation -> refactor.]

## Next executable action
[One command or small action, with the expected observable result.]
```

Include only relevant acceptance-criteria rows; every row must be observable and have a verification method. Use a unit test, integration test, query, or command when possible. Use manual verification only when automation cannot check the result. The schema is strict at handoff boundaries; the number of requirements, questions, and criteria is flexible.

## Handoff

After the requirement set is ready, use the separate skills:

1. `/skill:ood` when the behavior has meaningful state or responsibility assignment
2. `/skill:define-contract`
3. `/skill:red-test`
4. `/skill:green-implement`
5. `/skill:refactor-green`

If the first slice has not been selected, ask the user to select it before handing off. OOD design may cover the related requirement set, but downstream contract and test skills must take one selected slice at a time.

## Completion criterion

The requirement set is ready when:

- Related requirements are captured without artificial one-item limitation.
- The scope is one understandable topic or category with a clear purpose and boundary.
- Independent outcomes are split enough to have clear acceptance criteria and execution boundaries.
- A developer can start the first slice without guessing its trigger, input, output, or success condition.
- Failure behavior is stated or explicitly marked unknown.
- The next action is safe, reversible, and testable.
- Another person can verify completion without asking what “works” means.

If it is not ready, ask one focused question or propose one time-boxed experiment; do not expand into a full system design.
