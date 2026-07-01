---
name: to-html
description: Render any file as a rich Kanagawa-themed HTML document with visual components. Use when the user says "to html", "render this", "convert to html", "show this visually", "visualize this", or points at a file and asks for a visual or HTML view.
---

# To HTML

Read the source file the user points at. If no path given, use the most recently written output file. Read `../references/kanagawa.css`.

Generate a self-contained HTML document and write it beside the source with a `.html` extension (same directory, same filename stem). Never modify the source.

## HTML boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{source filename}</title>
  <style>
    {full contents of kanagawa.css}
  </style>
</head>
<body>
  {content}
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({ startOnLoad: true, theme: 'base', themeVariables: {
      primaryColor: '#2A2A37', primaryTextColor: '#DCD7BA', primaryBorderColor: '#7E9CD8',
      lineColor: '#727169', secondaryColor: '#1F1F28', tertiaryColor: '#2A2A37',
      edgeLabelBackground: '#1F1F28', clusterBkg: '#2A2A37',
      titleColor: '#DCD7BA', nodeTextColor: '#DCD7BA', edgeStrokeColor: '#727169'
    }});
  </script>
</body>
</html>
```

## Section → card mapping

Each `## Heading` becomes a `.card` div with a matching variant. Map by what the heading contains:

| Heading contains | Card class |
|---|---|
| Goal, Info | `.card.goal` |
| Failure, Error, Bad | `.card.failure` |
| Ambiguous, Warning, Zone | `.card.ambiguous` |
| Good, Direction, Decision, Success | `.card.good` |
| Action, Steps, Sequence | `.card.action` |
| Context, Design, Architecture, Special | `.card.special` |
| Anything else | `.card` (no variant) |

Card structure:
```html
<div class="card {variant}">
  <div class="card-title">{heading text}</div>
  {section content}
</div>
```

## Visual components — chosen by content, not applied uniformly

- **Numbered lists inside Action / Steps / Sequence sections** → `.checklist` with `<input type="checkbox">` per item
- **Bulleted lists inside Failure / Good / Ambiguous / Evaluation sections** → `.checklist` with `<input type="checkbox">` per item
- **All other lists** → standard `<ul>` or `<ol>`
- **Tables** → `<table>` with `<th>` headers (kanagawa.css styles them automatically)
- **Code blocks** → `<pre><code>`
- **Inline code** → `<code>`

## Mermaid diagrams

Only generate a mermaid diagram when the source text explicitly states a relationship using:
- Arrows: `→`, `->`, `⟶`, `=>`
- Phrases: "leads to", "depends on", "feeds into", "flows to", "calls", "triggers"

Pick the diagram type that best fits the content:
- Pipeline / sequence of steps → `flowchart LR` or `flowchart TD`
- System interactions over time → `sequenceDiagram`
- Data structures / classes → `classDiagram`
- Timeline / schedule → `gantt`

Every mermaid block **must** open with this init directive:
```
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#2A2A37', 'primaryTextColor': '#DCD7BA', 'primaryBorderColor': '#7E9CD8', 'lineColor': '#727169', 'secondaryColor': '#1F1F28', 'tertiaryColor': '#2A2A37', 'edgeLabelBackground': '#1F1F28', 'clusterBkg': '#2A2A37', 'titleColor': '#DCD7BA', 'nodeTextColor': '#DCD7BA'}}}%%
```

Wrap each diagram in `<div class="mermaid">`.

## Faithfulness rules — check before writing

1. **Complete**: count the `##` sections in the source. Confirm the same count of cards exists in the HTML. If any section is missing, add it.
2. **No additions**: no heading or card appears in the HTML that isn't in the source. If one was added, remove it.
3. **No inferred diagrams**: a diagram is only present if the source text contains explicit relationship language (arrows or the phrases above). Never draw connections inferred from context or proximity.

Verify all three before writing the output file.
