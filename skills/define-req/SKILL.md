---
name: define-req
description: Interview a human to narrow a vague request into one coherent, executable requirement slice with clear scope, acceptance criteria, dependencies, failure behavior, and a safe next action. Use when a request contains multiple topics, is too broad, or needs clarification before implementation.
disable-model-invocation: true
---

# Define Requirement Slice

Interview the human and produce one coherent requirement slice. The slice may contain normal, boundary, and failure requirements, but they must all belong to the same topic, category, purpose, and execution boundary.

## Input

- A human's vague request, goal, or problem description
- Available repository, documents, and constraints when they exist

## Output

A requirement set for one specific slice: a human-understandable scope, related requirements, acceptance criteria, dependencies, failure behavior, explicit non-goals, and one next action. Return it in the conversation unless the human asks for a file.

## Hard scope rule

Do not combine various things merely because they are in the same project or sentence.

Keep requirements together only when they share:

- the same topic or category
- the same purpose and actor/system
- the same context or state
- one coherent execution boundary
- acceptance criteria that verify the same outcome

Split or defer a request when it combines unrelated features, different users, different purposes, separate release boundaries, or unrelated data/state. Do not solve every discovered topic in the same interview.

A requirement set may contain multiple rows for one slice—for example, normal behavior, an invalid input, and a dependency failure. Those are scenarios of one outcome, not unrelated requirements.

## Human interview

Run an interactive interview; do not produce a large questionnaire.

1. Start by restating the candidate slice in plain language and ask the human to confirm or narrow it:

   > “Which one topic should we make executable now? What should be included, and what should wait?”

2. Ask **one question at a time**, in plain language. Ask only questions that can change scope, acceptance, risk, or verification.
3. After each answer, briefly update:
   - **Confirmed** — decisions now fixed
   - **Still open** — the next uncertainty
4. Do not silently fill in product decisions. State a low-risk assumption or ask the human.
5. If the answer introduces a different topic, park it under **Deferred topics** and return to the selected slice.
6. Confirm the scope boundary before asking detailed edge-case questions.
7. Do not draft the final requirement set until the slice has a clear outcome, boundary, and verification method.

## Interview order

Use this order, skipping only what is already known:

1. **Topic and boundary** — What single topic/category are we solving now? What is explicitly not part of it?
2. **Actor and value** — Who uses or depends on it? What useful outcome do they get?
3. **Trigger and context** — What event or starting state begins it?
4. **Normal outcome** — What should happen on the ordinary successful path?
5. **Inputs and dependencies** — What data, state, tools, or services are required?
6. **Failure and boundary behavior** — What should happen for empty, invalid, duplicate, unavailable, or maximum cases that are relevant to this slice?
7. **Verification** — What observable result proves it works, and what is the cheapest trustworthy check?
8. **First action** — What small, safe, reversible action can start implementation or an experiment?

Do not ask implementation questions such as “Should this use a class or a hashmap?” during this interview. Save responsibility, data model, APIs, workflow mechanics, and trade-offs for `/skill:ood` when the slice needs OOD.

## Bounded scope check

Before finishing, scan the selected slice for:

- boundary values: zero, one, empty, maximum, negative where meaningful
- state transitions the requested behavior allows, including duplicate calls
- concurrency, only if the system is actually concurrent
- failure of each named dependency once
- invalid or adversarial input at each trust boundary

For every candidate case, name the concrete input, state, or call sequence that triggers it, then mark it **in scope**, **out of scope**, or **deferred with a condition**. Only in-scope cases need acceptance criteria now. Do not invent mechanics before `/skill:ood` defines the actual data model and APIs. A hypothetical case with no concrete trigger is recorded once and not pursued.

## Requirement set

```markdown
## Slice
- Topic/category: [one coherent topic]
- Purpose: [the outcome this slice provides]
- Actor/system: [who or what uses it]
- Trigger/context: [what starts it]

## Scope
- In scope: [the boundary of this slice]
- Out of scope: [unrelated topics and excluded behavior]
- Deferred topics: [new topics parked for later, if any]

## Requirements

### R{id}: [short name]
When [trigger], [actor/system] shall [one action] so that [observable value].

[Repeat only for scenarios belonging to this same slice]

## Preconditions and dependencies
- [required state, data, tool, or service]

## Acceptance criteria
| Requirement | Category | Given | When | Then | Verification |
|---|---|---|---|---|---|
| R{id} | Normal | ... | ... | ... | ... |
| R{id} | Exception/Boundary | ... | ... | ... | ... |

## Failure behavior
[What stops, retries, rolls back, waits, or gets reported. Use “not specified” rather than inventing policy.]

## Open decisions
[Only decisions that block safe implementation or verification]

## First executable action
[One safe, reversible action or experiment with its expected observable result]
```

## Handoff

After this slice is complete:

1. Use `/skill:ood` when it has meaningful state, domain responsibilities, or object collaboration.
2. Otherwise use `/skill:define-contract` directly.
3. Then use `/skill:red-test`, `/skill:green-implement`, and `/skill:refactor-green`.

Downstream skills must take this selected slice, not the parked topics. They must not combine unrelated requirements into one contract or test.

## Completion criterion

The interview is complete when:

- The request is bounded to one topic/category and one coherent purpose.
- A human can tell what belongs in the slice and what does not.
- The actor, trigger, outcome, inputs, success condition, and relevant failure behavior are clear.
- Related scenarios have observable acceptance criteria and verification methods.
- Unrelated topics are explicitly deferred or out of scope.
- The first action is safe, reversible, and testable.
