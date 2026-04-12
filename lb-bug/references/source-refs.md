# Source Code References

## Convention

Reference source code inline in prose using this format:

```markdown
The authentication flow begins in `src/services/UserService.ts :: UserService.authenticate`,
which validates the JWT token before delegating to the session store.
```

For a linked reference:

```markdown
See [`UserService.authenticate`](../../src/services/UserService.ts) — handles token validation.
```

- Paths are **relative from the `.md` file's location** to the repo root
- Format: `path/to/file :: ClassName.methodName`
- For module-level functions: `path/to/file :: functionName`

## Before Adding Any Reference

Always verify the symbol exists:

```bash
grep -n "methodName\|ClassName" path/to/file
```

If the symbol does not exist yet:
- Write it as `[not yet implemented]` in prose
- Place an `IMPLEMENT` flag nearby describing what needs to be created

## Not Yet Implemented

```markdown
Token refresh is handled by `src/services/AuthService.ts :: AuthService.refreshToken` [not yet implemented].

<!-- IMPLEMENT: AuthService.refreshToken(token: string): Promise<string> — validate token is within 1h of expiry, issue new JWT with reset expiry -->
```
