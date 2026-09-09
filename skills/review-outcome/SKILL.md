---
name: review-outcome
description: Review whether a change delivers its intended, observable outcome. Use when checking behavior against a request, goal, acceptance statement, user flow, or supplied result evidence.
disable-model-invocation: true
license: MIT
---

# Outcome Review

Review only whether the change delivers the intended observable outcome. Do not review architecture, style, concurrency, test design, or general code quality.

## Inputs

Accept any combination of:

- **Context:** a directory, file, repository snapshot, issue, request, or stated goal.
- **Changed code:** a diff, branch, commit, pull request, or current `HEAD`.
- **Result evidence:** logs, command output, API responses, screenshots, stored data, or other observed results.

Treat missing inputs as unknowns, not as permission to invent requirements. State which evidence was available.

## Review process

1. Identify the intended outcome in concrete terms: who or what acts, what starts the flow, and what should be observable afterward.
2. Trace the changed path from its entry point to its observable result.
3. Compare the actual behavior and supplied result evidence with the intended outcome.
4. Check the normal flow, relevant alternate flows, limits, and failure outcomes only when they affect the intended result.
5. Report only outcome gaps, contradictions, or unverified claims.

Do not infer success from code shape alone when result evidence is available. Do not treat a passing command as proof of the product outcome unless the command checks that outcome.

## Reference material

- [Intent criteria](../references/intent-checklist.md)
- [Story criteria](../references/req-checklist.md)
- [Requirements engineering](../references/requirement-engineering.md)

## Output

Return the review directly in the current session. Do not create or modify a review report file unless explicitly asked.

Write for a human. Every finding must have a separate `Example` section. Put the example in a fenced code block using the most useful form: real code, JSON, logs, input/output data, or an ASCII diagram. Use actual values from the evidence when available; otherwise label it illustrative.

```markdown
# Outcome Review

## Verdict
[Meets outcome | Partially meets outcome | Does not meet outcome | Cannot determine]

## Evidence reviewed
- [context]
- [changed code]
- [result evidence]

## Findings
### [High|Medium|Low] — [short title]
- **Location:** [file, symbol, line, or result]
- **Problem:** [what observable outcome is missing, wrong, or unproven]
- **Reason:** [why this prevents or threatens the intended result]
### Example

```text
[concrete input/flow and observed versus expected result]
```

- **Recommended handling:** [specific strategy to correct or verify it]

## Not assessed
- [missing context or behavior outside this review]
```

If no finding exists, say so plainly and name the evidence that supports the verdict. Do not manufacture recommendations.
