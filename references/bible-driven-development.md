# Bible-Driven Development

The Bible is the durable source of engineering intent. It records what MUST remain true and why. Implementation may change freely while it remains compliant.

> **Manage invariants, not implementations.**

## Lifecycle

```text
Human intent
-> Enact: define WHY and WHAT
-> Bible
-> Audit: compare WHAT with reality
-> Evidence / violations
-> Reform: correct implementation and reinforce checks
-> Audit
```

The three authorities are deliberately separate:

| Operation | Bible | Implementation | Violations |
|---|---|---|---|
| Enact | write | read | read |
| Audit | read | read | write |
| Reform | read | write | read |

Reform never fixes a violation by weakening a Law. If the WHAT no longer serves its WHY, stop and return the evidence to Enact.

## Bible locations and inheritance

A Bible root is a `.bible/` directory. The effective Bible for a target is the ordered chain of applicable roots:

```text
~/.bible/                         global engineering Laws
-> <repository>/.bible/           repository Laws
-> <component>/.bible/            optional narrower sub-Bible
-> target
```

- `~/.bible/` describes how the owner builds software.
- `<repository>/.bible/` describes what that repository MUST be.
- A nested `<component>/.bible/` is a sub-Bible for that component. It inherits Laws from its nearest parent and may add narrower Laws.
- A child Bible MUST NOT weaken or contradict an inherited Law. Laws at any applicable level MUST NOT make incompatible requirements for the same target. Change or reconcile conflicting Laws through Enact instead.
- The global and repository roots are the default scopes. Add component sub-Bibles only when a clear boundary needs its own Laws.

Agents MUST read the parent-to-child chain before auditing or reforming a target. A child Law is additional scope, not an override.

## Canonical directory structure

```text
.bible/
+-- index.md
+-- laws/
|   +-- index.md
|   +-- <category>/
|       +-- index.md
|       +-- <subcategory>/
|           +-- index.md
|           +-- <law>.md
+-- tools/
    +-- index.md
    +-- <category>/
        +-- index.md
        +-- <subcategory>/
            +-- index.md
            +-- <tool>
```

The taxonomy has exactly two levels:

```text
laws/<category>/<subcategory>/<law>.md
tools/<category>/<subcategory>/<tool>
```

Do not add another taxonomy directory. Use Law metadata, tags, names, or prose for further classification.

### Directory rules

- Every directory inside `.bible/` MUST contain `index.md`.
- `laws/` contains only Law categories and Law documents.
- `tools/` contains only inspection-tool categories and executable tools.
- `index.md` is the only file allowed at the root, category, and subcategory navigation levels.
- Law files live only at `laws/<category>/<subcategory>/` and end in `.md`.
- Tool files live only at `tools/<category>/<subcategory>/`; each tool MUST have a deterministic exit status and evidence output.
- Empty categories are allowed while a taxonomy is being established, but an index should explain their purpose.

## Index files

An index is a navigation and semantic entry point, not just a README. Every index SHOULD answer:

1. **Purpose** — why the directory exists;
2. **Contents** — what its artifacts mean;
3. **Navigation** — where an agent should go next.

Agents should read the nearest index before traversing deeper. This provides progressive discovery instead of loading the whole Bible.

## Laws

A Law is a Markdown document under `laws/`. The category describes the concern, for example `architecture/dependency`, `behavior/cli`, or `development/testing`.

Every Law MUST contain both sections:

```markdown
# LAW-ARCH-014 — Sender Public Interface

## WHY

Callers should depend only on the essential sending capability.

## WHAT

Sender SHALL expose exactly one public method: `send`.

## Scope

The Sender type and its callers.

## Audit

Run the public-interface inspection tool and record its output.
```

- **WHY** records the protected intent, risk, requirement, or lesson.
- **WHAT** is the enforceable condition. Audit judges WHAT, not a private reinterpretation of WHY.
- **Scope** states where the Law applies.
- **Audit** names the inspection method and expected evidence when practical.

A Law without WHY cannot be safely amended or reformed. A Law without WHAT cannot be judged. Laws SHOULD constrain boundaries and observable invariants rather than prescribe an implementation sequence.

Every enacted Law MUST have a stable unique `LAW-...` identifier. The identifier connects the Law to its audit script and remains unique within the effective Bible chain.

## Tools

Tools under `tools/` inspect reality; they are not Laws. A tool may serve many Laws. Prefer the cheapest reliable Judge:

```text
static check
-> focused test
-> integration test
-> end-to-end test
-> agent review
-> human review
```

A deterministic tool has this contract:

- exit code `0`: the checked condition holds;
- exit code `1`: the checked condition is violated;
- exit code `2`: the tool cannot determine the result;
- stdout/stderr: enough command, input, observed result, and expected result to reproduce the Evidence.

When a Law's WHAT can be checked by a command, Enact SHOULD create a dedicated executable audit script at `.bible/tools/<category>/<subcategory>/<LAW-ID>.audit.sh`. The script is the Law's `audit.sh`: run it from the target repository root with the target path as `$1`; use exit `0` for compliant, `1` for violated, and `2` when it cannot determine the result. Print the command, expected condition, observed result, and useful paths or output. If the check is nondeterministic or needs agent/human judgment, it MUST NOT guess or return `0`; return `2` and print this machine-visible alert with the concrete follow-up method:

```text
AI VERIFICATION METHOD:
Method: <inspection, comparison, probe, or human decision to perform>
Inputs: <paths, command output, or other evidence needed>
Expected: <condition to judge>
Observed: <what the script could establish>
Next action: <what the AI or human must do>
```

A Law that genuinely needs human judgment may omit the script, but its Audit section MUST say why.

A Law should name its audit script or other Audit method in its Audit section. Bible Audit runs the matching `<LAW-ID>.audit.sh` first when it exists and records its exit code and output. For exit `2`, it MUST surface the complete `AI VERIFICATION METHOD` alert and follow it before deciding compliance. Missing evidence is `Cannot determine`, not `Compliant`.

## Enact, Audit, Reform

### Enact

Enact starts with `@skills/grill-me` unless intent and scope are already confirmed. It establishes WHY before WHAT, defines scope and a Judge, then asks for approval before writing. Enact may create, amend, repeal, reorganize, or add tools. It MUST NOT modify implementation merely to make a Law pass.

### Audit

Audit resolves the effective parent chain, selects applicable Laws, checks for contradictory requirements, reads WHY and WHAT, runs each Law's Judge, and records commands, paths, exit codes, and observed output. It is read-only. If Laws conflict, report a Law conflict and stop the workflow for Enact; if WHAT and WHY appear inconsistent, report a Law concern instead of ignoring WHAT or editing the Bible.

### Reform

Reform consumes current Audit violations, reads WHY and WHAT, finds the cause, makes the smallest safe implementation change, and reinforces the Judge where useful. It may modify source, tests, configuration, build logic, or deterministic tooling, but never a Bible. It audits the changed state again before declaring the violation resolved.

## Linter

Use the repository linter before committing a Bible structure change:

```text
python skills/bible-audit/scripts/lint_bible.py .bible
```

For a repository Bible governed by a global Bible, include the parent explicitly:

```text
python skills/bible-audit/scripts/lint_bible.py .bible --parent ~/.bible
```

The linter checks directory shape, required indexes, taxonomy depth, Law Markdown files, required WHY/WHAT sections, duplicate Law identifiers, executable tools, and broken relative links in indexes. It does not decide whether a WHAT is a good Law or whether implementation complies; Audit owns those judgments.

Exit status:

```text
0  structure is valid
1  one or more violations were found
2  invalid command or unreadable input
```

## Working rule

```text
WHY
-> WHAT
-> Judge
-> Evidence
-> Reform
```

Use Enact to change the rules, Audit to establish the facts, and Reform to change the software.
