---
name: bible-loop
description: Run a bounded Bible audit-to-reform loop with subagents, stopping cleanly or returning evidence for Bible revision.
disable-model-invocation: true
license: MIT
---

# Bible Loop

Orchestrate `bible-audit → bible-reform` until the target is compliant or the retry limit is reached. This is the execution loop; it does not enact or revise Laws. Read `../references/bible-driven-development.md` before starting.

## Inputs

Accept:

- Bible path and implementation target (otherwise resolve `~/.bible/`, the repository `.bible/`, and the nearest component `.bible/`);
- optional scope or violation IDs;
- optional maximum loop count, such as `max 5`, `5 iterations`, or `loop=5`.

The default maximum is **3**. Parse a positive integer; if it is missing, invalid, zero, or negative, use 3 and state that assumption. Count each complete audit/reform cycle, including a clean audit as the final cycle.

A `.bible/` governs its directory tree. Nested Bibles inherit Laws from their nearest parent and may add narrower Laws, but may not weaken inherited Laws. Pass the complete root-to-target Bible chain to every subagent.

## Protocol

1. Establish and show the target, Bible chain, scope, maximum, and available evidence. Run the bundled `@skills/bible-audit/scripts/lint_bible.py` against each Bible root. If no repository Bible exists, stop and invoke `@skills/bible-enact`; do not invent one.
2. For each cycle, dispatch a read-only audit subagent before any reform subagent. Use the explicit `subagent()` mechanism and pass the same current-state target, Bible chain, scope, and evidence. The audit subagent follows `@skills/bible-audit`, returns its complete report, and MUST NOT edit files.
3. If the audit is `Compliant`, stop successfully. If it is `Cannot determine`, stop and show the missing evidence; do not ask Reform to guess.
4. If violations exist and the cycle limit has not been reached, dispatch a reform subagent with the audit report verbatim. Use a worker-capable subagent for Reform, but instruct it to follow `@skills/bible-reform`, change only implementation-side files, and return its complete report. It MUST NOT edit any Bible file.
5. After Reform returns, verify that every Bible in the chain is unchanged (for example, compare `git diff -- [Bible paths]` or recorded hashes), collect its checks and fresh audit result, then begin the next cycle from the current state. If a Bible changed, stop as `Enact required`. Do not reuse a pre-fix audit result.
6. At the limit, stop. Show every unresolved violation, its latest evidence, failed or missing checks, changed files, and any Law concerns. State that this evidence can be supplied to `@skills/bible-enact` for a human WHY/WHAT decision; Enact decides whether amendment or repeal is justified. Do not amend the Bible automatically.

Use this dispatch shape, adapting paths and context:

```typescript
subagent({
  name: `Bible-Audit-${cycle}`,
  agent: "scout",
  task: "Follow @skills/bible-audit. Read-only audit of [target] against [Bible chain]. Return the complete report with one result per applicable Law and concrete command/path evidence. Do not edit or delegate."
});
```

Then, only when the audit has violations:

```typescript
subagent({
  name: `Bible-Reform-${cycle}`,
  agent: "worker",
  task: "Follow @skills/bible-reform for [target]. Here is the current audit report: [verbatim report]. Preserve each Law's WHY and WHAT. Edit implementation-side files only; never edit any `.bible/` file. Run focused checks and return the complete reform report."
});
```

Do not dispatch audit and reform in parallel: Reform depends on the current audit. If Reform reports a Law concern, ambiguity, failed check, or an attempted Bible change, stop immediately and surface it for Enact/human review.

## Session output

```markdown
# Bible Loop

## Configuration
- **Target:** ...
- **Bible chain:** ...
- **Maximum cycles:** ...

## Cycle 1
- **Audit:** [report/verdict]
- **Reform:** [report/checks, or not run]

## Final status
[Compliant | Stopped: cannot determine | Stopped: maximum reached | Stopped: Enact required]

## Evidence for next Enact
- [unresolved violation and latest evidence; Enact decides whether a Law change is justified]
```

Completion criterion: every cycle has a current audit report, every reform was based on that report and verified, no Bible was edited by the loop, and the final status plus complete unresolved evidence is shown.
