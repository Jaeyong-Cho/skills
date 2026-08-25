# manifest.json format

Everything `scripts/build_paper.py` renders into `index.html`, and everything `scripts/lint_paper.py` checks, lives in one `manifest.json`. Six fixed section keys, in this order, plus `diagrams`:

```json
{
  "title": "A short, plain-language title",
  "abstract": "One paragraph. No blank line inside it.",
  "introduction": "First paragraph.\n\nSecond paragraph.\n\nThird paragraph.",
  "background": {
    "bg1": "Plain text, no subtitle rendered.",
    "bg2": { "title": "Prior Work", "text": "First paragraph.\n\nSecond paragraph." }
  },
  "methodology": {
    "data-collection": { "title": "Data Collection", "text": "..." },
    "analysis": { "title": "Analysis", "text": "..." }
  },
  "results": "First paragraph.\n\nSecond paragraph.\n\nThird paragraph.",
  "conclusion": "First paragraph.\n\nSecond paragraph.\n\nThird paragraph.",
  "diagrams": [
    { "id": "fig1", "file": "assets/fig1-pipeline.svg", "caption": "The pipeline end to end.", "section": "methodology" },
    { "id": "fig2", "file": "assets/fig2-results.svg", "caption": "Results by cohort.", "section": "results" },
    { "id": "fig3", "file": "assets/fig3-architecture.svg", "caption": "System architecture.", "section": "background" }
  ]
}
```

## Section values

- **`introduction`, `results`, `conclusion`** — a plain string. Paragraphs are separated by a blank line (`\n\n`); everything else is one paragraph run through as-is.
- **`background`, `methodology`** — either a plain string (same paragraph rule as above, no subsections), or an object of subsections. Each subsection value is either a plain string (no subtitle, just folded into the section) or `{"title": ..., "text": ...}` (gets its own numbered sub-heading). Subtitles are optional — use them only where the section genuinely splits into distinct parts.
- **`abstract`** — a plain string, exactly one paragraph (no `\n\n`).
- **`title`** — a plain string, no paragraph/sentence structure.

## `diagrams`

At least 5 entries — a floor, not a target. More figures are good: add one anywhere a reader would learn more from a picture than a paragraph (per `DIAGRAM-SELECTION.md`'s gate), don't stop once the floor is met. Each needs:
- `id` — short identifier, used nowhere but this file.
- `file` — path to a standalone `.svg` file, relative to `manifest.json`'s directory (normally `assets/{id}-{slug}.svg`).
- `caption` — one sentence, at most 140 characters, rendered under the figure. A caption never shrinks the figure to fit — it wraps within the figure's own width instead (`assets/template.html`'s figure/figcaption CSS) — but a caption this long is really a paragraph in disguise; shorten it.
- `section` — where the figure is placed, right after that target's own text:
  - a top-level section key (`introduction`, `background`, `methodology`, `results`, `conclusion`) — placed at the end of that section, after every one of its subsections.
  - `"{section}.{subsection-key}"` (e.g. `"methodology.data-collection"`) — sub-title granularity: placed right after that one subsection's text, not the whole section. Only valid when that section is given as an object and the key names one of its subsections.
  - Omit, or name a section/subsection that doesn't exist, to have it placed in an appendix at the end of the paper instead.

Every `.svg` file needs a `viewBox` attribute (not just `width`/`height`) — without one, scaling it down to the page's `max-width` can crop it instead of shrinking it cleanly.

## Numbering

Sections are fixed by order, not stored in the manifest — `build_paper.py` derives it: Introduction = 1, Background = 2, Methodology = 3, Results = 4, Conclusion = 5. A section given as an object gets its subsections numbered `N-1`, `N-2`... in the object's key order. Title and Abstract are never numbered.

**Figures are numbered too** — Fig 1, Fig 2..., in the order they're placed in the built paper (reading order, not the `diagrams` array's order), never written by hand. To cite one from prose, write `{{fig:some-id}}` anywhere in a section/subsection/abstract's text (e.g. `"...as shown in {{fig:fig1}}, throughput..."`) — `build_paper.py` replaces it with a link reading "Fig N" to that exact figure. `some-id` must be a real `diagrams[].id`; `lint_paper.py` checks this.
