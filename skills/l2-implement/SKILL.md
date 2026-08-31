---
name: l2-implement
description: Implement one L2 domain function directly from a plain-language description of a business rule/behavior, via TDD, per references/abstraction-levels.md — depends on L3 only through an interface, never a concrete implementation. Invoke as /l2-implement, or via l1-implement.
disable-model-invocation: true
---

# L2 Implement

Turn a human's plain-language description of one business rule into a real, TDD-built L2 function — no plan file, no round-based interview. The lighter path for a single domain rule that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

Before starting: if the description covers more than one business rule, needs a new domain concept/entity to hold it, or reads like a whole feature, **MUST STOP** and recommend `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` instead (or `@skills/refact-grill-me` if this is about splitting existing code) — name why in one line. A single, clear business rule skips this and goes straight to step 1.

1. **Name the L2 function.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) in domain terms, not technical terms — if it needs "and", it's more than one rule; go back to the scope check.
2. **Find its L3 dependency, if any.** Does deciding this rule need a technical capability (current price, inventory count, a stored record, ...)? If so it depends on an *interface* for that capability, never a concrete implementation, per `../references/abstraction-levels.md`. Dispatch a sub-agent to check the repo: does the interface exist, does an implementation of it exist — reuse before creating, per `../references/deep-modules.md`. If neither exists, that's an `@skills/l3-implement` follow-up, not this skill's job — name it plainly, and depend on the interface (declared but not yet implemented) so this function still compiles/type-checks.
3. **Write the failing test first.** One test through the function's public behavior (input → expected decision/output), not through its internals; mock only the L3 interface from step 2 if the function depends on one. Run it — confirm RED, per `../references/tdd.md`.
4. **Write the L2 function.** Domain terminology, the business rule only — no direct database/HTTP/SDK/filesystem call inline; call the L3 interface from step 2 instead, if there is one, per `../references/abstraction-levels.md`'s L2 rules. Name it per `../references/naming.md`.
5. **Green, then refactor.** Run the test from step 3 — confirm GREEN. Check for deep-module opportunities (`../references/deep-modules.md`), then re-run the test — still green.

Completion criterion: the L2 function exists, expresses the rule in domain terms, depends on L3 only through an interface if it depends on it at all, and its test went RED → GREEN for real, shown, not asserted from memory.

Tell the human the function's file:line, its test file:line, whether an L3 interface/implementation was reused, missing, or newly declared, and the test result, when done.
