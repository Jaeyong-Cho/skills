---
name: l1-implement
description: Implement one L1 orchestration function directly from a plain-language description of a use case/flow, decomposed and built per references/abstraction-levels.md — reuses existing L2/L3 functions, creates new ones only when the description fully specifies them, stubs the rest as a visible TODO. Invoke as /l1-implement.
disable-model-invocation: true
---

# L1 Implement

Turn a human's plain-language description of one use case into a real, working L1 function — no plan file, no round-based interview. The lighter path for a single flow that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

Before starting: if the description covers more than one L1 flow, or reads like a whole feature (new schema, new service, cross-system contract, ambiguous acceptance criteria), **MUST STOP** and recommend `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` instead — name why in one line. A single, clear use case skips this and goes straight to step 1.

1. **Name the L1 function.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) — if it can't be said in one sentence without "and", it's more than one L1 flow; go back to the scope check.
2. **Decompose.** Run the Decomposition check from `../references/abstraction-levels.md`: list the L2 domain functions and L3 mechanism functions this L1 function needs. Dispatch a sub-agent to check the repo for each — reuse before creating, per `../references/deep-modules.md`; never re-implement what already exists a few files over.
3. **Fill gaps only where the description is complete.** For each L2/L3 function from step 2 that doesn't exist yet: if the description fully specifies its behavior (inputs, outputs, and the business rule or mechanism), implement it for real, at its correct level, following `../references/abstraction-levels.md`'s per-level rules. If the description leaves it underspecified, **MUST NOT** guess the business logic — write a stub that fails loudly (raise/throw "not implemented: {decision}") and list it plainly to the human as a follow-up; never silently fabricate behavior.
4. **Write the L1 function.** Orchestration only — calls the L2/L3 functions from steps 2-3 in sequence, no direct database/HTTP/SDK/filesystem call inline, per `../references/abstraction-levels.md`'s L1 rules. Name it and its parts per `../references/naming.md`.
5. **Test it.** One integration test exercising the L1 function end to end, per `../references/deterministic-evaluation.md` — the real function, not a mock of the thing under test. Run it: green, or the specific stub from step 3 raising visibly in the test output — either way, shown for real, not asserted from memory.

Completion criterion: the L1 function exists and calls only named L2/L3 functions, no inline mechanism; every gap from step 2 is either implemented for real or an explicit loud stub naming the missing decision; the integration test ran and its actual result is in hand.

Tell the human the function's file:line, which L2/L3 functions were reused vs. newly created vs. stubbed, and the test result, when done.
