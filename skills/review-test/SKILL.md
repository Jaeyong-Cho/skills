---
name: review-test
description: Review whether tests provide reliable confidence in important behavior at the lowest reasonable maintenance cost. Use as the testing stage in the review loop or when code and tests change.
disable-model-invocation: true
license: MIT
---

# Test Review

Review only testing strategy and test quality. Do not review production architecture, naming, concurrency, or general code quality unless the test exposes a testing concern.

## Inputs

Accept any combination of:

- **Context:** a directory, file, repository snapshot, existing test conventions, or behavior contract.
- **Changed code:** a diff, branch, commit, pull request, or current `HEAD`.
- **Result evidence:** test output, failures, coverage signal, logs, API responses, or data.

Inspect the changed production path and its tests together. If no test evidence is supplied, say what confidence cannot be established.

## Review checklist

- [ ] [Testing guidelines](../references/testing-guidelines.md) — choose the smallest reliable test level and avoid false confidence.

## Review process

1. Identify the important behavior, contract, or failure the change should protect.
2. Choose the smallest test level that can reliably observe it: unit, integration, API/contract, or end-to-end.
3. Check that tests assert observable behavior rather than implementation details or call order.
4. Check that integration boundaries use realistic integration evidence when correctness depends on a database, framework, filesystem, broker, cache, serialization layer, or external service.
5. Check mocks: use them mainly at boundaries where isolation has real value; avoid mocking internal collaborators by default.
6. Check deterministic, independent, readable, maintainable tests and clear failure messages.
7. For a bug fix, check for a regression case that reproduces the old failure at the lowest reliable level.
8. Avoid demanding tests for trivial delegation, getters, setters, constructors, or private details already covered through public behavior.
9. Rank findings by the importance and failure impact of the behavior left unprotected. Show the highest-impact testing gap or false-confidence risk first, then defer lower-priority findings.

Optimize for confidence in important behavior, not test count or coverage percentage. Do not duplicate coverage across levels unless each test protects a different failure mode.

## Output

Return the review directly in the current session. Do not create or modify a review report file unless explicitly asked. Every finding must have a separate `Example` section using a fenced code block for real test code, input/output data, logs, or an ASCII test-boundary diagram. Use actual evidence values when available; otherwise label the example illustrative.

```markdown
# Testing Review

## Verdict
[Testing is sufficient | Testing gap or smell found | Cannot determine]

## Evidence reviewed
- [context]
- [changed code]
- [test and result evidence]

## Findings
### [Blocker|High|Medium|Low] — [short title]
- **Location:** [test, production behavior, or missing test area]
- **Problem:** [missing, misleading, brittle, over-coupled, or wrongly leveled test]
- **Reason:** [failure mode left unprotected, false confidence, unnecessary maintenance, or weak signal]
### Example

```text
[specific behavior and what the current test would miss or incorrectly accept]
```

- **Recommended handling:** [add or change the smallest reliable test, replace an implementation assertion with an outcome assertion, use realistic integration evidence, or remove meaningless coverage]

## Untested risks
- [important behavior or failure mode with insufficient evidence]
```

A passing test suite is evidence, not proof of sufficient testing. Explain exactly what the tests do and do not establish.
