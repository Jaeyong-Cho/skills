---
name: one-requirement
description: Turn a vague request into exactly one small, executable requirement with observable acceptance criteria, dependencies, failure behavior, and one safe next action. Use when a request is too broad, ambiguous, or needs to be made actionable before implementation.
disable-model-invocation: true
---

# One Requirement

Turn the request into one requirement that a person or agent can execute and verify without guessing.

## Rules

- Produce exactly one outcome. Split independent outcomes instead of hiding them behind “and”.
- Specify **what** must happen, not an implementation design.
- Ask only questions whose answers can change scope, acceptance, risk, or verification.
- Inspect the repository or documents before asking for facts that can be found there.
- If an answer requires running something to know, run a small experiment instead of guessing.
- Do not implement unless the user explicitly asks for implementation.

## Workflow

1. State the desired outcome in the user's words.
2. Write a candidate requirement:

   > When **[trigger]**, **[actor/system]** shall **[action]** so that **[observable value]**.

3. Check the minimum contract:
   - actor or system
   - trigger
   - inputs and preconditions
   - one observable output or state change
   - failure behavior
   - verification method
4. Classify the next move:
   - **Act directly** when the change is small, isolated, reversible, and easy to verify.
   - **Run a spike** when the unknown is factual or environment-specific.
   - **Think/design first** when the change affects production data, rollback, security, shared contracts, or other irreversible behavior.
5. Ask the single highest-impact unanswered question. Repeat only until the next action is safe, testable, and reversible. State low-risk assumptions instead of conducting an endless interview.
6. Produce the requirement card below.

## Requirement card

```markdown
## Requirement
When [trigger], [actor/system] shall [one action] so that [observable value].

## Scope
- In scope: [smallest slice]
- Out of scope: [explicitly excluded work]

## Preconditions and dependencies
- [required state, data, tool, or service]

## Acceptance criteria
| Category | Given | When | Then | Verification |
|---|---|---|---|---|
| Normal | ... | ... | ... | ... |
| Exception/Boundary | ... | ... | ... | ... |

## Failure behavior
[What stops, retries, rolls back, or gets reported. Use “not specified” rather than inventing policy.]

## Next executable action
[One command or small action, with the expected observable result.]
```

Include only relevant acceptance-criteria rows; every row must be observable and have a verification method. Use a unit test, integration test, query, or command when possible. Use manual verification only when automation cannot check the result.

## Quality gate

The requirement is ready when:

- It describes one outcome, not a feature bundle.
- A developer can start without guessing the trigger, input, output, or success condition.
- Failure behavior is stated or explicitly marked unknown.
- The next action is safe, reversible, and testable.
- Another person can verify completion without asking what “works” means.

If it is not ready, ask one focused question or propose one time-boxed experiment; do not expand into a full system design.
