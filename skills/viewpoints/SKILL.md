---
name: viewpoints
description: Build a set of complementary viewpoints on a subject instead of picking one chart — profile the data or structure, shortlist diverse forms (charts and diagrams) from a catalog, render each in a consistent theme, and annotate each with how to read it and what it reveals. Use when the user wants to explore or discover insights in a dataset, visualize a system, algorithm, or schema, asks how to visualize something without naming a form, or wants multiple/comparative views of the same subject.
---

A single visualization answers one question well; a gallery of **viewpoints** — several complementary forms shown side by side — answers several. The forms aren't only statistical charts: viewpoints can mix data charts (bar, scatter, heatmap) with structural diagrams (flowchart, architecture, entity-relationship, state, directory tree) when the subject has a structural face as well as, or instead of, a tabular one. Build a gallery of viewpoints instead of guessing the single "best" view.

MUST NOT use unicode arrows (`→`, `⇒`), box-drawing characters (`─`, `│`, `┌`), bullets (`•`, `▪`), or emoji. USE ASCII instead.

## Steps

1. **Profile the subject.** First identify what you're visualizing — tabular data, a structure (system, codebase, algorithm, schema, filesystem), or both. For tabular data: per column note data type, cardinality, and missingness; for the whole, note inter-column relationships, hierarchical structure, and temporal structure. For a structure: note its elements and the relations among them — sequence/control flow, dependency, containment/hierarchy, state transitions, and cardinality. Done when every face the subject has (data, structural, or both) is profiled, stating "none" where a dimension doesn't apply — a partial profile understates what the gallery could show.

2. **Shortlist from the gallery.** Match the profile against `references/catalog.md`. The same form may appear more than once when it targets a genuinely different data slice or answers a different question — a bar chart of sales-by-region and a bar chart of units-by-category are two distinct entries, not a duplicate. What's redundant is the same form over the *same* data and purpose — two bar-chart variants of one slice is one entry, not two. There is no cap on the number of charts — include every form that adds genuine analytical value for some data slice or question, however many that is. Done when every structure present in the profile (a time column, a hierarchy, a numeric relationship, etc.) is covered by at least one shortlisted form, and the only entries excluded are those that are the same form over the same data slice and purpose (redundant) or that add no analytical value. Usefulness per chart, not a target count, is the bar.

3. **Render every shortlisted form as SVG**, using whatever plotting tool the project already uses for data charts, and mermaid (`mmdc`) or graphviz for structural diagrams, styled from `references/palette.md` (the token-light theme): assign categorical slots in the documented order, use the sequential or diverging ramp where the form calls for one, and pull surface/text/gridline/border colors from the chrome table rather than picking colors ad hoc. Prefer SVG output for crisp scaling; fall back to PNG only when the tool can't emit SVG. Light mode only for now — dark-mode data marks aren't derived yet, so fall back to any sensible default dark categorical set. Done when every shortlisted form has been rendered — none dropped silently for seeming redundant or hard to implement.

4. **Annotate each rendered form** with reader-facing notes using the template below — information that helps someone read the view, not why it was chosen — drawing every claim from what the render actually shows, not boilerplate copied from the catalog entry. Done when all four sections are filled for every rendered form.

5. **Rank the gallery (optional)** — most relevant to the user's stated question first.

6. **Assemble the gallery page into an output directory.** Pick an output directory — use the one the user named, else default to `gallery/{dataset-slug}/`. Create it, write the manifest and any rendered images there, build a manifest JSON (schema in `scripts/build_gallery.py`'s docstring) with one entry per rendered form — its catalog category, title, image, and the four explanation fields — then run `python scripts/build_gallery.py {output-dir}/manifest.json {output-dir}/index.html`. Done when `{output-dir}/index.html` exists, embeds every rendered image directly (no external file references), and opens standalone in a browser.

7. **Serve the gallery.** Copy `scripts/serve.sh` to the gallery directory to make run manually. (binds `0.0.0.0:4800`; pass a second arg to override the port), then report the URL to open: http://localhost:4800. MUST NOT RUN server. user will manually run it.

## Output template (per visualization)

- **What it shows** — the content of this view: which variables or elements it depicts, and the slice, scenario, or scope drawn.
- **How to read it** — how to decode the marks, axes, or layout, and where to look first.
- **Key takeaways** — the specific patterns, values, or relationships visible in this render.
- **Watch for** — how this view can mislead: what to read cautiously or discount.

See `references/catalog.md` for the full set of forms, grouped by the structure they surface: comparison, distribution, relationship, composition, trend & time, hierarchy, network, geospatial, multivariate, and structure & flow (flowchart, sequence, architecture, entity-relationship, state, directory tree). `references/template.html` and `scripts/build_gallery.py` turn a finished gallery into a single themed `index.html`.
