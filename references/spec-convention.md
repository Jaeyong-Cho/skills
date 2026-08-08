# Spec Document Convention

A target project's spec documents live under `spec/**/*.md`, not a single `SPEC.md`/`docs/spec.md`/`requirements.md` file.

- One file per topic/feature: `spec/{topic-slug}.md`, or nested `spec/{area}/{topic-slug}.md` for large projects.
- Each file follows `../template/spec.md`'s format — Introduction, sub-topics, each with an AC (acceptance criteria) block.
- `spec/index.md` is the table of contents: one heading per top-level area, every spec file listed underneath as a link to its path.
- If `spec/` doesn't exist yet in the target project, create it and note that in the plan/report.
- Adding or updating a spec file always updates `spec/index.md` in the same change — an unlisted spec file is treated as not done.
