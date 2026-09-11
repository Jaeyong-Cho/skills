# Scratch constraint-gathering input

This scratch input is assembled from the repository's `to-constraint`, `get-context`, and requirements-engineering guidance. It deliberately contains durable constraints from only some categories so omitted categories can be checked.

## Case A: partial project request

The change is documentation-only in `references/demo.md`; preserve the existing Markdown structure, formatting, and naming conventions, and use the exact command `python3 -m unittest`. Do not add libraries or dependencies. Work on branch `experiment/checklist`, and do not publish or release anything. The repository maintainer gives final approval. Keep generated output in `experiments/01-constraint-checklist.raw/`. Credentials must stay out of files. Read configuration from environment variables, keep sample data local, support Python 3.11, finish within 2 seconds, and record stdout in the experiment report. Include the verification command and a license note in the documentation.

## Case B: sparse prose-only request

Please capture the explicit requirements and boundaries in `contexts/01-constraints-demo.md`. Keep the exact path and command `python3 -m unittest`, and preserve the current file naming convention. No production files may be changed.

## Case C: broad but incomplete request

The implementation must preserve the public API contract and existing document structure, follow the repository's formatting and naming conventions, use the current dependencies, run the existing test suite, and remain compatible with Python 3.11. Work in the named feature branch, keep deployment configuration unchanged, and document the result. The owner approves the change. Do not alter licensing, and record test output for review. There is no release or rollback plan in this request.
