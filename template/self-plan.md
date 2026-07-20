# Plan: {Title}

**Type:** Self-Plan
**ADR:** {path to `.context/adr/{timestamp}-{slug}.md`}

## Action Sequence
- e.g. Write failing test `test_cache_hit_skips_db` in `tests/auth/test_cache.py`, asserting `AuthService.validate(token)` calls `TokenCache.get` before any DB call.
- e.g. Implement `TokenCache.get(token)` in `src/auth/cache.py` (Redis-backed, 5-minute TTL), so `test_cache_hit_skips_db` passes.
  - **Working:** Entire function — Redis client setup, TTL, connection error handling. This is a leaf stage's own algorithm, not a call to another flow stage, so it has no hole.
- e.g. Wire `TokenCache.get(token)` into `AuthService.validate(token)` in `src/auth/service.py` so it checks the cache before falling back to the DB.
  - **Working:** The DB-lookup branch itself (`UserRepository.find(token)` and its query).
  - **Hole:** The line(s) in `validate` where it calls `TokenCache.get(token)` and decides, from the result, whether to call the DB. TODO (per `todo-hole.md`):
    ```python
    # TODO:
    # 1. Call TokenCache.get(token).
    # 2. If it returns a cached user, return that.
    # 3. Otherwise call UserRepository.find(token) and return that.
    # e.g. token="user-42-session" -> get() returns None (miss)
    #      -> UserRepository.find("user-42-session") -> the user record
    cached = TokenCache.get(/* */)
    if cached:
        return /* */
    return /* */
    ```
- e.g. Wire `AuthService.validate(token)` into the request handler in `src/auth/handler.py` (the client-facing entry point) so incoming requests are authorized before reaching the route.
  - **Working:** Response formatting and the 401 branch.
  - **Hole:** The line(s) where the handler calls `AuthService.validate(token)` and gates the route on its result. TODO (per `todo-hole.md`): ...

## Recommended Human Work Order
Every holed step above, reordered top-down along the flow (entry point → algorithm) instead of build order. Steps with no hole (e.g. Step 2, `TokenCache.get`) are omitted — they're already complete.
- e.g. Step 4: Wire `AuthService.validate` into the request handler — `src/auth/handler.py`, function `handle_request` — the flow's entry point; start here to see the whole flow before descending into it.
- e.g. Step 3: Wire `TokenCache.get` into `AuthService.validate` — `src/auth/service.py`, method `AuthService.validate` — one level down; the flow's next stage.

## Closeout
- [ ] Review + Test — once every hole above is filled in, re-run `/auto-action` on this plan; it detects the holes are gone and reviews each one against its recorded intent, then runs the tests
