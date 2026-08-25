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

At least 3 entries. Each needs:
- `id` — short identifier, used nowhere but this file.
- `file` — path to a standalone `.svg` file, relative to `manifest.json`'s directory (normally `assets/{id}-{slug}.svg`).
- `caption` — one sentence, rendered under the figure.
- `section` — which top-level section key (`introduction`, `background`, `methodology`, `results`, or `conclusion`) the figure is placed inside, right after that section's text. Omit or name an unknown section to have it placed in an appendix at the end instead.

## Numbering

Fixed by section order, not stored in the manifest — `build_paper.py` derives it: Introduction = 1, Background = 2, Methodology = 3, Results = 4, Conclusion = 5. A section given as an object gets its subsections numbered `N-1`, `N-2`... in the object's key order. Title and Abstract are never numbered.
