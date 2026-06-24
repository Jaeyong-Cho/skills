# Refact Reference

## The Coordinate System

Every architecture is plotted on three axes. The axis you move along determines the operation type:

```
         ↑ Abstractness (vertical)
         │   high-level use cases
         │     domain logic
         │       infrastructure
         │─────────────────────────→ Subdomain (horizontal)
        ╱        domain A | domain B | domain C
       ╱ Sharding (diagonal — parallel deployed instances)
```

- **Abstractness** (vertical) — inversely proportional to distance from the system's clients; a graphical UI is highly abstract (users interact with it directly), while device drivers at the opposite end operate in raw bits and registers; intermediate layers (routing, proxies, OS) are placed toward the top even if not highly abstract, to keep diagrams simple — high-level above, low-level below; vertical split extracts a layer
- **Subdomain** (horizontal) — distinct functional areas side by side; horizontal split separates domains
- **Sharding** (diagonal) — multiple deployed instances; combine collapses unnecessary instances
-
## Code Structure and the Level of Pain

The right structure depends on size. Decomposing too early adds complexity; not decomposing at scale causes pain. The clarity force shifts direction as the codebase grows:

| Scale | Appropriate structure | Pain if ignored |
|-------|-----------------------|-----------------|
| ~10 lines | Simple script — no classes, no modules | Over-engineering kills velocity |
| ~100 lines | Procedures or classes — divide into named units | Everything-in-one starts to hurt |
| ~5 000 lines | Modules → classes → methods hierarchy | A 5k-line file is unreadable |
| ~100 000 lines | Services — separate deployable units | Merge conflicts, compile times, nobody understands the whole |

**The rule**: switch to the next level of decomposition when staying at the current level becomes more painful than the added complexity of splitting.

Each transition is a vertical split (extracting a layer of abstraction) or a horizontal split (separating a subdomain) — never both at once.

## Cohesers — push toward unity

| Force | When active |
|-------|-------------|
| Debuggability | Single process is easier to trace and reproduce |
| Data consistency | No distributed state or sync needed |
| Small team / early stage | Speed and simplicity matter more than flexibility |
| Data analysis | Fewer integration points to query across |

## Decouplers — push toward separation

| Force | When active |
|-------|-------------|
| Variability | Conflicting requirements need multiple implementations |
| Location | Components must run on different machines or devices |
| Conway's Law | Team boundaries demand code boundaries |
| Scale | Parts must scale independently |

## Bidirectional forces

| Force | Favors cohesion when... | Favors decoupling when... |
|-------|------------------------|--------------------------|
| Clarity | Small system, few concepts | Large system, many concepts |
| Velocity | Single team, early stage | Multiple teams, parallel work |
| Throughput | Integration is fast enough | Distribution unlocks more |

## Evolution rule

> Only pay for decoupling when a decoupler is present and active. Cohesion is the default.

Typical progression: **Monolith → Layers → Services** as decouplers accumulate.
Contraction happens when cohesers outweigh the original decoupler that justified a split.

