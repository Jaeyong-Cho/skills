# Architecture: {Title}

**ADR:** {path to `.context/adr/{slug}.md`}

## Static View
> - Directory structure, classes — each with purpose and description — and their dependency relationships, placed per archi.md's layers (Objects/Logics/Usecase/External).
> - Dependencies as an ASCII flow diagram (plain characters only — `|`, `v`, `+--`, `->`; see `../references/document-style.md`); an arrow pointing from an inner layer to an outer one is a design error.

**Directory structure**
```
e.g.
src/auth/
  service.py   # AuthService (Usecase)
  cache.py     # TokenCache (Logics)
```

**Classes**
|Class|Layer|Purpose|
|--|--|--|
|e.g. `AuthService`|Usecase|Orchestrates token validation: cache first, DB fallback|
|e.g. `TokenCache`|Logics|Reads/writes validated tokens in Redis with a 5-minute TTL|

**Dependencies**
```
AuthService (Usecase) -> TokenCache (Logics) -> Redis
AuthService (Usecase) -> DB
```

## Dynamic View
> - One ASCII call-flow diagram per scenario in the requirements spec's User Scenario section — name the subsection to match. Plain characters only (`|`, `v`, `+--`, `->`); branch legs get a short inline label (e.g. `-- cache hit ->`), see `../references/document-style.md`.

### {Scenario name}
```
e.g.
Client
  |
  v
AuthService.validate(token)
  |
  v
TokenCache.get(token)
  |
  +-- cache hit  -> return cached result -> AuthService -> Client
  |
  +-- cache miss -> DB.validate(token) -> TokenCache.set(token, result) -> AuthService -> Client
```
