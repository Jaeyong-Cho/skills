---
name: aeo-system
description: |
  Write system-level ADRs, PoCs, and documentation that span multiple repositories. Manages a dedicated architecture repo with a sub-repo registry — can read files directly from registered repos to build cross-service context.
  Triggers: "aeo-system", "system ADR", "cross-repo design", "system architecture", "service contract", "multi-repo design", or when a decision affects more than one repository.
---

# AEO System Architecture

The architecture repo is the single source of truth for decisions that span services. Sub-repos handle their own internal decisions with `aeo`. Only use this skill when a decision crosses a repository boundary.

**One system ADR = one cross-repo contract or boundary decision.** Internal service decisions belong in the service repo.

---

## Setup

Run `aeo-init` in the architecture repo. Then create the sub-repo registry at `.aeo/repos.toml`:

```toml
[repos]
auth-service    = "../auth-service"
order-service   = "../order-service"
payment-service = "../../payment/payment-service"
```

Paths are relative to the architecture repo root. Each sub-repo registers itself here when it joins the system.

System ADR IDs: `SYS-0001`, `SYS-0002`, etc. Output: `.aeo/src/adr/SYS-<ID>-<slug>.md`

---

## Reading sub-repos

Before writing a system ADR, read the relevant sub-repos for context:

```bash
# List registered repos
cat .aeo/repos.toml

# Read a sub-repo's ADRs
ls <path>/.aeo/src/adr/

# Find which sub-repos reference a system ADR
grep -r "SYS-0001" $(cat .aeo/repos.toml | grep -oP '".*?"' | tr -d '"')/.aeo/ 2>/dev/null

# Check a sub-repo's source for divergence from the contract
ls <path>/src/
```

Use this to: understand current state before proposing a contract, find which services are already implementing something, or verify a system ADR is correctly reflected downstream.

---

## Step 1: Scope check

Before writing, confirm the decision truly crosses a repo boundary:

- Does it define an API contract, event schema, or shared data model?
- Does it assign ownership of a domain entity to a specific service?
- Does it affect how two or more services communicate or coordinate?

If yes → write a system ADR here. If no → use `aeo` in the service repo.

---

## Step 2: Write a system ADR

Read sub-repo context first (see above), then use the same `aeo` grill-me and ADR template. Add two extra sections:

**Services involved** — which repos are affected and how:
```
- auth-service: owns User entity, exposes /session
- order-service: consumes session token, reads User.id only
```

**Contract** — the exact interface crossing the boundary:
- API: endpoint, method, request/response shape
- Event: name, schema, producer, consumers
- Shared model: entity name, fields, ownership rules

---

## Step 3: Link from sub-repo ADRs

When a service ADR depends on a system decision, add to the service repo ADR:

```markdown
## System context

Implements [SYS-0001 User Session Contract](../architecture/.aeo/src/adr/SYS-0001-user-session.md)
```

---

## Step 4: Documentation and commit

Write system docs with `aeo-docs`. Use commit format from `../aeo/references/commit.md` with type `feat(system)`.
