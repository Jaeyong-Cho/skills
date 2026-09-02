---
name: l2-implement
description: Implement one L2 domain function directly from a plain-language description of a business rule/behavior, per references/abstraction-levels.md — depends on L3 only through an interface, never a concrete implementation. Code only, no test — see @skills/func-test. Invoke as /l2-implement, or via l1-implement/to-code.
disable-model-invocation: true
---

# L2 Implement

Turn a human's plain-language description of one business rule into a real L2 function — no plan file, no round-based interview. The lighter path for a single domain rule that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

1. **Name the L2 function.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) in domain terms, not technical terms — if it needs "and", it's more than one rule; go back to the scope check.
2. **Find its L3 dependency, if any.** Does deciding this rule need a technical capability (current price, inventory count, a stored record, ...)? If so it depends on an *interface* for that capability, never a concrete implementation, per `../references/abstraction-levels.md`. Dispatch a sub-agent to check the repo: does the interface exist, does an implementation of it exist — reuse before creating, per `../references/deep-modules.md`. If neither exists, that's an `@skills/l3-implement` follow-up, not this skill's job — name it plainly, and depend on the interface (declared but not yet implemented) so this function still compiles/type-checks.
3. **Write the L2 function.** Domain terminology, the business rule only — no direct database/HTTP/SDK/filesystem call inline; call the L3 interface from step 2 instead, if there is one, per `../references/abstraction-levels.md`'s L2 rules. Name it per `../references/naming.md`. No `L1`/`L2`/`L3` or skill-name jargon in code comments/docstrings — that's this project's internal shorthand, not for the codebase.
4. **Check for deep-module opportunities** (`../references/deep-modules.md`) — narrow interface, hide complexity, no duplication.

This skill only writes code — no test. Run `@skills/func-test` on the finished function separately when it needs coverage; this is a deliberate deviation from `../references/tdd.md`'s RED-first default, scoped to this lightweight path.

Completion criterion: the L2 function exists, expresses the rule in domain terms, and depends on L3 only through an interface if it depends on it at all.

Tell the human the function's file:line, whether an L3 interface/implementation was reused, missing, or newly declared, and that `@skills/func-test` is the next step for coverage.
