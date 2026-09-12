---
name: bible-reform
description: Correct implementation violations reported by bible-audit while preserving each Law's WHY and strengthening its verification.
disable-model-invocation: true
license: MIT
---

# Bible Reform

Restore implementation compliance from an Audit report. Reform may change implementation, tests, configuration, and verification support; it MUST NOT amend, weaken, repeal, or otherwise edit any file under a `.bible/`.

## Inputs and safeguards

1. Read `../references/bible-driven-development.md`.
2. Require a current `bible-audit` report, or run `@skills/bible-audit` first. Do not fix from a vague claim or stale evidence.
3. Read the violated Law's full parent/child chain, including both WHY and WHAT, before editing.
4. If the report contains a Law concern, an ambiguous scope, missing evidence, or a WHAT that no longer serves its WHY, stop and return it to `@skills/bible-enact`. Do not work around the Law.
5. Inspect the actual cause and all relevant callers before choosing the smallest safe correction. Do not make a cosmetic change that only fools the Judge.

## Reform each violation

For each selected violation, in priority order:

1. State the violated WHAT, protected WHY, root cause, and intended observable outcome.
2. Make the smallest implementation change that satisfies WHAT and preserves WHY.
3. Add or strengthen the lowest-cost useful regression check, lint rule, assertion, or other Judge reinforcement when the existing Audit method does not prevent recurrence. Do not add speculative infrastructure.
4. Run the Law's Audit method and the focused regression check. Capture commands, exit codes, and observed results.
5. If the check fails, stop with the evidence. Do not weaken the Law or claim success.
6. Run the bundled `@skills/bible-audit/scripts/lint_bible.py` against unchanged Bible roots and re-run `@skills/bible-audit` against the changed state before declaring the violation resolved.

Do not bundle unrelated cleanup. If one fix changes another Law's scope or observable behavior, stop for human review rather than silently expanding the task.

## Output

Return:

```markdown
# Bible Reform

## Input
- **Audit:** [report/source]
- **Bible chain:** [global → repository → component, as applicable]

## Changes
### VIOLATION-001 — [title]
- **Law / WHY / WHAT:** [identifiers and concise text]
- **Root cause:** [evidence-based cause]
- **Changed:** [files and behavior]
- **Reinforcement:** [test, Judge, or `None` with reason]
- **Checks:** [commands, exit codes, observed result]
- **Re-audit:** [Compliant / remaining violation / Cannot determine]

## Unresolved
- [blocked item and evidence, or `None`]

## Verdict
[Reformed | Partially reformed | Stopped for Enact]
```

Completion criterion: each attempted violation has a cause, a WHAT-and-WHY-preserving change or an explicit blocker, verification evidence, and a fresh audit result; no Bible file was modified.
