# Abstraction Levels (L1 / L2 / L3)

Every function or method sits at one of three levels. Code reads top-to-bottom as a description of the system when each function stays at one level and calls downward — never upward. "Downward" doesn't mean exactly one hop: `L1 → L1 → L2` (an orchestration composed of orchestrations) and `L1 → L3` (skipping L2 when there's genuinely no business rule to add) are both normal — see Dependency direction below.

This is the quick reference — table, dependency direction, agent questions, smells. For the full rule set with Good/Bad code examples (all 15 rules), read `abstraction-levels/full-guidelines.md`.

**Related docs, different scale of the same idea:** `meta-pattern.md`'s Abstractness axis (use cases / domain logic / infrastructure) is this same vertical split, but at the system/module-decomposition scale rather than per-function — read it when the question is "does this need a new module or service," not "what level is this function." `deep-modules.md` is how to shape the interface at an L1→L2 or L2→L3 boundary once it exists — small interface, hidden complexity, dependencies accepted not created.

| Level | Answers | Typical examples | DDD equivalent |
|-------|---------|-------------------|-----------------|
| **L1 — Intent** | What does this do, from the caller's view? | Public APIs, use cases, app services, orchestration methods | Application Service |
| **L2 — Domain** | What should happen per business rules? | Validation, calculation, policy, state transition | Entity / Domain Service |
| **L3 — Mechanism** | How is it technically done? | DB, HTTP, SDK, filesystem, serialization | Infrastructure / Gateway |

## Dependency direction

```
L1 (intent) → L2 (domain) → L3 (mechanism)
```

The rule is **never call upward** — L3 never calls L2 or L1, L2 never calls L1 — not "always exactly one hop down." Two shapes both satisfy it and are both normal:

- **Same-level composition** — an L1 function calling another L1 function (`L1 → L1 → L2`) is fine when the outer one is an orchestration of orchestrations; same for L2 calling L2.
- **Level skip** — an L1 function calling L3 directly (`L1 → L3`) is fine when there's genuinely no business rule between the intent and the mechanism, and the direct call still reads as intent. Skip only because there's truly nothing for L2 to add — not to avoid writing a domain rule that should exist (that's the Missing L2 smell below, a different thing).

L2 may depend on an L3 *interface* (e.g. `PaymentGateway`), never a concrete L3 implementation (`StripeClient`) — that keeps L2 swappable and testable without infrastructure. A dependency pointing the other way (L3 or L2 code deciding business outcomes) is a design error.

## Public/private is a different axis

Public vs. private answers "who can call this." L1/L2/L3 answers "what kind of concept is this." A public method can legitimately be L2 (`order.calculate_total()`, `order.can_cancel()`) — it's a real domain operation callers need, not system-level orchestration. Don't force every public method to L1, and don't assume every private method is L2/L3 — a private method that hides a meaningful domain rule (`_calculate_discount`) is still L2 in substance; hide *mechanics*, not *meaning*.

## Agent questions

- **One-sentence test** — can this function be explained in one clear sentence without "and"? If explaining it needs a list of unrelated steps, it mixes levels — split it.
- **Three-level test**, in order: Does it describe overall workflow → L1. Does it express a business rule/state transition → L2. Does it describe a technical mechanism → L3.
- **Decomposition check** (for a new or changed L1 flow): which L2 domain functions does this orchestration need — and for each, is there truly no business rule involved, in which case it calls L3 directly instead? Which L3 mechanism functions do those L2 functions (or the direct-L3 steps) need? Do they already exist, or must they be created? Naming this before writing the L1 function is what tells a real level-skip apart from the Missing L2 smell.

## Testing by level

- **L1** — no unit test of its own; it has nothing to unit-test beyond the calls it sequences. Covered by the integration test the checklists already require (per `deterministic-evaluation.md`), exercising L1 through to L3 for real.
- **L2** — TDD it (`tdd.md`, `tdd-tests.md`): RED → GREEN → REFACTOR, one test per business rule, through the function's public behavior. Don't mock the domain rule under test — mock only the L3 interface it depends on (per `deep-modules.md`'s "accept dependencies, don't create them").
- **L3** — TDD it too, but the test hits the real mechanism (a real test DB/HTTP call against a test instance) or the vendor's documented contract — not a mock of the thing the test is supposed to verify. L3 gets mocked *at* the L2/L3 interface by L2's tests, never inside its own.

## Smells

| Smell | What it looks like | Level |
|---|---|---|
| L1 leaking L3 | Orchestration method makes the HTTP/DB/SDK call itself instead of delegating | L1 |
| L2 leaking L3 | Business rule mixed with an HTTP/DB call in the same function | L2 |
| Missing L2 | L1 skips straight to L3 to avoid writing a business rule that actually exists (validation, calculation, policy) — a justified skip has no rule to write in the first place | L1→L3 |
| Mechanical extraction | Private function split out only because a block was long, not because it names a concept (see `deep-modules.md`) | any |
| Domain rule hidden as plumbing | A meaningful business rule buried in a `_helper`/`_process` name instead of a domain-revealing one | L2 |
| Shallow L1 | Orchestration re-implements domain logic inline instead of delegating to L2 | L1 |
| Technical name at L1/L2 | `execute_step()`, `handle_data()`, `process_request()` instead of `checkout()`, `calculate_discount()` (see `naming.md`) | L1/L2 |
