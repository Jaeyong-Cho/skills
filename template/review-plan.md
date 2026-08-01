# Plan: {Title}

**Type:** Review-Plan

## Action Sequence
- e.g. Write failing test `test_cache_hit_skips_db` in `tests/auth/test_cache.py`, asserting `AuthService.validate(token)` calls `TokenCache.get` before any DB call.
- e.g. Implement `TokenCache.get(token)` in `src/auth/cache.py` (Redis-backed, 5-minute TTL) so `test_cache_hit_skips_db` passes.
- e.g. Write failing test `test_validate_uses_cache_then_falls_back` in `tests/auth/test_service.py`, asserting `AuthService.validate(token)` returns the cached user when present, and calls `UserRepository.find(token)` otherwise.
- e.g. Implement `AuthService.validate(token)` in `src/auth/service.py`: call `TokenCache.get(token)` first, return its result on a hit, otherwise call `UserRepository.find(token)` and return that, so `test_validate_uses_cache_then_falls_back` passes.
- e.g. Write failing test `test_handler_rejects_unauthorized` in `tests/auth/test_handler.py`, asserting the request handler returns 401 when `AuthService.validate(token)` returns no user, and forwards to the route otherwise.
- e.g. Wire `AuthService.validate(token)` into the request handler in `src/auth/handler.py` (the client-facing entry point) so incoming requests are authorized before reaching the route, until `test_handler_rejects_unauthorized` passes.

## Review Sequence
Every implementation step above, reordered top-down along the flow (entry point -> algorithm/leaf) instead of build order, so a human reviewer can trace input -> output the way a reader would. Each entry names the step, its file and function/class location, and a concrete point to verify there.
- e.g. Step 6: Request handler wiring — `src/auth/handler.py`, function `handle_request` — the flow's entry point. Verify: unauthorized requests (no cached user, no DB match) get a 401 before reaching the route, and authorized ones are forwarded with the resolved user attached.
- e.g. Step 4: `AuthService.validate` — `src/auth/service.py`, method `AuthService.validate` — one level down. Verify: the cache is checked before the DB, the cache hit short-circuits the DB call, and the DB result is returned unchanged on a miss.
- e.g. Step 2: `TokenCache.get` — `src/auth/cache.py`, method `TokenCache.get` — the algorithm/leaf stage. Verify: the 5-minute TTL is applied, and a Redis connection error is treated as a cache miss rather than raised.

## Closeout
- [ ] Test
- [ ] Review — walk the Review Sequence above against the finished code, entry point to leaf, and confirm each verification point holds
