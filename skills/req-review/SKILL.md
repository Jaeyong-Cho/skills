---
name: req-review
description: Review one approved requirement slice before design, using domain, user, tester, and skeptic perspectives.
disable-model-invocation: true
---

# Requirement Review

Review one focused requirement slice before `/skill:ood`. Read `../references/stage-review.md` first.

## Input

- The requirement card from `/skill:req`, either in the conversation or at a supplied file path.
- Repository context only when needed to verify domain terminology or an existing constraint.

Do not review implementation, classes, interfaces, frameworks, schemas, or database choices. If the requirement is not available, ask for it rather than guessing.

## Review step

Launch one workflowScript that fans out **one fresh, read-only `stage-reviewer` child per persona**:

- Stage: Requirements; Persona: Domain Expert (primary).
- Stage: Requirements; Persona: User (primary).
- Stage: Requirements; Persona: Tester.
- Stage: Requirements; Persona: Skeptic.

Each child receives the requirement card verbatim or its exact path, inspects only its assigned persona, and reports only concrete findings using the shared finding format. Do not send all personas to one reviewer; the independent contexts are the point of this review.

Use the `subagent` tool through one `workflowScript` with `runs.all([...])`; every child uses `agent: "stage-reviewer"`, `context: "fresh"`, and no write tools or edits. The workflow must await all children and return clearly labelled persona reports. The parent is the aggregator: merge duplicate findings, preserve the responsible persona, and classify the combined result. Launch the workflow asynchronously, then wait for its completion result before continuing; do not proceed while it is still detached. If `stage-reviewer` is unavailable, stop and report that `./install.sh` must install `npm:pi-subagents` and the custom agent.

## Parent disposition

Merge duplicate findings. Then present:

1. **Must fix before proceeding** — Critical/Major requirement defects.
2. **Should improve without blocking** — useful but non-blocking changes.
3. **Deliberately deferred** — implementation or design concerns for OOD/TDD.

Do not silently change the requirement. Ask the human to resolve or explicitly accept every blocking finding. Proceed to OOD only when the verdict is `PROCEED` or the human explicitly accepts the remaining risk.

## Completion criterion

The slice still has one purpose and execution boundary; its actor, trigger, outcome, preconditions, relevant failure behavior, and objectively verifiable acceptance criteria are clear; no implementation design has leaked into scope; and every blocking review finding has been resolved or explicitly accepted.
