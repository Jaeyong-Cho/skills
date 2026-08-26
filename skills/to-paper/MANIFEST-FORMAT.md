# manifest.json format

Everything `scripts/build_paper.py` renders into `index.html`, and everything `scripts/lint_paper.py` checks, lives in one `manifest.json`. Seven fixed section keys, in this order, plus `diagrams`, plus an optional trailing `appendix`:

```json
{
  "title": "A short, plain-language title",
  "abstract": ["One paragraph, one array element."],
  "introduction": ["First paragraph.", "Second paragraph.", "Third paragraph."],
  "background": {
    "bg1": ["Plain text, no subtitle rendered."],
    "bg2": { "title": "Prior Work", "text": ["First paragraph.", "Second paragraph."] }
  },
  "methodology": {
    "data-collection": { "title": "Data Collection", "text": ["..."] },
    "analysis": { "title": "Analysis", "text": ["..."] }
  },
  "results": ["First paragraph.", "Second paragraph.", "Third paragraph."],
  "discussion": ["First paragraph.", "Second paragraph.", "Third paragraph."],
  "conclusion": ["First paragraph.", "Second paragraph.", "Third paragraph."],
  "diagrams": [
    { "id": "fig1", "diagram_type": "Flowchart", "file": "assets/fig1-pipeline.diagram.html", "caption": "The pipeline end to end.", "section": "methodology" },
    { "id": "fig2", "diagram_type": "Bar chart", "file": "assets/fig2-results.diagram.html", "caption": "Results by cohort.", "section": "results" },
    { "id": "fig3", "diagram_type": "Architecture", "file": "assets/fig3-architecture.diagram.html", "caption": "System architecture.", "section": "background" },
    { "id": "tbl1", "type": "table", "rows": [["Metric", "Before", "After"], ["Latency", "85ms", "20ms"]], "caption": "Latency before and after.", "section": "results" }
  ],
  "appendix": {
    "raw-metrics": { "title": "Raw Metrics", "text": ["run_id,latency_ms,cpu_pct", "1,85,42", "2,20,38"] }
  }
}
```

## Section values

Every section's prose is a **JSON array of paragraph strings** — one element per paragraph, never a single string with blank lines inside it. Each array element becomes one `<p>` — except an element that's itself a **JSON array of item strings**, which renders as one `<ul>` bullet list instead (e.g. `["Intro paragraph.", ["First point.", "Second point."], "Closing paragraph."]`). A bullet-list element counts as one paragraph toward the range below; it needs 2-8 items, each at most 20 words (`lint_paper.py`'s `MIN_LIST_ITEMS`/`MAX_LIST_ITEMS`), and skips the per-paragraph sentence-count check. Not valid inside `abstract`, which must stay a single plain paragraph string.

Paragraph count is checked per section (a subsection inherits its parent section's range), not one flat rule: introduction 3-5, background 4-8, methodology 2-4, results 2-4, discussion 3-6, conclusion 1-3 (`lint_paper.py`'s `SECTION_PARAGRAPH_RANGES`).

- **`introduction`, `results`, `discussion`, `conclusion`** — an array of paragraph strings.
- **`background`, `methodology`** — either an array of paragraph strings (same as above, no subsections), or an object of subsections. Each subsection value is either an array of paragraph strings (no subtitle, just folded into the section) or `{"title": ..., "text": [...]}` (gets its own numbered sub-heading, `text` an array of paragraph strings). Subtitles are optional — use them only where the section genuinely splits into distinct parts.
- **`abstract`** — an array of paragraph strings, constrained to exactly one element (one paragraph).
- **`title`** — a plain string, no paragraph/sentence structure (never an array).

## `appendix` (optional)

Same shape as `background`/`methodology` above — an array of paragraph strings, or an object of subsections (each `{"title": ..., "text": [...]}` or a bare array) — but exempt from every prose-quality rule above: no paragraph-count range, no per-paragraph sentence-count, no per-sentence/per-bullet-item word limit. It's for raw experiment output, detailed statistics, data dumps — content that's naturally a wall of numbers, not academic prose, and would otherwise get forced into an unnatural sentence cadence just to pass the lint. `lint_paper.py` only checks it's structurally well-formed (paragraphs are strings or bullet lists of strings) and that any `{{fig:...}}`/`{{tbl:...}}` refs inside it are real. Prefer a table (`diagrams[]`, `"type": "table"`) for anything that's naturally rows and columns — reach for `appendix` only for content a table doesn't fit either (a raw log excerpt, a CSV dump, a long parameter list). Renders as an unnumbered "Appendix" heading (and unnumbered subsection titles) after Conclusion; a diagram can target it too (`"section": "appendix"` or `"appendix.{sub-key}"`, same rules as any section).

## `diagrams`

At least 5 non-table entries — a floor, not a target; a table is not a figure, so table entries don't count toward it (see "Two kinds" below). More figures are good: add one anywhere a reader would learn more from a picture (or a table) than a paragraph (per `DIAGRAM-SELECTION.md`'s gate), don't stop once the floor is met. Every entry needs:
- `id` — short identifier, used nowhere but this file.
- `caption` — one sentence, at most 140 characters, rendered under the figure. A caption never shrinks the figure to fit — it wraps within the figure's own width instead (`assets/template.html`'s figure/figcaption CSS) — but a caption this long is really a paragraph in disguise; shorten it.
- `section` — where the figure is placed, right after that target's own text:
  - a top-level section key (`introduction`, `background`, `methodology`, `results`, `discussion`, `conclusion`) — placed at the end of that section, after every one of its subsections.
  - `"{section}.{subsection-key}"` (e.g. `"methodology.data-collection"`) — sub-title granularity: placed right after that one subsection's text, not the whole section. Only valid when that section is given as an object and the key names one of its subsections.
  - `"{target}@{N}"` (e.g. `"introduction@2"` or `"methodology.data-collection@1"`, 1-based) — paragraph granularity: placed right after that target's Nth paragraph specifically (a bullet-list element counts as one paragraph here too), not at the end of the whole section/subsection. `N` must be a real paragraph index for that target.
  - Omit, or name a section/subsection/paragraph that doesn't exist, to have it placed in an appendix at the end of the paper instead.

Two kinds, chosen by an optional `type` field:
- **Diagram (default, no `type` field)** — `diagram_type`, the exact "Use" name from `DIAGRAM-SELECTION.md`'s Visual-type guide (e.g. `"Flowchart"`, `"Bar chart"`, `"Architecture"`) — required, and what the diversity rule below counts. `file`, a path relative to `manifest.json`'s directory — **the `.diagram.html` draft itself** (normally `assets/{id}-{slug}.diagram.html`), not an exported `.svg`. `build_paper.py` extracts the `<svg>...</svg>` block straight out of whatever `file` points to and inlines it directly into `index.html` at build time — no `<img>`, no separate export step, no staleness risk from an unexported edit. (A standalone `.svg` still works too, e.g. if one already exists — the extraction is identical either way.) Its `<svg>` needs **both** a `viewBox` (without one, scaling it down to the page's `max-width` can crop it instead of shrinking it cleanly) **and** explicit `width`/`height` attributes matching it (they establish the correct aspect ratio unambiguously).
- **Table (`"type": "table"`)** — `rows`, an array of arrays: the first row is the header, every row (including the header) must have the same number of columns. No `file`, no `diagram_type` (it counts as its own kind, `"table"`, toward the diversity rule below). Rendered as a real `<table>`, not an image — reach for this whenever the content is naturally rows and columns (a before/after comparison, a results breakdown) rather than forcing it into a chart. A table is not a figure: it gets its own "Table N" numbering (see Numbering below), separate from and not counted toward the 5-figure floor above.

**At least 3 different kinds** across all `diagrams[]` entries — the distinct `diagram_type` values used, plus `"table"` if any table entries exist. Five flowcharts is one kind; `lint_paper.py` rejects it. Pick each figure's type independently from `DIAGRAM-SELECTION.md` (step 3 of `SKILL.md`) instead of reusing whatever type the last figure happened to use.

## Numbering

Sections are fixed by order, not stored in the manifest — `build_paper.py` derives it: Introduction = 1, Background = 2, Methodology = 3, Results = 4, Discussion = 5, Conclusion = 6. A section given as an object gets its subsections numbered `N-1`, `N-2`... in the object's key order. Title, Abstract, and the optional `appendix` (and its subsections) are never numbered.

**Figures are numbered too** — Fig 1, Fig 2..., in the order they're placed in the built paper (reading order, not the `diagrams` array's order), never written by hand. To cite one from prose, write `{{fig:some-id}}` anywhere in a section/subsection/abstract's text (e.g. `"...as shown in {{fig:fig1}}, throughput..."`) — `build_paper.py` replaces it with a link reading "Fig N" to that exact figure. `some-id` must be a real non-table `diagrams[].id`; `lint_paper.py` checks this.

**Tables have their own numbering** — Table 1, Table 2..., a separate sequence from Fig N (also reading order): a table is not a figure. Cite one with `{{tbl:some-id}}` instead of `{{fig:some-id}}` (e.g. `"...as shown in {{tbl:tbl1}}, latency..."`) — it resolves to a "Table N" link. `some-id` must be a real table (`"type": "table"`) `diagrams[].id`; `{{fig:...}}` pointing at a table id, or `{{tbl:...}}` pointing at a non-table id, is a lint error.
