---
name: l1-implement
description: Implement one L1 orchestration function directly from a plain-language description of a use case/flow, decomposed per references/abstraction-levels.md — reuses existing L2/L3 functions, stubs every missing one as a visible TODO (never builds them here; that's a separate l2-implement/l3-implement call). Invoke as /l1-implement, or via to-code.
disable-model-invocation: true
---

# L1 Implement

Turn a human's plain-language description of one use case into a real, working L1 function — no plan file, no round-based interview. The lighter path for a single flow that `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` would be overkill for.

## Scope check

1. **Name the L1 function.** From the description, state its one-sentence test (per `../references/abstraction-levels.md`) — if it can't be said in one sentence without "and", it's more than one L1 flow; go back to the scope check.
2. **Decompose.** Run the Decomposition check from `../references/abstraction-levels.md`: list the L2 domain functions and L3 mechanism functions this L1 function needs. Dispatch a sub-agent to check the repo for each — reuse before creating, per `../references/deep-modules.md`; never re-implement what already exists a few files over.
3. **Stub every gap — never implement one here.** For each L2/L3 function from step 2 that doesn't exist yet: write only a stub — right name and signature, a `# TODO: implement via @skills/l2-implement` or `# TODO: implement via @skills/l3-implement` comment (whichever level it is) naming the missing decision/mechanism, and a body that fails loudly (raise/throw "not implemented: {decision}"). This applies regardless of how completely the description specifies the behavior — **MUST NOT** write real L2/L3 logic in this skill, even when the description fully specifies it; building a stubbed function for real is a separate, later call to that level's own `-implement` skill.
4. **Write the L1 function.** Orchestration only — calls the L2/L3 functions from steps 2-3 in sequence, no direct database/HTTP/SDK/filesystem call inline, per `../references/abstraction-levels.md`'s L1 rules. Name it and its parts per `../references/naming.md`.

This skill only writes code — no test. Run `@skills/func-test` on the finished function separately when it needs coverage; this is a deliberate deviation from `../references/tdd.md`'s RED-first default, scoped to this lightweight path.

Completion criterion: the L1 function exists and calls only named L2/L3 functions, no inline mechanism; every gap from step 2 is an explicit loud TODO stub naming the missing decision and which skill builds it for real.

Tell the human the function's file:line, which L2/L3 functions were reused vs. stubbed (and which skill each stub needs), and that `@skills/func-test` is the next step for coverage.
