---
name: review-risk
description: Review material failure and integrity risks introduced by a change. Use for invalid input, dependency failure, external contracts, data loss, partial state, concurrency, retries, or other high-impact risk.
disable-model-invocation: true
license: MIT
---

# Risk Review

Review only material risks that could make the system unsafe, corrupt state, break an external contract, or fail unpredictably. Do not perform a general architecture, style, testing, or maintainability review.

## Inputs

Accept any combination of:

- **Context:** a directory, file, repository snapshot, request, contract, or current behavior.
- **Changed code:** a diff, branch, commit, pull request, or current `HEAD`.
- **Result evidence:** logs, errors, responses, stored data, metrics, stress output, or reproduction steps.

Missing evidence is uncertainty. Do not invent a risk or claim safety without labeling the assumption.

## Risk scope

Select only the risk families relevant to the change:

- **Failure risk:** invalid input, boundary values, missing state, unavailable dependencies, timeouts, malformed data, partial completion, or misleading success.
- **Boundary risk:** external APIs, authentication or authorization boundaries, serialization, migrations, data contracts, vendor behavior, or unsafe dependency leakage.
- **Concurrency risk:** shared state, parallel work, retries, duplicate delivery, cancellation, ordering, shutdown, races, deadlocks, or non-atomic updates.

If none of these risks are present, say that the risk stage is not applicable. Do not manufacture hypothetical risks.

## Review checklist

- [ ] [Error handling](../references/clean-code/07-error-handling.md) — trace invalid input, failure, and recovery paths.
- [ ] [Boundaries](../references/clean-code/08-boundaries.md) — check external contracts and trust boundaries.
- [ ] [Concurrency](../references/clean-code/13-concurrency.md) — check shared state, ordering, retries, and atomicity.
- [ ] [Concurrency appendix](../references/clean-code/appendix-a-concurrency-ii.md) — check deeper interleaving and shutdown cases when relevant.
- [ ] [Code-smell prompts](../references/clean-code/17-smells-and-heuristics.md) — use targeted prompts to expose material risk.

## Review process

1. Identify the changed operation and its blast radius.
2. Select the applicable risk family or families and explain why.
3. Trace the risky path from trigger to caller-visible result and final state.
4. Check the highest-impact realistic failure or interleaving first.
5. Check recovery, rollback, idempotency, ownership, and observability where they affect safety.
6. Rank findings by impact and evidence, not by how unusual the scenario sounds.
7. Report one primary target at a time; defer lower-priority risks until the primary target is resolved.

A risk finding must identify a concrete trigger, the unsafe result, and a practical handling strategy. A passing happy path does not establish safety.

## Output

Return the review directly in the current session. Do not create or modify a review report file unless explicitly asked. Every finding must have a separate `Example` section using a fenced code block for real code, logs, input/output data, or an ASCII state/interleaving diagram.

```markdown
# Risk Review

## Verdict
[No material risk found | Risk found | Risk stage not applicable | Cannot determine]

## Risk families checked
- [failure / boundary / concurrency]

## Evidence reviewed
- [context]
- [changed code]
- [result evidence]

## Findings
### [Blocker|High|Medium|Low] — [short title]
- **Location:** [file, symbol, dependency, operation, or result]
- **Risk trigger:** [specific input, state, dependency event, or interleaving]
- **Problem:** [unsafe, corrupt, misleading, unavailable, duplicated, or non-atomic result]
- **Reason:** [impact and why the current handling cannot safely contain it]

### Example

```text
[real code, logs, data, or ASCII diagram showing the trigger and result]
```

- **Recommended handling:** [validation, explicit error, contract isolation, transaction, idempotency, synchronization, rollback, timeout, or recovery strategy]
- **Evidence strength:** [confirmed / strongly indicated / unverified]

## Unverified risks
- [important risk and the missing evidence]
```

Do not recommend broad refactoring unless it is required to remove the material risk.
