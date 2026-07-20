# ADR: {Title}

**Date:** {YYYY-MM-DD}

> Target: ≤20 words per sentence; total prose (excluding diagrams/tables) under ~450 words — a 5-minute read. If a draft runs over, flag it to the user and continue; don't block on it.

## Context
> What is the problem, What is the current state, What should be changed
> Stage-to-stage content (current state → problem → change) → ASCII flow diagram, plain characters only (`|`, `v`, `+--`, `->`; see `../references/document-style.md`).

```
e.g.
Current State
  Auth tokens validated on every request by hitting the DB
    |
    v
Problem
  Throughput capped at 200 req/s
    |
    v
Change
  Move validation to a cache
```

## Decision
> - Concrete design — which API(s) are affected or introduced, which source file(s) hold the change, and how the source structure is organized (modules, layers, directories).
> - Comparison content (before vs. after) → Markdown table for the facts, ASCII flow diagram (plain characters only — `|`, `v`, `+--`, `->`; see `../references/document-style.md`) for the call-path shape.
> - The full Static/Dynamic View lives in the paired `architecture.md`, not here.

|Aspect|Before|After|
|--|--|--|
|e.g. API|`AuthService.validate(token)`|`AuthService.validate(token)` (unchanged signature)|
|e.g. Files|`src/auth/service.py`|`src/auth/service.py`, `src/auth/cache.py` (new)|
|e.g. Behavior|Hits DB directly on every call|Checks `TokenCache.get(token)` first (5-min TTL), falls back to DB on miss|

```
e.g.
Before:  AuthService -> DB
After:   AuthService -> TokenCache -> Redis
                      -> DB  -- cache miss ->
```

## Observability
> - Runtime checkpoints — internal state, logs, or intermediate data to observe mid-execution, with the final output.
> - Each checkpoint is a parallel (where, what) pair → Markdown table.

|Checkpoint|What to Observe|
|--|--|
|e.g. Cache lookup|`cache_hit`/`cache_miss` counter per request|
|e.g. Final response|Throughput result (req/s)|

## Test-Loop Design
> - Check if an existing test-loop scenario already covers this; extend it rather than creating a new one.
> - E2E only — what `run` resets/initializes, what it writes, what `verify` checks per scenario.
> - One row per scenario, each with parallel attributes → Markdown table.

|Scenario|Reset/Init|Verify|
|--|--|--|
|e.g. `auth-flow` (extended)|Clear Redis, replay 100 recorded requests|Assert cache hit rate > 90% after warmup|

## Verification Criteria
> - How a human confirms the result is good, checkable, mapped to the requirements spec's Normal / Exception / Boundary categories.
> - Same shape as the requirements spec's Acceptance Criteria table.

|Criterion (Given–When–Then)|Category|
|--|--|
|e.g. Given a warmed cache - When 1000 req/s sustained for 60s - Then p99 latency < 20ms|Normal|
