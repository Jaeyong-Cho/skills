---
name: aeo-system
description: |
  Write system-level ADRs, PoCs, and documentation that span multiple repositories. Manages a dedicated architecture repo as the single source of truth for cross-repo contracts, service ownership, and shared domain models. Sub-repos reference system decisions by ID.
  Triggers: "aeo-system", "system ADR", "cross-repo design", "system architecture", "service contract", "multi-repo design", or when a decision affects more than one repository.
---

# AEO System Architecture

The architecture repo is the single source of truth for decisions that span services. Sub-repos handle their own internal decisions with `aeo`. Only use this skill when a decision crosses a repository boundary.

**One system ADR = one cross-repo contract or boundary decision.** Internal service decisions belong in the service repo.

---

## Setup

### Architecture repo

Run `aeo-init` in the architecture repo. System ADRs use the prefix `SYS-`:

```bash
mkdir -p .aeo/src/adr .aeo/src/poc .aeo/src/docs
```

IDs: `SYS-0001`, `SYS-0002`, etc.

### Sub-repo pointer

In each sub-repo, create `.aeo/system.toml`:

```toml
repo = "../architecture"   # relative or absolute path to the architecture repo
```

Sub-repos read this to locate system ADRs when referencing them.

---

## Step 1: Scope check

Before writing, confirm the decision truly crosses a repo boundary:

- Does it define an API contract, event schema, or shared data model?
- Does it assign ownership of a domain entity to a specific service?
- Does it affect how two or more services communicate or coordinate?

If yes → write a system ADR here. If no → use `aeo` in the service repo.

---

## Step 2: Write a system ADR

Use the same `aeo` grill-me and ADR template. Add two extra sections:

**Services involved** — which repos are affected and how:
```
- auth-service: owns User entity, exposes /session
- order-service: consumes session token, reads User.id only
```

**Contract** — the exact interface crossing the boundary:
- API: endpoint, method, request/response shape
- Event: name, schema, producer, consumers
- Shared model: entity name, fields, ownership rules

System ADR output: `.aeo/src/adr/SYS-<ID>-<slug>.md`

---

## Step 3: Link from sub-repo ADRs

When a service ADR depends on a system decision, add a reference:

```markdown
## System context

Implements [SYS-0001 User Session Contract](../architecture/.aeo/src/adr/SYS-0001-user-session.md)
```

---

## Step 4: Scan sub-repos (optional)

To build a cross-service view, list which system ADRs each sub-repo implements:

```bash
grep -r "SYS-" */aeo/src/adr/ 2>/dev/null
```

---

## Step 5: Documentation and commit

Write system docs with `aeo-docs`. Use the commit format from `../aeo/references/commit.md` with type `feat(system)`.
