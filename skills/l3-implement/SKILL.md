---
name: l3-implement
description: Implement one L3 mechanism function directly from a plain-language description of a technical operation (DB, HTTP, SDK, filesystem, ...), via TDD against the real mechanism, per references/abstraction-levels.md — exposes a simple interface upward, no business decisions inside. Invoke as /l3-implement, or via l1-implement/l2-implement.
disable-model-invocation: true
---

# L3 Implement

Turn a human's plain-language description of one technical operation into a real, TDD-built L3 function — no plan file, no round-based interview. The lighter path for a single mechanism that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

Before starting: if the description bundles more than one external system/mechanism, needs a new vendor/service integration decision, or reads like a whole feature, **MUST STOP** and recommend `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` instead — name why in one line. A single, clear technical operation skips this and goes straight to step 1.

1. **Name the L3 function and its interface.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) in mechanism terms (the technical thing it does), and name the interface/contract it implements for L2 to depend on. Dispatch a sub-agent to check the repo for an existing one first — reuse before creating, per `../references/deep-modules.md`; create the interface only if none exists and the description makes clear what L2 needs from it.
2. **Write the failing test first**, against the real mechanism — a real test DB/HTTP call against a test instance, or the vendor's documented contract — never a mock of the thing under test, per `../references/abstraction-levels.md`'s Testing by level section. Run it — confirm RED.
3. **Write the L3 function.** Technical mechanism only — no business decision beyond what the mechanism itself strictly requires (a retry/timeout policy is fine, a discount rule is not). Hide the SDK/HTTP/DB details behind the interface from step 1, per `../references/abstraction-levels.md`'s L3 rules and rule 6 in `../references/abstraction-levels/full-guidelines.md` (interfaces define contracts, not mechanisms). Name it per `../references/naming.md`.
4. **Green, then refactor.** Run the test from step 2 — confirm GREEN. Check for deep-module opportunities (`../references/deep-modules.md`: narrow the interface, hide more of the client/SDK), then re-run — still green.

Completion criterion: the L3 function exists behind a named interface, no business decision embedded in it, and its test went RED → GREEN for real against the real mechanism (or documented contract), shown, not asserted from memory.

Tell the human the function's file:line, its interface, its test file:line and what it actually hit (real DB/HTTP/vendor sandbox — name it), and the test result, when done.
