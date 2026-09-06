---
name: define-req
description: Interview a human to narrow a request into one focused, executable requirement slice with a clear boundary, observable success condition, and safe next action. Use when a request is broad or ambiguous before design or implementation.
disable-model-invocation: true
---

# Define Requirement Slice

Define one focused slice that a human can understand, implement, and verify. Do not turn this into a full product specification or system design.

## Input

- A human's request, goal, or problem description
- Repository context only when it is needed to establish the slice

## Output

One focused requirement slice with its scope, outcome, essential preconditions, acceptance criteria, explicit exclusions, and next action. Return it in the conversation unless the human asks for a file.

## Scope rule

**Exactly one specific slice per invocation.** The slice must stay within one topic or category, one purpose, and one coherent execution boundary.

Keep only what is needed to verify that one outcome. Do not produce a list of sibling requirements. If the request contains another feature, user goal, data area, or release boundary, record it as out of scope or deferred. Do not solve it in this interview.

One slice consists of the main happy path plus the directly relevant edge, boundary, and failure cases for that same outcome. Do not split those scenarios into separate slices unless they introduce a different purpose or execution boundary. It does not need every possible edge case.

## What this skill does not do

Do not use this skill to:

- design the domain model, classes, data model, APIs, or workflow
- enumerate every edge case or failure mode
- choose libraries, algorithms, or infrastructure
- write tests or implementation code

Those belong to `/skill:ood`, `/skill:define-contract`, `/skill:red-test`, and the later skills.

## Human interview

Use a short, focused interview. Ask one plain-language question at a time.

1. Restate the proposed slice and ask the human to confirm or narrow it:

   > “What single topic and outcome should we make executable now?”

2. Ask only the next question needed to define this slice:
   - Who or what uses it?
   - What triggers it?
   - What is the one useful outcome?
   - What input or starting state is essential?
   - What observable result means success?
   - Is there one directly relevant failure or boundary case that changes the scope?
3. After each answer, summarize **Confirmed**, **Still open**, and **Next question**.
4. If the human introduces a different topic, park it under **Deferred topics** and return to the selected slice.
5. Do not ask questions whose answers belong to OOD or implementation. State “deferred to design” instead.
6. Stop when the slice boundary and success condition are clear. Do not keep interviewing for completeness.

## Focused requirement card

```markdown
## Slice
- Topic/category: [one topic]
- Purpose: [one outcome]
- Actor/system: [who or what uses it]
- Trigger/context: [what starts it]

## Scope
- In scope: [the smallest useful behavior]
- Out of scope: [other topics, features, or mechanics]
- Deferred topics: [new topics parked for later]

## Requirement
When [trigger], [actor/system] shall [one action] so that [observable outcome].

## Preconditions and essential dependencies
- [only dependencies required to define or verify this slice]

## Acceptance criteria
| Category | Given | When | Then | Verification |
|---|---|---|---|---|
| Normal | ... | ... | ... | ... |
| Relevant exception/boundary | ... | ... | ... | ... |

## Relevant failure behavior
[Only behavior that changes this slice's scope or safe execution; otherwise “deferred to design”.]

## First executable action
[One safe, reversible action with its expected observable result]
```

Omit the exception row when no directly relevant exception changes the slice. Do not invent empty requirements or fill the card with hypothetical cases.

## Handoff

After this card is confirmed:

1. Use `/skill:ood` only if the slice has meaningful state, domain responsibilities, or object collaboration.
2. Otherwise use `/skill:define-contract` directly.
3. Then use `/skill:red-test`, `/skill:green-implement`, and `/skill:refactor-green`.

Downstream skills must use this slice and must not pull deferred topics back into it.

## Completion criterion

The interview is complete when:

- Exactly one specific slice is defined: one happy path plus its directly relevant edge, boundary, and failure cases.
- Sibling features are not mixed into it.
- The slice covers one understandable topic, purpose, and execution boundary.
- A human can tell what belongs and what does not.
- The actor, trigger, outcome, essential input, and success condition are clear.
- Only directly relevant exception behavior is included.
- The first action is safe, reversible, and testable.
