---
name: func-test
description: Write and run a real test for one existing function, choosing the test shape (L1 integration / L2 domain-rule / L3 real-mechanism) per references/abstraction-levels.md's Testing by level section. The decoupled test step for l1-implement/l2-implement/l3-implement, which write code only. Invoke as /func-test.
disable-model-invocation: true
---

# Func Test

Turn a human's pointer to one existing function into a real test for it — no plan file, no round-based interview. Standalone from `@skills/l1-implement`/`@skills/l2-implement`/`@skills/l3-implement`, which write code only; run this separately whenever a function needs coverage.

## Scope check

Before starting: if the human names more than one function, or a whole flow/feature spanning several files, **MUST STOP** and recommend `@skills/dev-grill-me` → `@skills/to-plan` → `@skills/do-plan` instead (or `@skills/refact-grill-me` for a refactor's behavior-preservation baseline) — name why in one line. A single, existing function skips this and goes straight to step 1.

1. **Classify the function's level.** Read it against the Three-level test in `../references/abstraction-levels.md` — L1 (orchestration), L2 (domain rule), or L3 (mechanism). This decides the test shape in step 3.
2. **Find its dependencies and existing conventions.** Dispatch a sub-agent to check the repo: what test framework/fixtures/naming does this module already use — reuse that convention, per `../references/deep-modules.md`'s "reuse before creating." For an L2 function, name the L3 interface(s) it depends on (the only thing allowed to be mocked). For an L1 function, note whether any callee is still a loud TODO stub (per `l1-implement`) — that's an expected fail path, not a bug.
3. **Write the test**, per `../references/abstraction-levels.md`'s Testing by level section and `../references/tdd-tests.md`/`../references/tdd-mocking.md`:
   - **L1** — one integration test exercising the function end to end through real L2/L3 calls (a callee still stubbed as TODO is asserted to raise, not faked green).
   - **L2** — one test per business rule through the function's public behavior; mock only the L3 interface it depends on, never the rule itself.
   - **L3** — a test against the real mechanism (real test DB/HTTP call against a test instance, or the vendor's documented contract) — never a mock of the thing under test.
4. **Run it and report the real result.** Pass or fail, from the actual run — never asserted from memory.

Completion criterion: one test exists for the named function, at the shape its level requires, and its actual pass/fail result is in hand.

Tell the human the function's file:line, the test's file:line, which level's test shape was used, and the real result.
