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

Launch exactly one fresh, read-only `stage-reviewer` sub-agent with this task:

- Stage: Requirements.
- Personas: Domain Expert (primary), User (required), Tester, Skeptic. The User persona must be included even when the actor is an operator, administrator, or API client.
- Artifact: include the requirement card verbatim or give its exact path.
- Scope: inspect the artifact and relevant repository evidence; report only concrete findings.
- Output: use the shared finding format and end with Must fix, Should improve, Deliberately deferred, and `Verdict: BLOCK | PROCEED`.

Use the `subagent` tool through a `workflowScript`, with `agent: "stage-reviewer"`, `context: "fresh"`, and no write tools or edits. The workflow body must await the child (`const result = await runs.run("stage-review", {...}); return result.output;`). Launch the workflow asynchronously, then wait for its completion result before continuing; do not proceed while it is still detached. If `stage-reviewer` is unavailable, stop and report that `./install.sh` must install `npm:pi-subagents` and the custom agent.

## Parent disposition

Merge duplicate findings. Then present:

1. **Must fix before proceeding** — Critical/Major requirement defects.
2. **Should improve without blocking** — useful but non-blocking changes.
3. **Deliberately deferred** — implementation or design concerns for OOD/TDD.

Do not silently change the requirement. Ask the human to resolve or explicitly accept every blocking finding. Proceed to OOD only when the verdict is `PROCEED` or the human explicitly accepts the remaining risk.

## Completion criterion

The slice still has one purpose and execution boundary; its actor, trigger, outcome, preconditions, relevant failure behavior, and objectively verifiable acceptance criteria are clear; no implementation design has leaked into scope; and every blocking review finding has been resolved or explicitly accepted.
