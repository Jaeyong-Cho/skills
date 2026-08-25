# Diagram Selection

Copied from `@skills/diagram-design`'s §2 "When to Use" and §3 "Visual-type guide" (its `SKILL.md`, v2.4) — kept local so picking a figure's type doesn't require loading that skill's much larger `SKILL.md`. If that skill's table changes, re-sync this file by hand.

## When to use a diagram at all

Use one of the 28 types below when a reader will learn more from a visual than from prose, a table, or a bulleted list.

**Don't draw a diagram for:**
- Lists of things → table or bullets.
- Simple before/after → table.
- One-shape "diagrams" → just write the sentence.

Before drawing, ask: *Would the reader learn more from this than from a well-written paragraph?* If no, don't draw.

## Visual-type guide (28)

| If you're showing… | Use | `../diagram-design/references/…` |
|---|---|---|
| Components + connections in a system | Architecture | `type-architecture.md` |
| Legacy IT landscape grouped by phase/department | IT current-state | `type-it-state.md` |
| Decision logic with branches | Flowchart | `type-flowchart.md` |
| Time-ordered messages between actors | Sequence | `type-sequence.md` |
| States + transitions + guards | State machine | `type-state.md` |
| Entities + fields + relationships | ER / data model | `type-er.md` |
| Events positioned in time | Timeline | `type-timeline.md` |
| Cross-functional process with handoffs | Swimlane | `type-swimlane.md` |
| Two-axis positioning / prioritization | Quadrant | `type-quadrant.md` |
| Multiple entities scored across 3-5 criteria | Radar / Spider | `type-radar.md` |
| Reinforcing cycle / flywheel | Loop | `type-loop.md` |
| Hierarchy through containment / scope | Nested | `type-nested.md` |
| Parent → children relationships | Tree | `type-tree.md` |
| Ownership, reporting, routing, escalation | Org chart | `type-org-chart.md` |
| Stacked abstraction levels | Layer stack | `type-layers.md` |
| Overlap between sets | Venn | `type-venn.md` |
| Ranked hierarchy or conversion drop-off | Pyramid / funnel | `type-pyramid.md` |
| Quantitative comparison across categories | Bar chart | `type-bar.md` |
| Part-of-whole where relative size is the story | Treemap | `type-treemap.md` |
| Continuous trends over time, or two-state change | Line chart | `type-line.md` |
| Tasks and phases on a timeline | Gantt | `type-gantt.md` |
| Distribution/correlation between two variables | Scatter plot | `type-scatter.md` |
| End-to-end data stack on a container cluster | High-Level | `type-high-level.md` |
| Multi-actor sequential process with data handoffs | Process | `type-process.md` |
| Multi-tier data storage with quality levels | Medallion | `type-medallion.md` |
| Role-scoped data flow across a pipeline | Data flow | `type-data-flow.md` |
| Integration topology of a data platform | DP integration | `type-dp-integration.md` |
| Per-role / per-component access matrix | DP security matrix | `type-dp-security-matrix.md` |

## Rules of thumb

- If a 3-column table communicates the same thing, pick the table.
- If two types seem useful, pick the dominant axis of what the figure shows.
- Above 9 nodes, it's probably two diagrams — split into an overview + detail rather than cramming one.
