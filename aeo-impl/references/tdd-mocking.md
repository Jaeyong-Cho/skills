# Mocking Guidelines

## Mock at system boundaries only

Mock things that are external to the system — not things that are internal to it.

| Mock | Don't mock |
|---|---|
| HTTP clients, external APIs | Internal services in the same process |
| Database I/O in unit tests | Domain logic collaborators |
| Email/SMS senders | Entity methods |
| Clock / randomness | Method-layer workflows |

## Why

Mocking internal collaborators ties tests to implementation structure. When you restructure internals, tests break even though behavior is unchanged. This defeats the purpose of tests.

## When integration tests hit a real boundary

Prefer a test double at the outermost boundary (e.g. an in-memory database adapter, a fake HTTP server) rather than mocking individual internal calls.

```typescript
// Good — mock at the boundary
const fakeEmailer: Emailer = { send: jest.fn() }
await registerUser(email, password, fakeEmailer)
expect(fakeEmailer.send).toHaveBeenCalledWith(email, "welcome")

// Bad — mock an internal collaborator
jest.mock("./UserRepository")
jest.mock("./PasswordHasher")
```

## Rule

If removing the mock would require a network call or disk write, mock it.
If removing the mock would just run more of your own code, don't mock it.
