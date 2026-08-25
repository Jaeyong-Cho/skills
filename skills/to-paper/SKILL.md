---
name: to-paper
description: Write a short HTML research paper — Title, Abstract, Introduction, Background, Methodology, Results, Conclusion, with numbered sections/subsections, at least 3 diagram-design-themed SVG figures, and a writing-quality linter — then build it into index.html. Invoke as /to-paper.
disable-model-invocation: true
---

# To-Paper

A research paper as one manifest.json plus a build script, the same split `@skills/diagram-design` uses between content and rendering. Everything the paper says lives in `manifest.json`; `index.html` is always regenerated from it, never hand-edited.

1. **Confirm the output directory.** Ask the user where `{slug}-research-paper/` should be written — recommend `./{slug}-research-paper/` at the current project root as the default (this repo's usual "skill-named directory at project root" convention), but let them name any path. Once confirmed, `mkdir -p {dir}/assets`. Completion criterion: a confirmed absolute path, directory created.
2. **Draft the manifest.** Read `MANIFEST-FORMAT.md` first for the exact JSON schema (six fixed section keys, paragraph/subsection shape, `diagrams` array). Write `{dir}/manifest.json`. Subtitles on `background`/`methodology` subsections are optional — only split a section that genuinely has distinct parts.
3. **Pick each diagram's type.** Read `DIAGRAM-SELECTION.md` first — its "When to use a diagram at all" gate (if a table, a bulleted list, or a well-written sentence would teach the reader as much, don't draw it), its Visual-type guide table (architecture, flowchart, sequence, timeline, quadrant, tree, layer stack, bar/line/scatter chart, ...), and its Rules of thumb — the dominant axis of what the figure shows decides the type, not habit.
4. **Draw at least 3 diagrams.** Read `../diagram-design/references/style-guide.md` (tokens: `paper`/`ink`/`muted`/`accent`/`link`, Instrument Serif / Geist / Geist Mono) and the `../diagram-design/references/type-*.md` matching each figure's type from step 3, and follow its §1 Philosophy and §4 anti-patterns. **Do not invoke `@skills/diagram-design` directly** — it renders a full standalone HTML document; this skill only needs the bare `<svg>...</svg>` markup, saved as its own file under `{dir}/assets/{id}-{slug}.svg`, using the same tokens as `assets/template.html` so figures and page match. Every SVG carries the accessible-SVG contract step 5's `scripts/lint_paper.py` checks — `role="img"`, a `<title>` as its first child, a non-empty `<title>`/`<desc>` pair with diagram-prefixed ids, `aria-labelledby` naming them in that order. Add each to the manifest's `diagrams` array (`id`, `file`, `caption`, `section`).
5. **Lint the manifest.** Run `python3 scripts/lint_paper.py {dir}/manifest.json` (relative to this skill's directory). Fix every reported violation — title word count, abstract-is-one-paragraph, 3-5 paragraphs per other section/subsection, 3-8 sentences per paragraph, at most 20 words per sentence, at least 3 diagrams with existing accessible SVG files (the same contract `diagram-design/scripts/self_check.py` enforces, applied to a bare `.svg` instead of a full HTML page) — and re-run until clean. A red lint is not a done draft.
6. **Build `index.html`.** Run `python3 scripts/build_paper.py {dir}/manifest.json`. It renders `{dir}/index.html` from `assets/template.html`, deriving section numbers (Introduction=1 … Conclusion=5, subsections `N-1`, `N-2`...) itself — never hand-number a heading in the manifest.
7. **Re-run after any later edit.** A follow-up change to content or figures means editing `manifest.json` (or replacing an SVG under `assets/`), then repeating steps 5-6 — never hand-editing `index.html`.

Completion criterion: `manifest.json`, `index.html`, and at least 3 `assets/*.svg` files exist; step 5's lint is clean; `index.html`'s headings show the numbering step 6 derived.

Tell the user the output directory path and that it's clean of lint errors when done.
