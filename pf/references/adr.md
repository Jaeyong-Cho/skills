# Architectural Decision Record (ADR)

Every change — new feature, refactoring, or architecture design — is an ADR. There are no separate document types.

**One ADR = one problem.** If the scope covers multiple independent problems, split into separate ADRs before starting. A sign of too-broad scope: the grill-me branches into unrelated decision trees.

Output: `.pf/src/adr/<ID>-<slug>.md`

For layer definitions, read `references/layers.md`.
For deep module principles, read `references/deep-modules.md`.
For cross-cutting concern design, read `references/aop.md`.

## ID assignment

```bash
ls .pf/src/adr/*.md 2>/dev/null | wc -l
```

Zero-padded 4-digit format: `0001`, `0002`, etc.

---

## Step 1: Grill-me

Run the `grill-me` skill to reach shared understanding before writing.

---

## Step 2: ADR template

```markdown
# [ID] Title

**Status:** Proposed | Accepted | Deprecated | Superseded by [ID]

## Context

What triggered this decision? What problem, need, or violation prompted it?
What constraints are in play?

## User Stories

A numbered list covering all aspects of the change from the user's perspective.

1. As a <actor>, I want <feature>, so that <benefit>
2. ...

Express with diagram

## Decision

What was decided and why. Walk through the three layers:

**Value** — What does the end user need from this? Which features are worth
building? What does success look like? What must never happen?

**Aspect** — How is the need met? Which objects are used and from which angle?
What algorithm or workflow produces the outcome?

**Object** — What objects must exist? Each object must have more than just
data — it should own properties, actions, behaviors, and relationships relevant
to its concern. If logic that belongs to an object lives outside it, the object
is too thin. Are the objects stable and invariant across different uses? Is the
abstraction level right — not too large, not too small?

For each relationship: cardinality, ownership, navigability, aggregate boundary.
View-specific joins belong in the aspect layer.

Call out any leakage between layers.

## Out of Scope

What is explicitly not part of this decision.

## Before / After

Show the current structure and the target structure.
For a greenfield decision, show only the target.
In the **After** diagram, mark every node that is new or changed with a highlight style so the delta is immediately visible:

```
classDef changed fill:#f5a623,stroke:#c97d0a,color:#000
class NewNode,ChangedNode changed
```

Use orange (`#f5a623`) as the default highlight. Nodes that are unchanged carry no class.

**Before:**
```mermaid
graph TD
  ...
```

**After:**
```mermaid
graph TD
  ...
  classDef changed fill:#f5a623,stroke:#c97d0a,color:#000
  class NewOrChangedNode changed
```

## Step-by-Step Plan

Each item is one RED→GREEN TDD cycle. Order from the most end-to-end behavior (tracer bullet) to the most specific.

For each item:
- **Behavior** — what the system does (maps to a User Story)
- **Test target** — which public interface to test through (value entry point, entity action)
- **File** — what to create or modify, and which layer `[value|method|entity]`

Example:

1. User can log in with valid credentials
   - Test: call `login(email, password)` → returns session token
   - Files: `src/commands/login.ts` [value], `src/services/auth.ts` [aspect]
2. User object validates its own password hash
   - Test: `user.verifyPassword(plain)` → true/false
   - Files: `src/models/user.ts` [object]
3. ...
```

After writing the ADR, ask the user to confirm before writing any code.

---

## After implementation is confirmed

Once the user has reviewed the code:

1. Use the `pf-review` skill to review the implementation and update the documentation
2. Mark the ADR status as `Accepted`

## SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./adr/<ID>-<slug>.md)
```
