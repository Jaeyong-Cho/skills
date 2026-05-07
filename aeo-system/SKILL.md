---
name: aeo-system
description: |
  Analyze and evolve multi-repo system boundaries: find where a feature belongs, decide whether to split or combine repos, understand how services relate, and determine which executables are needed. Produces a system ADR when a boundary decision is confirmed.
  Triggers: "aeo-system", "where does this feature go", "should I split this repo", "which service owns this", "new service or existing", "how do these repos work together", "system architecture", or any question about repo/service boundaries.
---

# AEO System Architecture

Use this skill to answer boundary questions across repos. A system ADR is the output of a decision — run analysis first.

Sub-repo registry: `.aeo/repos.toml` in the architecture repo.

```toml
[repos]
auth-service    = "../auth-service"
order-service   = "../order-service"
payment-service = "../../payment/payment-service"
```

---

## Step 1: Read the current system

```bash
cat .aeo/repos.toml
```

For each registered repo, read its ADRs and source structure to build a map of what each service owns and does:

```bash
ls <path>/.aeo/src/adr/
ls <path>/src/
```

Build a picture: which entities does each service own, what does it expose, what does it consume?

---

## Step 2: Answer the question

Pick the question type and apply the matching lens:

**"Where does this feature go?"**
- Does it fit cleanly inside one service's existing entity/value boundary? → add it there
- Does it require a new entity that doesn't belong to any current service? → new service
- Does it coordinate two services without owning anything? → method layer in an existing orchestrator

**"Should I split this repo?"**
- Find parts that have different change rates, different owners, or different deployment needs
- A good split: the two halves rarely need to change together
- A bad split: they share entities or would need a synchronous contract just to do basic work

**"Should I combine these repos?"**
- If two repos always change together, they share a hidden entity — find it and make it explicit in one repo
- Combine when the contract between them is more expensive than the coupling

**"Which services/executables are needed?"**
- Each executable should own one bounded context: one set of stable entities + the methods to act on them
- If an executable mixes two unrelated entity groups, it's a candidate for splitting

**"How do these repos work together?"**
- Trace the flow: which service initiates, which owns the entity, which consumes
- Draw a Mermaid diagram showing ownership and communication direction

---

## Step 3: Write a system ADR (when a decision is made)

System ADR IDs: `SYS-0001`, `SYS-0002`, etc. Output: `.aeo/src/adr/SYS-<ID>-<slug>.md`

Use the same `aeo` grill-me and ADR template. Add two extra sections:

**Services involved** — which repos are affected and how
**Contract** — the exact interface: API endpoint, event schema, or shared model

After writing, link from affected sub-repo ADRs:
```markdown
## System context
Implements [SYS-0001](../architecture/.aeo/src/adr/SYS-0001-user-session.md)
```

---

## Step 4: Documentation and commit

Write system docs with `aeo-docs`. Commit with type `feat(system)` using `../aeo/references/commit.md`.
