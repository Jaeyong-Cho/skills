---
name: api-impl
description: Implement existing API specs faithfully — no new API design. Reads user-provided API docs (public method signatures, CLI interface, UI, algorithms, testing strategy, dependencies on other APIs) and implements each entry point one at a time. Use when user has a designed API spec and wants it filled in, mentions "implement this API", "implement from docs", "implement existing API", "implement based on spec", "api-impl", or hands over method signatures to fill in.
---

# API Impl (From Docs)

Design is already done. Your job: implement it faithfully.

Read [deep-modules](../pf/references/deep-modules.md), [layers](../pf/references/layers.md), [tdd](../pf/references/tdd.md), [tdd-tests](../pf/references/tdd-tests.md), [tdd-mocking](../pf/references/tdd-mocking.md), and [tdd-refactoring](../pf/references/tdd-refactoring.md) before starting.

**Layer dependency rule**: outer layers reference inner; inner layers never reference outer (`Value → Aspect → Object`). If any wired dependency violates this, stop and surface the conflict before continuing.

## Step 1: Read the api docs

User provides one or more API names to implement. For each, determine its layer and read `src/api/<layer>s/<name>.md` (e.g. `src/api/objects/user.md`, `src/api/aspects/auth.md`, `src/api/values/signup.md`).

## Step 2: Implement — one entry point at a time

For each public method / CLI command / UI handler:

1. **Match the signature exactly** — name, params, return type, errors
2. **Follow the algorithm** — implement the described logic; don't invent
3. **Wire dependencies correctly** — call other APIs as specified; accept them as injected params (don't create inside) per [deep-modules](../pf/references/deep-modules.md) testable interface rules
4. **Run and verify** — execute, confirm behavior matches spec description

Do not move to the next entry point until current one works.

## Step 3: Testability check

Per [deep-modules](../pf/references/deep-modules.md):

- [ ] Dependencies injected, not instantiated internally?
- [ ] Returns results instead of implicit side effects where spec allows?
- [ ] Interface surface matches spec exactly — not wider, not narrower?
- [ ] Ambiguous spec points surfaced to user before guessing?

## Step 4: Done

List implemented entry points vs spec. Flag any deviations with reason.

## Rules

- **No new public API.** Public methods are the API — match the spec exactly, no additions.
- Private methods are fine — create as many helpers as needed to implement the logic cleanly.
- Match public signatures exactly — name, params, return type.
- If spec is ambiguous, ask before guessing.
- If spec conflicts with testability principles, surface the conflict; don't silently deviate.
