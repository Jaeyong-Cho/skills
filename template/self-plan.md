# Plan: {Title}

**Type:** Self-Plan
**ADR:** {path to `.context/adr/{timestamp}-{slug}.md`}

## Action Sequence
- e.g. Write failing test `test_cache_hit_skips_db` in `tests/auth/test_cache.py`, asserting `AuthService.validate(token)` calls `TokenCache.get` before any DB call.
- e.g. Implement `TokenCache.get(token)` in `src/auth/cache.py` (Redis-backed, 5-minute TTL), so `test_cache_hit_skips_db` passes.
  - **Working:** Entire function — Redis client setup, TTL, connection error handling. This is a leaf stage's own algorithm, not a call to another flow stage, so it has no hole.
- e.g. Wire `TokenCache.get(token)` into `AuthService.validate(token)` in `src/auth/service.py` so it checks the cache before falling back to the DB.
  - **Working:** The DB-lookup branch itself (`UserRepository.find(token)` and its query).
  - **Hole:** The line(s) in `validate` where it calls `TokenCache.get(token)` and decides, from the result, whether to call the DB. TODO (per `todo-hole.md`): `# TODO: Turn `token` (e.g. "user-42-session") into the value this method returns (e.g. a validated user record) — using TokenCache.get and, on a miss, UserRepository.find.`

## Closeout
- [ ] Refactor
- [ ] Test
