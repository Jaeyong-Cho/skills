---
name: req-ood-tdd
description: Orchestrate one complete Requirements → OOD → human approval → TDD pipeline.
disable-model-invocation: true
---

# Requirements → OOD → TDD Pipeline

Run one vertical behavior slice through the complete staged workflow. This skill orchestrates the existing skills; it does not replace their rules or invent a second design process.

## Pipeline

```text
User request
    ↓
/skill:req
    ↓
/skill:ood
    ↓
Human design approval
    ↓
/skill:tdd
```

Run the stages strictly in order. Do not start a later stage while an earlier stage has a blocking finding or an unanswered human checkpoint.

## Start: establish the slice

1. Read the repository instructions and inspect only the context needed to understand the request.
2. Run `/skill:req` to interview the user and define exactly one focused slice. The requirement skill owns its `grill-me` interview.
3. Keep the requirement card, confirmed scope, explicit exclusions, deferred topics, and proposed artifact path as the pipeline state.
4. Do not design classes, interfaces, schemas, libraries, or tests during this stage.
5. Wait for the user's confirmation of the requirement slice before proceeding.

If the request contains multiple features, keep the recommended slice and park the rest as deferred. Never silently widen the pipeline.

## Object-oriented design

Run `/skill:ood` using only the confirmed requirement card and repository evidence.

The OOD stage MUST:

- derive the smallest coherent Objects, responsibilities, data ownership, boundaries, interfaces, workflow, edge cases, failures, and trade-offs;
- avoid implementation code and feature tests;
- preserve the requirement's scope and deferred topics.

## Human approval gate

After OOD, present the complete design brief, open assumptions, and proposed artifact path. Ask exactly:

> Do you approve this design, or should I change anything before writing it to `<proposed-path>`?

Stop and wait. Do not write the design artifact, begin TDD, or reinterpret silence as approval. If the user requests a design change, update the brief before asking again.

After approval, write the confirmed requirement and design artifacts to the approved paths. Carry their exact contents into TDD.

## TDD implementation

Run `/skill:tdd` for one approved acceptance criterion at a time. Preserve its human checkpoint:

```text
Given [starting state], when [action], then [observable result].
```

Complete RED → GREEN → REFACTOR in one invocation. Use the primary public boundary from the OOD contract, keep mocks at external boundaries, and do not implement deferred topics.

## Stop and resume rules

- A user-owned product, scope, architecture, or design decision stops the pipeline until the user answers it.
- If the requirement changes after OOD starts, return to `/skill:ood`; if its behavior or scope changes, re-confirm the requirement first.
- If OOD changes after approval, obtain design approval again before editing code.
- Keep all deferred topics deferred unless the user explicitly starts a new slice.

## Final report

Report:

1. confirmed requirement artifact path;
2. approved design artifact path;
3. changed production and test paths;
4. Red evidence, focused Green result, and regression result;
5. residual risks and the next safe action.

## Completion criterion

The pipeline is complete only when exactly one requirement slice was confirmed, the human approved the design, TDD observed the intended Red failure and achieved Green with regression tests passing, and no unapproved scope remains.
