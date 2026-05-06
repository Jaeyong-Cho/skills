# Design / Architecture Mode

Output: `.aeo/src/design/<ID>-<slug>.md`

## ID assignment

```bash
ls .aeo/src/design/*.md 2>/dev/null | wc -l
```

Zero-padded 4-digit format: `0001`, `0002`, etc.

## Deep Module principle

Every module in the design should be **deep**: its interface should be simpler than its implementation. A wide, thin interface that exposes internals is a design smell regardless of which layer it lives in. When evaluating each component, ask:

- Is the interface narrower than the implementation, or does it expose internal steps?
- Does the caller need to know internal details to use this correctly? (leaky interface)
- Are two components always edited together? (should be one)
- Is the same logic encoded in more than one place? (information leakage / duplication)

If a proposed module is shallow, either deepen it by pulling more behavior inside, or question whether it should exist as a separate module at all.

---

## Document structure (ADR format)

Each design document is an Architecture Decision Record. Use this structure:

```markdown
# [ID] Title

**Status:** Proposed | Accepted | Deprecated | Superseded by [ID]

## Context

Why is this decision being made? What problem or goal triggers this design?
What constraints or forces are in play?

## Decision

What was decided, and why. Walk through the three layers:

**Value** — What does the end user need from this? Which features are worth
building and why? What does a good result look like from the user's perspective?
What must never happen?

**Method** — From which aspect(s) are the entities being used?
What algorithm makes the decision? How do components interact?

**Entity** — What objects must exist? Are they stable and invariant?
Is the abstraction level right — not too large, not too small?

Call out any leakage between layers.

## Alternatives Considered

List the other options evaluated and why they were rejected.

## Consequences

Trade-offs, risks, and what this decision makes easier or harder going forward.

## Before / After

If this design changes an existing system, show a before/after Mermaid diagram.
If it is greenfield, show only the target architecture diagram.

```mermaid
graph TD
  ...
```

## Step-by-Step Plan

Ordered tasks to realize this design. Each step names the file or component,
what it does, and which layer it belongs to. Use the project's own directory
naming — the layer label in brackets is just to show which AEO layer it is.

1. Create `src/models/user.ts` — User entity [entity]
2. Create `src/services/auth.ts` — authentication workflow [method]
3. Create `src/commands/login.ts` — login use-case entry point [value]
4. ...
```

After writing the document, ask the user to confirm before starting implementation.

## SUMMARY.md entry

```markdown
  - [[<ID>] <title>](./design/<ID>-<slug>.md)
```
