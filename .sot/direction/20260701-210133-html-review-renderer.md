# To-HTML Skill

## Goal

A general-purpose `/to-html` skill that takes any file the user points at and renders it as a rich, readable HTML document. Kanagawa theme throughout. Visual components (checkboxes, color-coded sections, simple diagrams) are chosen to fit the content — not applied uniformly. The human opens the HTML to understand the content better than a plain .md file allows.

## Failure Criteria

- **Information loss**: the HTML omits any content from the source — sections, items, steps. Human makes decisions based on an incomplete picture.
- **Hallucinated structure**: the agent adds headings, groupings, or relationships that weren't in the source. The HTML presents a distorted version of the original — not a faithful render.

## Ambiguous Zone

- Agent reorders list items visually (e.g. puts checkboxes before prose) without losing content — acceptable if semantically equivalent.
- Agent adds minor visual grouping (e.g. wraps related fields in a card) that reflects the source structure — acceptable if it maps 1:1 to source sections.

## Direction

Build a standalone `/to-html` skill. The user points at any file (or says "convert the last result") and the skill:
1. Reads the source content
2. Generates an HTML document — Kanagawa theme, visual components adapted to content type (checkboxes for action steps, color-coded sections for good/ambiguous/bad zones, simple flow diagrams only where explicit relationships are stated)
3. Writes the HTML beside the source file (same path, `.html` extension)

The skill is not tied to the pipeline. It has no round-trip HTML-to-MD requirement. It is a viewing tool only.

## Constraints

- Content must be complete — every section and item from the source appears in the HTML
- Agent must not add structure, groupings, or relationships not present in the source
- Visual components are chosen per content type, not applied uniformly to everything
- Output lives beside the source file (same directory, `.html` extension)

## Out of Scope

- Subagent triggered automatically at end of directing/planning/evaluate
- Round-trip HTML-to-MD conversion for pipeline input
- Real-time browser editing
- Any pipeline integration
