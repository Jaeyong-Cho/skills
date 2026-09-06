---
name: l2-implement
description: Implement one L2 domain function directly from a plain-language description of a business rule/behavior, per references/abstraction-levels.md — depends on L3 only through an interface, never a concrete implementation. Code only, no test. Invoke as /l2-implement.
disable-model-invocation: true
---

# L2 Implement

Turn a human's plain-language description of one business rule into a real L2 function — no plan file, no round-based interview. The lighter path for a single domain rule that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

1. **Name the L2 function.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) in domain terms, not technical terms — if it needs "and", it's more than one rule; go back to the scope check.
2. **Find its L3 dependency, if any.** Does deciding this rule need a technical capability (current price, inventory count, a stored record, ...)? If so it depends on an *interface* for that capability, never a concrete implementation, per `../references/abstraction-levels.md`. Dispatch a sub-agent to check the repo: does the interface exist, does an implementation of it exist — reuse before creating, per `../references/deep-modules.md`. If neither exists, that's an `@skills/l3-implement` follow-up, not this skill's job — name it plainly, and depend on the interface (declared but not yet implemented) so this function still compiles/type-checks.
3. **Place and write the L2 function.** Dispatch a sub-agent to find where sibling L2 rules for this domain already live in the repo (module/folder convention) — put it there; open a new file only when no existing one fits. Domain terminology, the business rule only — no direct database/HTTP/SDK/filesystem call inline; call the L3 interface from step 2 instead, if there is one, per `../references/abstraction-levels.md`'s L2 rules. Name it per `../references/naming.md`. No `L1`/`L2`/`L3` or skill-name jargon in code comments/docstrings — that's this project's internal shorthand, not for the codebase.
4. **Check for deep-module opportunities** (`../references/deep-modules.md`) — narrow interface, hide complexity, no duplication.
5. **Review the diff for layer mixing.** Read back the actual function you just wrote against `../references/abstraction-levels.md`'s smells table — no L2-leaking-L3 (a business rule mixed with an inline HTTP/DB call in the same function), no Domain rule hidden as plumbing (a real rule buried in a `_helper`/`_process` name). Found one → fix it (extract the mechanism behind the L3 interface, rename to a domain-revealing name) before finishing.

This skill only writes code — no test. Add and run a real test for the finished function separately when it needs coverage; this is a deliberate deviation from `../references/tdd.md`'s RED-first default, scoped to this lightweight path.

Completion criterion: the L2 function exists, expresses the rule in domain terms, depends on L3 only through an interface if it depends on it at all, and step 5's layer-mixing review found nothing left inline.

Tell the human the function's file:line, whether an L3 interface/implementation was reused, missing, or newly declared, that the layer-mixing review passed clean, and that a real test is the next step for coverage.
