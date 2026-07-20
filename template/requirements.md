# SPEC - {title}

> Target: ≤20 words per sentence; total prose (excluding diagrams/tables) under ~450 words — a 5-minute read. If a draft runs over, flag it to the user and continue; don't block on it.

## Context
> The problem or trigger, and the current state before this spec — why this work exists at all.
> Stage-to-stage content (current state → trigger → desired state) → ASCII flow diagram, plain characters only (`|`, `v`, `+--`, `->`; see `../references/document-style.md`).

```
e.g.
Current State
  Auth tokens validated on every request by hitting the DB
    |
    v
Trigger
  Throughput capped at 200 req/s during peak traffic
    |
    v
Desired State
  1000 req/s sustained
```

## Requirements
> - What must be true.
> - One requirement per line, testable — avoid vague verbs like "support" or "handle" without a condition attached.

- e.g. Validated tokens must be served from cache for repeat requests within a 5-minute window.
- e.g. A cache outage must not block requests — fall back to DB validation.

## Decision
> - The choice made among alternatives, and why.
> - Not the requirement itself — the resolution when a requirement was ambiguous or had multiple valid implementations.
> - Comparison content (alternatives weighed against each other) → Markdown table.

|Option|Chosen|Why|
|--|--|--|
|e.g. Redis cache|Yes|Multiple app instances share validation state; each holds session tokens|
|e.g. In-process cache|No|Would miss on every other request behind the load balancer|

## Out of Scope
> - What was explicitly excluded, so it isn't silently re-litigated later.

- e.g. Token revocation is out of scope — a revoked token stays valid in cache for up to 5 minutes; the security team has accepted this window.

# User Scenario
> - One scenario per subsection — split into multiple when a single sequence grows too large to follow, or covers more than one path or actor.
> - Narrate each as the sequence the user lives through: {action} → {reaction} → {action} → ... down to the outcome — not a feature list.
> - An ASCII flow diagram (plain characters only — `|`, `v`, `+--`, `->`; see `../references/document-style.md`) is welcome alongside the narration wherever the scenario branches or a picture reads faster than the arrow chain.

## {Scenario name}
- e.g. Repeat request within window → cache hit, no DB round-trip → response returns in <20ms
```
Request arrives
    |
    v
Token cached?
    |
    +-- yes -> Serve from cache, <20ms
    |
    +-- no  -> Validate against DB -> Cache result, 5-min TTL -> Serve from cache, <20ms
```

# Acceptance Criteria
> - SMART AC — Specific, Measurable, Achievable, Relevant, Time-bound.
> - Each row is one verifiable condition, phrased as Given–When–Then.

|AC|Category|Verification Method|
|--|--|--|
|Given {starting state} - When {action} - Then {expected result}|Normal, Exception or Boundary|{how this gets checked — manual test, e2e test, unit test, test name, or query}|
|e.g. Given a warmed cache - When 1000 req/s sustained for 60s - Then p99 latency < 20ms|Normal|e2e test: `auth-flow` scenario|
|e.g. Given Redis is down - When a request arrives - Then it falls back to DB validation and still succeeds|Exception|unit test: `test_cache_fallback`|
