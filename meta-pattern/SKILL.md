---
name: meta-pattern
description: Identify and evolve a system's architecture using meta-patterns, the 3-axis coordinate system (Abstractness / Subdomain / Sharding), and coheser/decoupler forces. Reads the codebase, plots the current structure, names the pattern, and recommends the next evolutionary step. Use when user wants to structure a system, evolve an architecture, identify coupling/cohesion tradeoffs, or says "meta-pattern", "which architecture", "how should I structure this", "should I split this".
---

# Meta-Pattern

Architecture is structure. Plot first, name the pattern, then evolve using forces.

See [REFERENCE.md](REFERENCE.md) for the full pattern catalog and force definitions.

## Workflow

1. **Read codebase** — understand current structure if in a project; skip if not
2. **Plot on coordinates** — map the system onto the three axes (see below); describe where components sit
3. **Name the pattern** — identify which meta-pattern the plot matches
4. **Analyze forces** — list active cohesers (push together) and decouplers (push apart)
5. **Recommend evolution** — based on forces, name the next structural move; do not recommend more decoupling than forces justify

## The Three Axes

```
         ↑ Abstractness (high-level → low-level)
         │   Orchestrator
         │     Services
         │       DB queries
         │─────────────────────→ Subdomain (domain A | domain B | ...)
        ╱
       ╱ Sharding (diagonal — multiple deployed instances)
```

- **Abstractness** (vertical) — high-level use cases at top, low-level details at bottom
- **Subdomain** (horizontal) — distinct functional areas side by side
- **Sharding** (diagonal) — parallel deployed instances of the same module

## Forces

**Cohesers** (push toward unified code):
- Debuggability — single process is easier to trace
- Data consistency — no distributed state
- Small team / early stage — speed > flexibility

**Decouplers** (push toward separation):
- Variability — conflicting requirements need multiple implementations
- Location — components must run on different machines
- Conway's Law — team boundaries demand code boundaries
- Scale — throughput requires independent scaling

**Bidirectional** (context-dependent):
- Clarity — favors cohesion in small systems, decoupling in large ones
- Velocity — cohesion is fast early; decomposition enables parallelism later
- Throughput — integration is faster; distribution enables more of it

## Evolution rule

> Only pay for decoupling when a decoupler justifies it. Cohesion is the default; split when forced.

Systems typically evolve: **Monolith → Layers → Services** as decouplers accumulate. They can also contract when cohesers outweigh decouplers.
