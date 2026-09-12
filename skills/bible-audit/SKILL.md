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
3. If `.bible/tools/<category>/<subcategory>/<LAW-ID>.audit.sh` exists, run that executable first from the target repository root with the target path as its first argument. Otherwise use the Law's declared Audit method and the lowest-cost sufficient check. Inspect relevant files, callers, tests, dependency graphs, or command output as needed.
4. Interpret audit-script exit `0` as `Compliant`, `1` as `Violated`, and `2` or an execution failure as `Cannot determine`; do not override an audit-script result without concrete evidence. For exit `2`, preserve and surface the complete `AI VERIFICATION METHOD` block, then follow its method before deciding compliance. Record observed results, exact paths/line references, commands, exit codes, and relevant output. Missing or nondeterministic evidence is `Cannot determine`, not `Compliant`.
5. Compare applicable Laws for incompatible requirements on the same target, including inherited-versus-child conflicts. Report each as a separate `Law conflict`; do not choose a winner or reinterpret either Law.
6. If a Law's WHAT is command-verifiable but its matching audit script is missing, report a verification gap and use the declared Audit method only as provisional evidence. If WHAT and WHY appear inconsistent, report a separate `Law concern`; do not reinterpret the Law or propose an amendment here.

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

## Verification gaps
- [LAW-... — command-verifiable WHAT without a matching audit script, or `None`]

## AI verification methods
- [LAW-... — complete `AI VERIFICATION METHOD` alert and follow-up result, or `None`]

## Law conflicts
- [conflicting Law IDs, incompatible requirements, scope, and evidence, or `None`]

## Law concerns
- [WHAT/WHY inconsistency, or `None`]

## Verdict
[Compliant | Violations found | Cannot determine | Law conflict]
```

Do not hide clean results, skip applicable Laws, or call an unverified state compliant. An audit finding is evidence for Reform; a Law concern is evidence to return to Enact.

Completion criterion: every applicable inherited and local Law has a result, every available matching audit script was run and its exit/output recorded, every applicable Law conflict was checked and reported, every command-verifiable Law missing its audit script has a verification gap, every violation has concrete evidence tied to WHAT, separate Law concerns are recorded, and no file was modified.
