# Spec Document Convention

A target project's spec documents live under `spec/**/*.md`, not a single `SPEC.md`/`docs/spec.md`/`requirements.md` file.

- One directory per EPIC: `spec/{epic-slug}/`, one file per STORY inside it: `spec/{epic-slug}/{story-slug}.md`.
- `spec/{epic-slug}/index.md` follows `../template/spec-epic-index.md` — the EPIC's 3-sentence intro plus a list linking to its STORY files.
- Each STORY file follows `../template/spec.md`'s format — the spec lines, ending in an AC (acceptance criteria) block.
- `spec/index.md` follows `../template/spec-index.md` — one heading per top-level area, linking to each `spec/{epic-slug}/index.md`.
- `spec/overview.md` is the project's what/why in one short page — a paragraph, not a spec — linking into `spec/index.md` for detail rather than restating any requirement or AC.
- If `spec/` doesn't exist yet in the target project, create it and note that in the plan/report.
- Adding or updating a STORY file always updates its `spec/{epic-slug}/index.md` and the top-level `spec/index.md` in the same change — an unlisted file is treated as not done.
