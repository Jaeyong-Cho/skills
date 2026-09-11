# Raw experiment artifacts

- `source/to-constraint-SKILL.md` and `source/get-context-SKILL.md` are repository snapshots used to derive the category candidates and prose baseline.
- `source/requirement-engineering.md`, `source/document-style-writing-rules.md`, and `source/clean-code-meaningful-names.md` provide repository wording for durable verification, style, formatting, and naming constraints.
- `input.md` is the scratch input. Cases intentionally address only subsets of the candidates.
- `gold.json` is the manual annotation of categories explicitly addressed by each case, including explicit negative or unchanged statements.
- `analyze.py` applies the same cue extraction to both methods, then compares present-only prose reporting with an all-category checklist.
- `regenerate.sh` reproduces the Act step and writes `output.json`.
- `output.json` is the captured run output.
