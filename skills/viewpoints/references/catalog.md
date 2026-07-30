# Visualization Catalog

Each entry: what it's best for, what data it requires, its strengths and limitations co-located, and when to avoid it in favor of a sibling form in the same category.

## Comparison

**Bar chart** — Best for comparing a metric across discrete categories (up to ~15). Requires 1 categorical + 1 numeric. Strength: precise magnitude comparison via a shared baseline. Limitation: unreadable past ~15-20 categories; one metric only. Avoid when the category count is large (sort and truncate, or use a dot plot) or the goal is change over time (use a trend form instead).

**Grouped / stacked bar** — Best for comparing a metric across categories *and* a second grouping dimension. Requires 2 categorical + 1 numeric. Strength: adds a second comparison axis. Limitation: stacked segments beyond the first are hard to compare precisely. Avoid when there are more than ~4 subgroups — use small multiples instead.

**Dot / lollipop plot** — Best for a ranked comparison across many categories. Requires 1 categorical + 1 numeric. Strength: less visual clutter than bars, scales further. Limitation: less familiar to non-technical audiences.

**Radar / spider chart** — Best for comparing a handful of entities (<=5) across several metrics at once. Requires 1 categorical (entities) + 3-8 numeric axes. Strength: a compact multi-metric silhouette per entity. Limitation: area is perceptually misleading and axis order changes the shape's meaning. Avoid when axes aren't on comparable scales, or entity/axis count exceeds ~8 — use small multiples of bar charts.

## Distribution

**Histogram** — Best for the shape of one numeric variable (modality, skew, outliers). Requires 1 numeric, ideally 30+ points. Limitation: bin width choice changes the story; hides exact values. Avoid when comparing distributions across many groups — use a box or violin plot.

**Box plot** — Best for comparing spread and outliers across groups. Requires 1 categorical + 1 numeric. Strength: compact, scales to many groups, robust to outliers. Limitation: hides multimodality and per-group sample size. Avoid when n per group is very small (<5) or the audience needs the full shape — use a violin plot.

**Violin plot** — Best for comparing full distribution shape across groups. Requires 1 categorical + 1 numeric, ideally n>=20 per group. Strength: reveals multimodality box plots hide. Limitation: smoothing can imply structure the sample doesn't support at low n.

**Ridgeline plot** — Best for comparing many (5+) distributions at once, often ordered (e.g. by time or rank). Requires 1 ordered categorical + 1 numeric. Strength: shows how distribution shape shifts along the ordering. Limitation: overlapping ridges occlude data if not spaced well.

## Relationship

**Scatter plot** — Best for the relationship between two numeric variables. Requires 2 numeric. Strength: shows correlation, clusters, and outliers directly. Limitation: overplotting hides density past a few thousand points. Avoid when point count is very large (use a hexbin/density heatmap) or one variable is categorical (use a box or strip plot).

**Bubble chart** — Best for a relationship between two numeric variables plus a third (size) and optionally a fourth (color). Requires 3-4 numeric. Strength: adds dimensions without a new axis. Limitation: size is perceived non-linearly; easy to overload past 3 encoded variables. Avoid when precise size comparison matters — use faceted scatter plots instead.

**Correlation heatmap** — Best for relationships among many numeric variables at once. Requires 3+ numeric variables. Strength: surfaces which variable pairs deserve a closer look. Limitation: captures linear correlation only, and color-scale choice can exaggerate weak correlations.

## Composition

**Pie / donut chart** — Best for share-of-whole with <=5 categories at a single point in time. Requires 1 categorical + 1 numeric that sums to a whole. Limitation: angle comparison is unreliable past ~5 slices. Avoid when comparing composition across time, or with more than ~5 categories — use a stacked bar or treemap.

**Stacked area chart** — Best for how composition of a whole changes over time. Requires 1 time + 1 categorical + 1 numeric. Strength: shows total trend and share shift together. Limitation: middle bands lack a shared baseline, so precise reading is hard. Avoid when precise values matter more than overall shape — use small multiples of line charts.

**Treemap** — Best for composition within a nested/hierarchical whole. Requires hierarchical categorical + 1 numeric (size). Strength: shows share and hierarchy together, scales to many leaf categories. Limitation: deep hierarchies get hard to label; area comparison is distorted by aspect ratio.

## Trend & time

**Line chart** — Best for how one or a few numeric series change over time. Requires 1 time + 1+ numeric. Limitation: more than ~5 lines becomes an unreadable "spaghetti chart". Avoid when series count is large (use small multiples) or the x-axis isn't truly ordered/continuous.

**Small multiples** — Best for comparing the same trend across many (5+) groups without overlapping lines. Requires 1 time + 1 categorical (many levels) + 1 numeric. Strength: every panel stays legible. Limitation: harder to compare precise values across panels; needs consistent axes to stay honest.

**Calendar heatmap** — Best for daily-granularity patterns over months or years (activity, seasonality). Requires 1 date + 1 numeric. Strength: surfaces weekly/seasonal rhythm at a glance. Limitation: poor for reading exact magnitude; only works at day granularity.

## Hierarchy

**Tree diagram** — Best for the parent-child structure itself (org charts, taxonomies), independent of any numeric weight. Requires hierarchical categorical only. Limitation: wide trees need a lot of horizontal space.

**Sunburst** — Best for hierarchy plus a numeric weight per node, viewed radially. Requires hierarchical categorical + 1 numeric. Strength: compact, shows depth and share together. Limitation: outer-ring labels get cramped; angle comparison across rings is hard.

Treemap (see Composition) also serves hierarchy-plus-size and is often the better choice when labels need to stay readable.

## Network

**Node-link graph** — Best for entities and the relationships between them. Requires an edge list (source, target), optional node/edge weights. Strength: the only form that shows connectivity structure directly. Limitation: layout becomes an illegible "hairball" past a few hundred nodes; needs a force-directed/interactive library, not a static-chart library. Avoid when the question is about entity attributes rather than connections — use a table or heatmap instead.

**Arc / chord diagram** — Best for flows or relationships among a modest number of categories (<=20). Requires entities + weighted edges. Strength: shows flow volume between pairs cleanly. Limitation: doesn't scale past ~20-30 entities.

## Geospatial

**Choropleth map** — Best for a numeric variable aggregated by geographic region. Requires a region identifier (country, state, etc.) + 1 numeric. Strength: leverages familiar geography for pattern recognition. Limitation: large regions visually dominate regardless of their value (area bias); needs a mapping-capable library. Avoid when regions vary hugely in area and the metric isn't area-normalized — use a rate, not a raw count.

**Point map** — Best for individual located events or entities. Requires latitude + longitude, optional numeric for size/color. Strength: shows exact location and density/clusters. Limitation: overplotting in dense areas unless clustered.

## Structure & flow

For subjects with a structural face — a system, codebase, algorithm, schema, or filesystem — rather than (or alongside) tabular data. Render with mermaid or graphviz to SVG.
P.S. Prefer top-down direction diagram. Because the narrow left-right diagram is not readable.

**Flowchart** — Best for a process or algorithm's control flow: steps, branches, and loops. Requires an ordered sequence of steps with decision points. Strength: makes branching logic and dead ends legible. Limitation: sprawls when branches multiply; not for data magnitudes. Render with mermaid `flowchart`.

**Sequence diagram** — Best for interactions between actors/components over time — who calls whom, in what order. Requires participants + ordered messages. Strength: shows request/response ordering and lifelines clearly. Limitation: one scenario per diagram; parallel paths get busy. Render with mermaid `sequenceDiagram`.

**Architecture diagram** — Best for a system's components and how they connect (services, stores, queues, boundaries). Requires components + their connections/dependencies. Strength: conveys topology at a glance. Limitation: no fixed grammar — easy to overcrowd; keep to one abstraction level. Render with mermaid `flowchart` or graphviz.

**Entity-relationship diagram** — Best for a data model: entities, their attributes, and relationship cardinality. Requires entities + typed relationships (1:1, 1:N, N:M). Strength: the canonical view of a schema. Limitation: attribute-heavy entities crowd; not for instance data. Render with mermaid `erDiagram`.

**State diagram** — Best for the states of an entity and the transitions between them. Requires states + transition triggers. Strength: surfaces unreachable or terminal states. Limitation: state explosion with many orthogonal dimensions. Render with mermaid `stateDiagram`.

**Directory tree** — Best for a filesystem or project's nested structure. Requires a path hierarchy. Strength: shows nesting and grouping directly. Limitation: deep or wide trees need truncation. Render as an indented tree to SVG.

Node-link graph (see Network) also serves free-form dependency or relationship graphs that aren't a strict hierarchy.

## Multivariate

**Parallel coordinates** — Best for comparing many entities across many (4+) numeric variables at once. Requires 4+ numeric variables. Strength: scales to more dimensions than a scatter matrix. Limitation: line crossings become illegible past a few dozen entities or a handful of variables; axis order changes readability. Avoid when entity count is large — subsample or aggregate first.

**Scatterplot matrix (SPLOM)** — Best for pairwise relationships among several (3-6) numeric variables at once. Requires 3-6 numeric variables. Strength: every pairwise relationship visible in one view. Limitation: grows quadratically — unreadable past ~6 variables.
