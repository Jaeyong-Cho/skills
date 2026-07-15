# Plan: {Title}

**ADR:** {path to `.context/adr/{timestamp}-{slug}.md`}

## Action Sequence
e.g.
1. Write failing test `test_cache_hit_skips_db` in `tests/auth/test_cache.py`, asserting `AuthService.validate(token)` calls `TokenCache.get` before any DB call.
2. Implement `TokenCache.get(token)` in `src/auth/cache.py` (Redis-backed, 5-minute TTL) and wire it into `AuthService.validate(token)` in `src/auth/service.py` so `test_cache_hit_skips_db` passes.
3. Write failing test `test_cache_fallback_on_redis_down` in `tests/auth/test_cache.py`, asserting `AuthService.validate(token)` still returns a result when Redis raises a connection error.
4. Implement the fallback in `TokenCache.get(token)` (`src/auth/cache.py`): catch the Redis connection error and return a cache-miss so `AuthService.validate(token)` falls through to the DB, until `test_cache_fallback_on_redis_down` passes.

## Closeout
- [ ] Refactor
- [ ] Test
