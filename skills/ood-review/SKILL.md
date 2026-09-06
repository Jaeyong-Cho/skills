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

Launch one workflowScript that fans out **one fresh, read-only `stage-reviewer` child per applicable persona**:

- Stage: OOD; Persona: Implementer (primary).
- Stage: OOD; Persona: Future Developer (primary).
- Stage: OOD; Persona: Simplifier.
- Stage: OOD; Persona: Security/SRE only when the slice has material security, reliability, distributed-system, or operational risk.

Each child receives the requirement and design verbatim or their exact paths, inspects only its assigned persona, and reports only evidence-backed findings. Do not send all personas to one reviewer; the independent contexts are the point of this review.

Use the `subagent` tool through one `workflowScript` with `runs.all([...])`; every child uses `agent: "stage-reviewer"`, `context: "fresh"`, and no write tools or edits. The workflow must await all children and return clearly labelled persona reports. The parent is the aggregator: merge duplicate findings, preserve the responsible persona, and classify the combined result. Launch the workflow asynchronously, then wait for its completion result before the human design checkpoint; do not proceed while it is still detached. If `stage-reviewer` is unavailable, stop and report that `./install.sh` must install `npm:pi-subagents` and the custom agent.

## Parent disposition

Merge duplicate findings. Then present:

1. **Must fix before proceeding** — Critical/Major responsibility, boundary, dependency, failure, or coherence defects.
2. **Should improve without blocking** — useful but non-blocking simplifications.
3. **Deliberately deferred** — implementation-level concerns for TDD or product questions outside the slice.

Apply only approved design changes. Ask the human the single design question from `/skill:ood` after the review is incorporated; do not write the design or start TDD while a blocking finding remains unresolved.

## Completion criterion

Every in-scope acceptance criterion has an owner and observable boundary; responsibilities and data ownership are coherent; applicable interfaces and failures are explicit; no abstraction lacks a current reason; concrete likely change scenarios do not expose unacceptable rigidity; and every blocking finding is resolved or explicitly accepted.
