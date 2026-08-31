# Mocking Guidelines

## Mock at system boundaries only

Mock things external to system — not internal.

| Mock | Don't mock |
|---|---|
| HTTP clients, external APIs | Internal services in same process |
| Database I/O in unit tests | Domain logic collaborators |
| Email/SMS senders | Entity methods |
| Clock / randomness | Method-layer workflows |

For which boundary each abstraction level mocks at — L2 mocks the L3 interface it depends on, L3 never mocks itself — read `abstraction-levels.md`'s Testing by level section.

## Why

Mocking internal collaborators ties tests to implementation structure. When you restructure internals, tests break even though behavior is unchanged. Defeats purpose of tests.

## When integration tests hit a real boundary

Prefer test double at outermost boundary (e.g. in-memory database adapter, fake HTTP server) rather than mocking individual internal calls.

```typescript
// Good — mock at the boundary
const fakeEmailer: Emailer = { send: jest.fn() }
await registerUser(email, password, fakeEmailer)
expect(fakeEmailer.send).toHaveBeenCalledWith(email, "welcome")

// Bad — mock an internal collaborator
jest.mock("./UserRepository")
jest.mock("./PasswordHasher")
```

## Designing for mockability

At a boundary, shape the interface so mocking it is cheap — accept dependencies, don't create them internally (see `deep-modules.md`'s Interface Design for Testability).

Prefer one function per external operation over a generic fetcher — each mock returns one specific shape instead of needing conditional logic keyed on an endpoint argument:

```typescript
// Good — each call is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
}

// Bad — mocking needs conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
}
```

## Rule

If removing mock would require network call or disk write, mock it.
If removing mock would just run more of your own code, don't mock it.
