---
name: l3-implement
description: Implement one L3 mechanism function directly from a plain-language description of a technical operation (DB, HTTP, SDK, filesystem, ...), per references/abstraction-levels.md — exposes a simple interface upward, no business decisions inside. Code only, no test — see @skills/func-test. Invoke as /l3-implement, or via l1-implement/l2-implement/to-code.
disable-model-invocation: true
---

# L3 Implement

Turn a human's plain-language description of one technical operation into a real L3 function — no plan file, no round-based interview. The lighter path for a single mechanism that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

1. **Name the L3 function and its interface.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) in mechanism terms (the technical thing it does), and name the interface/contract it implements for L2 to depend on. Dispatch a sub-agent to check the repo for an existing one first — reuse before creating, per `../references/deep-modules.md`; create the interface only if none exists and the description makes clear what L2 needs from it.
2. **Write the L3 function.** Technical mechanism only — no business decision beyond what the mechanism itself strictly requires (a retry/timeout policy is fine, a discount rule is not). Hide the SDK/HTTP/DB details behind the interface from step 1, per `../references/abstraction-levels.md`'s L3 rules and rule 6 (interfaces define contracts, not mechanisms). Name it per `../references/naming.md`. No `L1`/`L2`/`L3` or skill-name jargon in code comments/docstrings — that's this project's internal shorthand, not for the codebase.
3. **Check for deep-module opportunities** (`../references/deep-modules.md`: narrow the interface, hide more of the client/SDK).

This skill only writes code — no test. Run `@skills/func-test` on the finished function separately when it needs coverage; this is a deliberate deviation from `../references/tdd.md`'s RED-first default, scoped to this lightweight path.

Completion criterion: the L3 function exists behind a named interface, no business decision embedded in it.

Tell the human the function's file:line, its interface, and that `@skills/func-test` is the next step for coverage (against the real mechanism, not a mock).
