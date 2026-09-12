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
4. If the report contains a verification gap, Law conflict, Law concern, ambiguous scope, missing evidence, or a WHAT that no longer serves its WHY, stop and return it to `@skills/bible-enact`. Do not add or work around a missing Bible audit script here.
5. Inspect the actual cause and all relevant callers before choosing the smallest safe correction. Do not make a cosmetic change that only fools the Judge.
6. Select exactly one related task per Reform invocation: a cohesive group of violations sharing a root cause, component, Law boundary, or change surface. If the report contains unrelated violations, leave them for later cycles.

## Reform one related task

For the selected related task:

1. State the selected violations, why they belong together, the violated WHATs, protected WHYs, root cause, and intended observable outcome.
2. Make the smallest implementation change that satisfies only this related group and preserves each Law's WHY. Do not fix unrelated violations in the same invocation.
3. Add or strengthen the lowest-cost useful regression check, lint rule, assertion, or other Judge reinforcement for this task when the existing Audit method does not prevent recurrence. Do not add speculative infrastructure.
4. Run the task's Law Audit methods and focused regression checks. Capture commands, exit codes, and observed results.
5. If a check fails, stop with the evidence. Do not weaken a Law or claim success.
6. Run the bundled `@skills/bible-audit/scripts/lint_bible.py` against unchanged Bible roots and re-run `@skills/bible-audit` against the changed state before declaring this task resolved.

Do not bundle unrelated cleanup or violations. If one fix changes another Law's scope or observable behavior, stop for human review rather than silently expanding the task.

## Output

Return:

```markdown
# Bible Reform

## Input
- **Audit:** [report/source]
- **Bible chain:** [global → repository → component, as applicable]
- **Selected related task:** [one cohesive violation group]

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
[Reformed one related task | Partially reformed one related task | Stopped for Enact]
```

Completion criterion: exactly one related task was selected for this invocation; every attempted violation in that task has a cause, a WHAT-and-WHY-preserving change or an explicit blocker, verification evidence, and a fresh audit result; unrelated violations remain unresolved for later cycles; no Bible file was modified.
