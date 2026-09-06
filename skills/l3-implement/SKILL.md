---
name: l3-implement
description: Implement one L3 mechanism function directly from a plain-language description of a technical operation (DB, HTTP, SDK, filesystem, ...), per references/abstraction-levels.md — exposes a simple interface upward, no business decisions inside. Code only, no test. Invoke as /l3-implement.
disable-model-invocation: true
---

# L3 Implement

Turn a human's plain-language description of one technical operation into a real L3 function — no plan file, no round-based interview. The lighter path for a single mechanism that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

1. **Name the L3 function and its interface.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) in mechanism terms (the technical thing it does), and name the interface/contract it implements for L2 to depend on. Dispatch a sub-agent to check the repo for an existing one first — reuse before creating, per `../references/deep-modules.md`; create the interface only if none exists and the description makes clear what L2 needs from it.
2. **Place and write the L3 function.** Dispatch a sub-agent to find where sibling L3 mechanisms for this technical capability (or the interface itself) already live in the repo (module/folder convention) — put it there; open a new file only when no existing one fits. Technical mechanism only — no business decision beyond what the mechanism itself strictly requires (a retry/timeout policy is fine, a discount rule is not). Hide the SDK/HTTP/DB details behind the interface from step 1, per `../references/abstraction-levels.md`'s L3 rules and rule 6 (interfaces define contracts, not mechanisms). Name it per `../references/naming.md`. No `L1`/`L2`/`L3` or skill-name jargon in code comments/docstrings — that's this project's internal shorthand, not for the codebase.
3. **Check for deep-module opportunities** (`../references/deep-modules.md`: narrow the interface, hide more of the client/SDK).
4. **Review the diff for layer mixing.** Read back the actual function you just wrote against `../references/abstraction-levels.md`'s smells table — no business decision embedded (a discount rule, a validation policy, anything beyond retry/timeout/serialization). Found one → push it up to an L2 caller instead of deciding it here.

This skill only writes code — no test. Add and run a real test for the finished function separately when it needs coverage; this is a deliberate deviation from `../references/tdd.md`'s RED-first default, scoped to this lightweight path.

Completion criterion: the L3 function exists behind a named interface, no business decision embedded in it, and step 4's layer-mixing review found nothing left inline.

Tell the human the function's file:line, its interface, that the layer-mixing review passed clean, and that a real test is the next step for coverage (against the real mechanism, not a mock).
