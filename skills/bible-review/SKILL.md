---
name: bible-review
description: Review implementation against its effective Bible Laws, show evidence for violations, and apply only human-confirmed implementation fixes.
disable-model-invocation: true
license: MIT
---

# Bible Review

Run a human-gated review of implementation compliance with the effective Bible Laws. This is the review counterpart to `bible-loop`: it may propose and verify implementation fixes, but never changes Laws automatically.

## Inputs

Accept any combination of:

- **Target:** a repository, component, file, diff, branch, or current behavior.
- **Bible path:** supplied root or the resolved global, repository, and component chain.
- **Scope:** optional Law IDs, categories, paths, or behaviors to review.
- **Evidence:** tests, commands, logs, screenshots, or other observed results.

Missing evidence is `Cannot determine`, not compliance.

## Review protocol

1. Establish and show the target, complete parent-to-child Bible chain, scope, and available evidence. Read `../references/bible-driven-development.md` and run `@skills/bible-audit/scripts/lint_bible.py` against every Bible root. If no applicable repository Bible exists, stop and recommend `@skills/bible-enact`; do not invent or amend a Law.
2. Dispatch one read-only audit subagent through the active host's native subagent mechanism. On Pi, use the `subagent()` call described in `../references/pi-custom-subagent.md`. Give it the same target, Bible chain, scope, and evidence. It must follow `@skills/bible-audit`, inspect every applicable inherited and local Law, return one result per Law, and make no edits or further delegation.
3. Show the complete audit result, including clean Laws, violations, `Cannot determine` results, and separate Law concerns. Do not reinterpret a precise WHAT because its WHY seems satisfied.
4. If the result is `Compliant` and has no verification gap or Law conflict, accept the review. If it contains a Law conflict, stop immediately and route the contradictory Laws to `@skills/bible-enact`; do not choose a winning Law. If it contains `Cannot determine`, a verification gap, a Law concern, or a critical/Blocker violation, stop and return the evidence for human handling or `@skills/bible-enact`.
5. For each remaining non-blocking violation, in priority order, show the Law's WHY, exact WHAT, observed actual state, evidence, smallest safe implementation fix, and focused check. Ask for explicit human confirmation before editing or dispatching any reform work. Never fix a violation by changing `.bible/` files.
6. After confirmation, apply only that implementation-side fix, or dispatch a worker-capable subagent to follow `@skills/bible-reform` for a larger fix. Preserve the Law's WHY and WHAT. Run the focused check, verify every Bible root is unchanged, and dispatch a fresh audit against the updated state before handling the next finding.
7. Continue until every applicable Law is compliant, the human stops or defers a fix, or a stop condition is reached. Never reuse a pre-fix audit result or declare success from a passing command that does not observe the Law's WHAT.

## Review controls

- **Current state wins:** every re-review uses the latest implementation and evidence.
- **Law authority:** WHAT is the compliance test; WHY explains its protected intent and exposes possible Law concerns.
- **No automatic Law changes:** amendment, repeal, or reorganization belongs to `@skills/bible-enact` after human review.
- **Human gate:** no implementation edit or reform dispatch occurs before explicit confirmation for that proposed fix.
- **No hidden findings:** show every Law result and every unresolved violation; list deferred work with its reason.
- **No false acceptance:** missing, stale, or nondeterministic evidence remains `Cannot determine`; preserve and follow every `AI VERIFICATION METHOD` alert.

## Session output

Use this structure:

```markdown
# Bible Review

## Configuration
- **Target:** ...
- **Bible chain:** ...
- **Scope:** ...
- **Evidence:** ...

## Review cycle [number]

### Law results
| Law | Scope | Result | Evidence |
|---|---|---|---|
| LAW-... | ... | Compliant / Violated / Cannot determine | ... |

### Verification gaps
- [LAW-... — command-verifiable WHAT without a matching audit script, or `None`]

### AI verification methods
- [LAW-... — complete `AI VERIFICATION METHOD` alert and follow-up result, or `None`]

### Law conflicts
- [conflicting Law IDs, incompatible requirements, scope, and evidence, or `None`]

### Finding [number]
- **Law:** LAW-...
- **WHY:** ...
- **Expected (WHAT):** ...
- **Actual:** ...
- **Evidence:** ...
- **Proposed fix:** ...
- **Action:** awaiting confirmation / confirmed / deferred / applied
- **Check:** ...

## Final status
[Compliant | Stopped: Law conflict — Enact required | Stopped: verification gap | Stopped: cannot determine | Stopped: Law concern | Stopped: human decision | Deferred findings]

## Deferred
- [Law, reason, and evidence]
```

## Completion criterion

The review is complete only when the latest audit covers every applicable inherited and local Law, every accepted fix has explicit human confirmation and a focused check, every changed state has been freshly audited, no Bible file was changed, and the final status plus complete evidence is shown.
