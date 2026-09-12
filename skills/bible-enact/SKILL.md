---
name: bible-enact
description: Define, amend, or repeal repository Laws from human intent using the Bible model. Start with a grill-me interview when intent or scope is not already settled.
disable-model-invocation: true
license: MIT
---

# Bible Enact

Turn confirmed human intent into durable Laws. Enact is the Bible's legislative authority; it does not edit implementation code.

## Start

1. Read `../references/bible-driven-development.md`.
2. Start with `@skills/grill-me` unless this session already contains a confirmed, narrow intent and scope. Do not write a Law before the interview reaches shared understanding and the human confirms it.
3. Locate the governing `.bible/` roots. Use the paths supplied by the human; otherwise resolve `~/.bible/`, the repository's `.bible/`, and any nearer component `.bible/`. If no repository Bible exists, ask where to create it and recommend `.bible/` at the repository root.
4. Read the relevant indexes and the full applicable parent-to-child Bible chain before proposing a change.

A `.bible/` governs its directory tree. A nested `.bible/` is a sub-Bible: it inherits Laws from its nearest parent Bible, then adds narrower Laws. A child may not weaken or contradict an inherited Law. Report a conflict for human enactment instead of silently overriding it. Use an explicit parent declaration only when the repository has one.

## Enactment

For each proposed Law:

1. Establish the underlying **WHY** before settling the **WHAT**.
2. Define a stable unique identifier and a narrow scope.
3. Make WHAT precise, observable, and testable where possible. Use `MUST`/`SHALL` for requirements.
4. Define an Audit method and expected Evidence. Prefer a deterministic Judge: test, compiler, linter, AST/dependency query, CLI command, or small script.
5. Check that the Law does not duplicate, contradict, or unnecessarily broaden an existing inherited or local Law.
6. Show the proposed create, amendment, or repeal and obtain explicit human approval before writing it.

Every Law document under `.bible/laws/<category>/<subcategory>/` MUST contain `## WHY` and `## WHAT`. This is the recommended complete shape:

```markdown
# LAW-<ID> — <Title>

## WHY

Why this Law exists and what risk, problem, or intent it protects.

## WHAT

What MUST remain true, stated precisely.

## Scope

Where this Law applies.

## Audit

How compliance is determined and what Evidence must be recorded.
```

Amending a Law requires preserving its WHY unless the human explicitly decides that the intent changed. Repeal only when the protected WHY no longer exists or is intentionally retired. Preserve the Law's history when the repository has an established convention; otherwise keep the diff small and record the reason in the session.

## Output

Return:

- Bible paths and parent chain;
- confirmed intent and WHY;
- proposed or applied Law changes;
- scope and inheritance impact;
- Judge, Audit method, and expected Evidence;
- unresolved conflicts or assumptions.

Completion criterion: every written Law has WHY and WHAT, with Scope and Audit defined when needed for evaluation; parent/child conflicts are resolved by human decision; and no implementation file was modified.
