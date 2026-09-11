# Constraint Checklist Trial

## Abstract
This experiment asked whether a minimal checklist exposes missing durable constraints better than prose-only gathering. A saved three-case trial compared category coverage against manual annotations. The checklist detected all 27 annotated omissions, while prose-only reporting detected none, so the result is supported within this trial.

## 1. Introduction
Constraint gathering can preserve requirements that would otherwise disappear from conversation history. Missing categories are especially risky when prose mentions inspection without requiring an itemized coverage check. This question therefore needed a real extraction trial rather than a judgment from reading instructions.

The repository's `to-constraint` skill names many categories and requires `Not established` entries. Its instruction remains prose, so compliance can vary during practical use. The trial tested whether a minimal checklist makes omissions more visible under the same input.

The experiment was isolated to `./experiments/` and made no production changes. It used repository text as the source for categories and wording. The result is evidence about this fixture, not a general usability claim.

## 2. Background
`to-constraint` directs inspection of paths, structure, tests, interfaces, dependencies, ownership, releases, and operational concerns. It also requires classification by source, type, and status. These instructions define the candidate coverage areas used here.

`get-context` separates intents, facts, constraints, assumptions, and unresolved questions. Requirements engineering adds verification, compatibility, performance, documentation, and licensing concerns. Together, these references support a broader durable-constraint checklist.

Coding style was included as an additional candidate because repository references explicitly discuss formatting and meaningful naming. It was not added to production skills. The candidate therefore tests the requested extension without changing repository behavior.

The prose baseline records categories detected in text but does not emit a complete absent-category list. The checklist records every candidate as present or missing. Both methods use the same cue extractor, isolating the reporting difference.

## 3. Methodology
The scratch input contained three repository-derived request cases with deliberately partial category coverage. `gold.json` manually records categories each case explicitly addresses, including explicit negative or unchanged statements. Missing gold categories represent omissions the gathering method should expose.

`analyze.py` extracts category cues, computes checklist omissions, and gives prose-only an empty missing report. It calculates missing-category precision and recall against the annotations. The expectation was support if the checklist found more annotated omissions, refutation if fewer, and inconclusive otherwise.

`regenerate.sh` runs the saved script from the raw directory and writes the captured JSON output. Source snapshots document derivation from `to-constraint`, `get-context`, requirements, document-style, and clean-code references. All trial artifacts remain under the confirmed experiments directory.

## 4. Results
The real Act run used `experiments/01-constraint-checklist.raw/regenerate.sh` and produced `experiments/01-constraint-checklist.raw/output.json`. The input, annotations, and extractor are preserved in `input.md`, `gold.json`, and `analyze.py` beside that script. The command completed successfully.

Across three cases, annotations contained 27 missing category entries. The checklist achieved 1.00 precision and 1.00 recall, while prose-only missing recall was 0. Case-level checklist matches were exact for A, B, and C.

Case A exposed three omissions, Case B exposed eighteen, and Case C exposed six. The checklist also covered the added coding-style candidate without false omissions. Full category lists and counts are available in the raw JSON output.

## 5. Discussion
The observed result supports the expectation because the checklist surfaced every annotated omission. Prose-only extraction retained present categories but provided no comparable omission signal. The difference came from requiring an explicit status for every candidate.

Adding coding style fit the repository evidence and did not alter production files. The extractor recognized formatting and naming language in Cases A and C. Case B correctly treated coding style as unestablished.

This trial uses three synthetic cases and manually authored annotations. Its cue patterns are simple and may not represent natural language variation. The result therefore supports a bounded trial claim, not superiority across users or repositories.

The baseline models a present-only prose workflow, although the existing skill asks authors to record unestablished categories. A human who follows that instruction perfectly could match the checklist. The evidence instead shows that explicit checklist structure is more reliably machine-checkable here.

## 6. Conclusion
The checklist detected 27 of 27 annotated omissions, versus zero detected by the present-only prose baseline. The experiment therefore supports the claim for this isolated fixture, with general reliability remaining untested. A larger natural-language trial is the next check.
