# Abstraction Levels (L1 / L2 / L3)

Every function or method sits at one of three levels. Code reads top-to-bottom as a description of the system when each function stays at one level and calls downward into the next.

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

L1 calls L2. L2 may depend on an L3 *interface* (e.g. `PaymentGateway`), never a concrete L3 implementation (`StripeClient`) — that keeps L2 swappable and testable without infrastructure. A dependency pointing the other way (L3 or L2 code deciding business outcomes, or L1 making an HTTP/DB call directly) is a design error.

## Public/private is a different axis

Public vs. private answers "who can call this." L1/L2/L3 answers "what kind of concept is this." A public method can legitimately be L2 (`order.calculate_total()`, `order.can_cancel()`) — it's a real domain operation callers need, not system-level orchestration. Don't force every public method to L1, and don't assume every private method is L2/L3 — a private method that hides a meaningful domain rule (`_calculate_discount`) is still L2 in substance; hide *mechanics*, not *meaning*.

## Agent questions

- **One-sentence test** — can this function be explained in one clear sentence without "and"? If explaining it needs a list of unrelated steps, it mixes levels — split it.
- **Three-level test**, in order: Does it describe overall workflow → L1. Does it express a business rule/state transition → L2. Does it describe a technical mechanism → L3.
- **Decomposition check** (for a new or changed L1 flow): which L2 domain functions does this orchestration need, and which L3 mechanism functions do those L2 functions need? Do they already exist, or must they be created? Naming this before writing the L1 function is what keeps it from collapsing into L1+L3 with no L2 in between.

## Testing by level

- **L1** — no unit test of its own; it has nothing to unit-test beyond the calls it sequences. Covered by the integration test the checklists already require (per `deterministic-evaluation.md`), exercising L1 through to L3 for real.
- **L2** — TDD it (`tdd.md`, `tdd-tests.md`): RED → GREEN → REFACTOR, one test per business rule, through the function's public behavior. Don't mock the domain rule under test — mock only the L3 interface it depends on (per `deep-modules.md`'s "accept dependencies, don't create them").
- **L3** — TDD it too, but the test hits the real mechanism (a real test DB/HTTP call against a test instance) or the vendor's documented contract — not a mock of the thing the test is supposed to verify. L3 gets mocked *at* the L2/L3 interface by L2's tests, never inside its own.

## Smells

| Smell | What it looks like | Level |
|---|---|---|
| L1 leaking L3 | Orchestration method makes the HTTP/DB/SDK call itself instead of delegating | L1 |
| L2 leaking L3 | Business rule mixed with an HTTP/DB call in the same function | L2 |
| Missing L2 | L1 calls an L3 mechanism directly with no domain function between them | L1→L3 |
| Mechanical extraction | Private function split out only because a block was long, not because it names a concept (see `deep-modules.md`) | any |
| Domain rule hidden as plumbing | A meaningful business rule buried in a `_helper`/`_process` name instead of a domain-revealing one | L2 |
| Shallow L1 | Orchestration re-implements domain logic inline instead of delegating to L2 | L1 |
| Technical name at L1/L2 | `execute_step()`, `handle_data()`, `process_request()` instead of `checkout()`, `calculate_discount()` (see `naming.md`) | L1/L2 |
