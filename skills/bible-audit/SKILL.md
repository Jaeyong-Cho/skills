---
name: bible-audit
description: Audit a repository or component against its governing Bible Laws, reporting violations with concrete evidence without changing code or Laws.
disable-model-invocation: true
license: MIT
---

# Bible Audit

Find where applicable Laws are false and collect reproducible evidence. Audit is read-only: never modify a `.bible/`, implementation, tests, configuration, or generated files.

## Scope and inheritance

1. Read `../references/bible-driven-development.md` and run `scripts/lint_bible.py` against each supplied Bible root first. Report structural failures; do not treat them as semantic compliance.
2. Use the Bible path and target supplied by the human or caller. Otherwise resolve `~/.bible/`, the repository's `.bible/`, and the nearest component `.bible/`. If no repository Bible exists, stop and recommend `@skills/bible-enact`.
3. Read the relevant indexes, then the target Bible and every parent Bible up to the root. A parent `.bible/` governs descendants unless its Scope excludes them. A nested `.bible/` adds Laws for its subtree.
4. Determine applicability from each Law under `laws/<category>/<subcategory>/` and the target. Do not audit unrelated Laws, and do not treat a child Law as permission to weaken an inherited Law.

## Judge

For every applicable Law:

1. Read both WHY and WHAT. Use WHY to understand the purpose and detect a possible Law design problem.
2. Judge compliance strictly against WHAT. Do not ignore a precise WHAT because another implementation seems to satisfy its WHY.
3. Use the Law's Audit method first. Run the lowest-cost sufficient check and inspect relevant files, callers, tests, dependency graphs, or command output.
4. Record observed results, exact paths/line references, commands, exit codes, and relevant output. Missing or nondeterministic evidence is `Cannot determine`, not `Compliant`.
5. If WHAT and WHY appear inconsistent, report a separate `Law concern`; do not reinterpret the Law or propose an amendment here.

## Output

Return one result for every applicable Law, followed by violations and separate Law concerns:

```markdown
# Bible Audit

## Target
- **Path:** [Bible roots and implementation target]
- **Bible chain:** [root → ... → nearest]

## Law results
| Law | Scope | Result | Judge/evidence |
|---|---|---|---|
| LAW-... | ... | Compliant / Violated / Cannot determine | command or inspection |

## Violations
### VIOLATION-001 — [short title]
- **Law:** LAW-...
- **WHY:** [intent]
- **Expected (WHAT):** [exact requirement]
- **Actual:** [observed state]
- **Evidence:** [paths, commands, output, exit code]
- **Smallest safe reform:** [candidate, not an edit]

## Law concerns
- [WHAT/WHY inconsistency, or `None`]

## Verdict
[Compliant | Violations found | Cannot determine]
```

Do not hide clean results, skip applicable Laws, or call an unverified state compliant. An audit finding is evidence for Reform; a Law concern is evidence to return to Enact.

Completion criterion: every applicable inherited and local Law has a result, every violation has concrete evidence tied to WHAT, separate Law concerns are recorded, and no file was modified.
