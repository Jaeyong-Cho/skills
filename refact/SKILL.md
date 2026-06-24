---
name: refact
description: Apply a single structural refactoring — vertical split (by abstraction), horizontal split (by subdomain), or combine (merge over-decoupled parts). One operation at a time, grounded in meta-pattern forces. Use when user wants to split a module, extract a layer, separate domains, merge components, or says "refact", "split this", "extract layer", "combine these", "separate domains".
---

# Refact

One structural move at a time. Split or combine — nothing else.

Grounded in the meta-pattern coordinate system and coheser/decoupler forces. See [REFERENCE.md](REFERENCE.md).

Read [meta-pattern](../references/meta-pattern.md), [tdd](../references/tdd.md), [tdd-refactoring](../references/tdd-refactoring.md), [tdd-tests](../references/tdd-tests.md), and [tdd-mocking](../references/tdd-mocking.md) before starting.

## Operations

| Operation | Axis | What changes |
|-----------|------|-------------|
| **Vertical split** | Abstractness ↕ | Extract a layer — separate high-level from low-level concerns in the same component |
| **Horizontal split** | Subdomain ↔ | Separate two domains that grew together into one |
| **Combine** | Any | Merge two components where the decoupler that justified the split no longer applies |

## Workflow

1. **Read** the target file(s) and surrounding context
2. **Identify the operation** — which axis? split or combine?
3. **Grill** — before acting, map every ambiguous or consequential decision this move requires; rank by impact; ask only the high-impact ones in order, one at a time; use `AskUserQuestion` for discrete options (recommended first); skip anything obvious or answerable from the codebase; user can say "wrap up" to move on
4. **Check the force** — name the coheser or decoupler that justifies this move; if none, don't do it
5. **Apply** — make the single structural change; do not refactor anything else in the same pass; all tests must be green before starting — never refactor while RED; run tests after each step; if a test breaks, you changed behavior — undo and try again
6. **Verify** — confirm the split boundary is clean: no circular deps, no leaked internals; all tests still green

## Split rules

- **Vertical**: the lower part must not import the upper part after the split
- **Horizontal**: after split, the two sides must not share internal state or logic — only public interfaces
- Move only what belongs to the new boundary; leave everything else untouched

## Combine rules

- Only combine when a coheser outweighs the original decoupler
- Prefer inlining over wrapping — don't create a new module that just delegates

## Done when

One boundary changed. Tests pass. No other files touched.
