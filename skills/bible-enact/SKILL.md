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
4. Define an Audit method and expected Evidence. Prefer a deterministic Judge: test, compiler, linter, AST/dependency query, CLI command, or small script. If a command can verify the WHAT, SHOULD create a dedicated executable `.bible/tools/<category>/<subcategory>/<LAW-ID>.audit.sh` for the Law. Give it the target path as `$1`, use exit `0` for compliant, `1` for violated, and `2` for `Cannot determine`, and print reproducible evidence. If the check is nondeterministic or needs agent/human judgment, the audit script MUST return `2` and print an `AI VERIFICATION METHOD` block naming the method, inputs, expected condition, observed facts, and next action; it MUST NOT guess a pass. If command verification is not possible, state why the Law needs human judgment in its Audit section.
5. Check that the Law does not duplicate, contradict, or unnecessarily broaden an existing inherited or local Law.
6. Show the proposed Law and audit script together, then obtain explicit human approval before writing either one.

Every Law document under `.bible/laws/<category>/<subcategory>/` MUST contain `## WHY` and `## WHAT`. When its WHAT is command-verifiable, its matching `<LAW-ID>.audit.sh` SHOULD be proposed under `.bible/tools/<category>/<subcategory>/`. This is the recommended complete shape:

```markdown
# LAW-<ID> — <Title>

## WHY

Why this Law exists and what risk, problem, or intent it protects.

## WHAT

What MUST remain true, stated precisely.

## Scope

Where this Law applies.

## Audit

Run `.bible/tools/<category>/<subcategory>/<LAW-ID>.audit.sh` from the target repository root with the target path as its first argument. Record its exit code and output as Evidence. Exit `2` MUST print the `AI VERIFICATION METHOD` block for the next reviewer.
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

Completion criterion: every written Law has a unique identifier, WHY, WHAT, Scope, and Audit; every command-verifiable Law has its executable `<LAW-ID>.audit.sh` proposed or written beside it when practical; parent/child conflicts are resolved by human decision; and no implementation file was modified.
