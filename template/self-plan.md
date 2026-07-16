# Plan: {Title}

**Type:** Self-Plan
**ADR:** {path to `.context/adr/{timestamp}-{slug}.md`}

## Action Sequence
- e.g. Write failing test `test_cache_hit_skips_db` in `tests/auth/test_cache.py`, asserting `AuthService.validate(token)` calls `TokenCache.get` before any DB call.
- e.g. Implement `TokenCache.get(token)` in `src/auth/cache.py` (Redis-backed, 5-minute TTL) and wire it into `AuthService.validate(token)` in `src/auth/service.py` so `test_cache_hit_skips_db` passes.
  - **Working:** Redis client setup, connection error handling, TTL constant.
  - **Hole:** The lookup-then-fallback sequence in `AuthService.validate`. TODO (per `todo-hole.md`): `# TODO: Turn `token` (e.g. "user-42-session") into the value this method returns (e.g. a validated user record).`
- e.g. Write failing test `test_cache_fallback_on_redis_down` in `tests/auth/test_cache.py`, asserting `AuthService.validate(token)` still returns a result when Redis raises a connection error.
- e.g. Implement the fallback in `TokenCache.get(token)` (`src/auth/cache.py`): catch the Redis connection error and return a cache-miss so `AuthService.validate(token)` falls through to the DB, until `test_cache_fallback_on_redis_down` passes.
  - **Working:** The `except RedisConnectionError` catch block and its structure.
  - **Hole:** What `get(token)` returns on that path. TODO (per `todo-hole.md`): `# TODO: Turn a Redis connection failure (e.g. ConnectionRefusedError) into the value get(token) returns (e.g. a cache-miss sentinel).`

## Closeout
- [ ] Refactor
- [ ] Test
