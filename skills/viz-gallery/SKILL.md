---
name: viz-gallery
description: Build a gallery of complementary visualizations for a dataset instead of picking one chart — profile the data, shortlist diverse forms from a catalog, render each in a consistent theme, and explain why it was chosen, what it shows, and when to prefer it over the others. Use when the user wants to explore or discover insights in a dataset, asks how to visualize data without naming a chart type, or wants multiple/comparative views of the same data.
---

A single chart answers one question well; a **gallery** — several complementary forms shown side by side — answers several. Build one instead of guessing the "best" chart.

## Steps

1. **Profile the dataset.** For each column, note data type, cardinality, and missingness. For the dataset as a whole, note relationships between columns, hierarchical structure, and temporal structure. Done when all six dimensions are stated, including "none" where one doesn't apply — a partial profile understates what the gallery could show.

2. **Shortlist from the gallery.** Match the profile against `references/catalog.md`. Done when every structure present in the profile (a time column, a hierarchy, a numeric relationship, etc.) is covered by at least one shortlisted form, and no two shortlisted forms are near-duplicates of the same form — two bar-chart variants is one form, not two. Diversity of vantage point, not chart count, is the goal.

3. **Render every shortlisted form**, using whatever plotting tool the project already uses, styled from `references/palette.md` (the token-light theme): assign categorical slots in the documented order, use the sequential or diverging ramp where the form calls for one, and pull surface/text/gridline/border colors from the chrome table rather than picking colors ad hoc. Light mode only for now — dark-mode data marks aren't derived yet, so fall back to any sensible default dark categorical set. Done when every shortlisted form has been rendered — none dropped silently for seeming redundant or hard to implement.

4. **Explain each rendered form** using the template below, drawing every claim from what the render actually shows, not boilerplate copied from the catalog entry. Done when all four sections are filled for every rendered form.

5. **Rank the gallery (optional)** — most relevant to the user's stated question first.

## Output template (per visualization)

- **Why this form** — what in the profile made it a match.
- **Insights** — patterns, trends, anomalies, or relationships actually visible in the render.
- **Strengths / limitations** — from the catalog entry, adjusted for what this specific render shows.
- **Best used for** — the analytical question this form answers better than the others in the gallery.

See `references/catalog.md` for the full set of forms, grouped by the structure in the data they surface: comparison, distribution, relationship, composition, trend & time, hierarchy, network, geospatial, multivariate.
