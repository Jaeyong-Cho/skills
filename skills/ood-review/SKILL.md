---
name: ood-review
description: Review one OOD and contract brief before TDD, using implementer, future-developer, simplifier, and risk-based operations perspectives.
disable-model-invocation: true
---

# OOD Review

Review one approved requirement's object-oriented design and boundary contracts before `/skill:tdd`. Read `../references/stage-review.md` first.

## Input

- The requirement slice from `/skill:req`.
- The OOD and contract brief from `/skill:ood`, either in the conversation or at a supplied file path.
- Relevant repository conventions and existing code.

Review the design, responsibilities, boundaries, collaborations, dependencies, workflow, edge cases, failure modes, and trade-offs. Do not demand implementation details that belong to TDD.

## Review step

Launch exactly one fresh, read-only `stage-reviewer` sub-agent with this task:

- Stage: OOD.
- Personas: Implementer (primary), Future Developer (primary), Simplifier, and Security/SRE only when the slice has material risk.
- Artifacts: include the requirement and design verbatim or give their exact paths.
- Scope: inspect the design and relevant repository evidence; use concrete likely change scenarios; report only evidence-backed findings.
- Output: use the shared finding format and end with Must fix, Should improve, Deliberately deferred, and `Verdict: BLOCK | PROCEED`.

Use the `subagent` tool through a `workflowScript`, with `agent: "stage-reviewer"`, `context: "fresh"`, and no write tools or edits. The workflow body must await the child (`const result = await runs.run("stage-review", {...}); return result.output;`). Launch the workflow asynchronously, then wait for its completion result before the human design checkpoint; do not proceed while it is still detached. If `stage-reviewer` is unavailable, stop and report that `./install.sh` must install `npm:pi-subagents` and the custom agent.

## Parent disposition

Merge duplicate findings. Then present:

1. **Must fix before proceeding** — Critical/Major responsibility, boundary, dependency, failure, or coherence defects.
2. **Should improve without blocking** — useful but non-blocking simplifications.
3. **Deliberately deferred** — implementation-level concerns for TDD or product questions outside the slice.

Apply only approved design changes. Ask the human the single design question from `/skill:ood` after the review is incorporated; do not write the design or start TDD while a blocking finding remains unresolved.

## Completion criterion

Every in-scope acceptance criterion has an owner and observable boundary; responsibilities and data ownership are coherent; applicable interfaces and failures are explicit; no abstraction lacks a current reason; concrete likely change scenarios do not expose unacceptable rigidity; and every blocking finding is resolved or explicitly accepted.
