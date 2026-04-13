# Document Structure

The V-Doc book lives in `book/` and follows the standard mdbook layout with mermaid support.

---

## Directory Layout

Each item is a **separate file**. Each document type has its own directory containing one file per item plus an `index.md` for the traceability summary.

```
book/
  book.toml
  mermaid.min.js
  mermaid-init.js
  src/
    SUMMARY.md
    tags.md                    ← tag registry (single source of truth)
    curs/
      index.md                 ← CuRS traceability summary
      CuRS-001.md
      CuRS-002.md
      ...
    srs/
      index.md                 ← SRS traceability summary
      SRS-001.md
      SRS-002.md
      ...
    sad/
      index.md                 ← SAD traceability summary
      SAD-001.md               ← always the directory structure item
      SAD-002.md
      ...
    sdd/
      index.md                 ← SDD traceability summary
      SDD-001.md
      SDD-002.md
      ...
    at/
      index.md                 ← AT traceability summary
      AT-001.md
      AT-002.md
      ...
    sit/
      index.md                 ← SIT traceability summary
      SIT-001.md
      ...
    ut/
      index.md                 ← UT traceability summary
      UT-001.md
      ...

src/
  (human-written source code)
tests/
  at/                          ← acceptance test stubs
  sit/                         ← integration test stubs
  ut/                          ← unit test stubs
```

---

## SUMMARY.md Structure

Every new item file must be added to `SUMMARY.md`. The structure is nested under each document type:

```markdown
# Summary

- [Tags](./tags.md)
- [Customer Requirements](./curs/index.md)
  - [CuRS-001: <title>](./curs/CuRS-001.md)
  - [CuRS-002: <title>](./curs/CuRS-002.md)
- [Software Requirements](./srs/index.md)
  - [SRS-001: <title>](./srs/SRS-001.md)
  - [SRS-002: <title>](./srs/SRS-002.md)
- [Architectural Design](./sad/index.md)
  - [SAD-001: Project directory structure](./sad/SAD-001.md)
  - [SAD-002: <title>](./sad/SAD-002.md)
- [Detailed Design](./sdd/index.md)
  - [SDD-001: <title>](./sdd/SDD-001.md)
- [Acceptance Tests](./at/index.md)
  - [AT-001: <title>](./at/AT-001.md)
- [Integration Tests](./sit/index.md)
  - [SIT-001: <title>](./sit/SIT-001.md)
- [Unit Tests](./ut/index.md)
  - [UT-001: <title>](./ut/UT-001.md)
```

---

## tags.md Structure

```markdown
# Tag Registry

All tags used across V-Doc items. Consult this before creating new tags. Add new tags here before using them in items.

| Tag | Description | Item Count |
|-----|-------------|------------|
| `#auth` | Authentication and authorization concerns | 7 |
| `#api` | External API surface | 4 |
| `#performance` | Performance constraints and optimizations | 2 |
| `#security` | Security requirements and controls | 5 |
| `#data` | Data models, storage, persistence | 6 |
| `#error` | Error handling and failure modes | 3 |
```

Item Count is updated by AI each time it adds or removes items with that tag.

---

## Item File Format

Each item is a standalone markdown file. The filename is the item ID in uppercase: `SRS-001.md`, `SAD-003.md`.

The file uses a **level-1 heading** (since it is its own page in the book) with **level-2 headings** for each field:

```markdown
# SRS-007: User authentication via email and password

## State
`draft`

## Tags
`#auth` `#security` `#user`

## Why
Users need a secure way to identify themselves to access protected features; this is the primary authentication method chosen from CuRS-002.

## Traces
- ← [CuRS-002](../curs/CuRS-002.md): The customer explicitly requested email/password login as the primary entry point, making this a mandatory requirement
- → [SAD-003](../sad/SAD-003.md): This requirement is fulfilled by the AuthService component, which owns credential validation and session creation
- → [AT-005](../at/AT-005.md): Acceptance test verifies the full login flow from the user's perspective, including the lockout scenario

## Description
Users shall be able to authenticate using a valid email address and password.
The system shall reject invalid credentials with an appropriate error message.
The system shall lock the account after 5 consecutive failed attempts.

> **Review needed** — verify lockout threshold (5 attempts) and whether unlock is automatic (time-based) or manual (admin action)
```

**Rules**:
- Use `# H1` for the item title, `## H2` for fields — each file is its own page
- Filename must exactly match the ID: `SRS-007.md` for `SRS-007`
- No `---` separators needed — the page boundary is the file boundary

---

## Mermaid Diagrams

The book has mermaid support. **Use mermaid diagrams aggressively** wherever they add clarity. A diagram is almost always clearer than prose for structure and flow.

### When to add diagrams

| Item type | Diagram type | When to add |
|-----------|-------------|-------------|
| SAD | `graph LR` component diagram | Always — show the component and its dependencies |
| SAD-001 | `graph TD` directory tree | Always — visualize the folder structure |
| SDD | `flowchart TD` algorithm | When the algorithm has branches or loops |
| SIT | `sequenceDiagram` | Always — show the interaction sequence between components |
| SRS | `flowchart LR` | When the requirement involves a multi-step user flow |

### Diagram placement

Add a `## Diagram` section after `## Traces` and before the item body:

```markdown
## Diagram

\`\`\`mermaid
graph LR
  Client --> AuthService
  AuthService --> UserRepository
  AuthService --> SessionStore
\`\`\`
```

### Mermaid examples by type

**SAD component diagram** (`graph LR`):
```
graph LR
  Client["Client (API router)"] --> AS["AuthService\nsrc/auth/AuthService.ts"]
  AS --> UR["UserRepository\nsrc/user/UserRepository.ts"]
  AS --> SS["SessionStore\nsrc/auth/SessionStore.ts"]
```

**SIT sequence diagram** (`sequenceDiagram`):
```
sequenceDiagram
  participant Router
  participant AuthService
  participant UserRepository
  Router->>AuthService: authenticate(email, password)
  AuthService->>UserRepository: findByEmail(email)
  UserRepository-->>AuthService: User | null
  AuthService-->>Router: Session | AuthError
```

**SDD algorithm flowchart** (`flowchart TD`):
```
flowchart TD
  A[Look up user by email] --> B{Found?}
  B -- No --> C[Return INVALID_CREDENTIALS]
  B -- Yes --> D{Locked?}
  D -- Yes --> E[Return ACCOUNT_LOCKED]
  D -- No --> F{Password match?}
  F -- No --> G[Increment failure counter\nReturn INVALID_CREDENTIALS]
  F -- Yes --> H[Reset counter\nCreate session\nReturn Session]
```

---

## Index File Format

Each document type directory has an `index.md` that serves as the overview and traceability summary. It links to all item files using relative paths.

```markdown
# Software Requirements Specification (SRS)

Formal requirements derived from CuRS. Each item must be testable.
Each item traces to one or more CuRS items and to one or more SAD items.

## Traceability Summary

| SRS | ← CuRS | → SAD | → AT |
|-----|--------|-------|------|
| [SRS-001](./SRS-001.md) | [CuRS-001](../curs/CuRS-001.md) | [SAD-001](../sad/SAD-001.md) | [AT-001](../at/AT-001.md) |
| [SRS-002](./SRS-002.md) | [CuRS-001](../curs/CuRS-001.md) | [SAD-002](../sad/SAD-002.md) | [AT-002](../at/AT-002.md) |
```

---

## Traceability Link Format

Links appear under the `## Traces` heading. Use **relative paths directly to the item file**. No anchors needed — each item is its own page.

```markdown
## Traces
- ← [CuRS-002](../curs/CuRS-002.md): <why this item originates from that upstream item>
- → [SAD-003](../sad/SAD-003.md): <why this downstream item is the response to this item>
- ↔ [SRS-008](../srs/SRS-008.md): <why these two peer items are related>
```

Direction convention:
- `←` upstream (where this item originates from)
- `→` downstream (what this item produces or is tested by)
- `↔` lateral (peer items in the same layer that constrain or relate to each other)

---

## SAD-Specific Conventions

SAD items must include enough detail for the human to create files and directories without guessing.

### SAD-001: always the directory structure item

`SAD-001.md` is reserved for the project directory structure. Created at init, updated whenever the structure changes.

```markdown
# SAD-001: Project directory structure

## State
`draft`

## Tags
`#structure`

## Why
A shared, authoritative directory map prevents component placement ambiguity across all other SAD items.

## Traces
- ← [SRS-001](../srs/SRS-001.md): SRS-001 defines the top-level system scope; this directory structure reflects the module boundaries implied by those requirements

## Diagram

\`\`\`mermaid
graph TD
  root["project/"] --> src["src/"]
  root --> tests["tests/"]
  src --> auth["auth/"]
  src --> user["user/"]
  src --> api["api/"]
\`\`\`

\`\`\`
src/
  auth/
    AuthService.{ext}
    SessionStore.{ext}
  user/
    UserRepository.{ext}
  api/
    router.{ext}
tests/
  at/
  sit/
  ut/
\`\`\`

> **Review needed** — confirm file extension and whether a monorepo layout is needed
```

### Component item

```markdown
# SAD-003: AuthService component

## State
`draft`

## Tags
`#auth` `#security`

## Why
Centralizing credential validation and session management in one component keeps auth logic auditable and prevents it from leaking into other layers.

## Traces
- ← [SRS-007](../srs/SRS-007.md): SRS-007 requires email/password authentication; AuthService is designated to own this responsibility end-to-end
- ← [SRS-008](../srs/SRS-008.md): SRS-008 requires account lockout; this policy is enforced within AuthService to keep auth logic centralized
- → [SDD-010](../sdd/SDD-010.md): SDD-010 specifies authenticate(), the core credential validation function of this component
- → [SIT-003](../sit/SIT-003.md): SIT-003 verifies that AuthService integrates correctly with UserRepository and SessionStore

## Diagram

\`\`\`mermaid
graph LR
  Router --> AS["AuthService\nsrc/auth/AuthService.ts"]
  AS --> UR["UserRepository (SAD-004)"]
  AS --> SS["SessionStore (SAD-005)"]
\`\`\`

## Location
`src/auth/AuthService.{ext}`

## Responsibility
Authenticate users, manage sessions, enforce lockout policy.

## Dependencies
UserRepository (SAD-004), SessionStore (SAD-005)

## Interface
- `authenticate(email, password) → Session | AuthError`
- `logout(sessionId) → void`
- `checkLockout(email) → LockoutStatus`

> **Review needed** — should AuthService own session creation, or delegate to a separate SessionService?
```

---

## SDD-Specific Conventions

SDD items must be detailed enough for the human to write the function body without ambiguity.

```markdown
# SDD-010: AuthService.authenticate()

## State
`draft`

## Tags
`#auth` `#security`

## Why
This is the sole entry point for credential validation; centralizing the logic here ensures lockout, hashing, and session creation always happen together.

## Traces
- ← [SAD-003](../sad/SAD-003.md): SAD-003 defines AuthService as the owner of credential validation; this function is its primary entry point
- → [UT-010](../ut/UT-010.md): UT-010 tests this function in isolation covering the happy path, wrong-password, and lockout cases

## Diagram

\`\`\`mermaid
flowchart TD
  A[Look up user by email] --> B{Found?}
  B -- No --> C[Return INVALID_CREDENTIALS]
  B -- Yes --> D{checkLockout}
  D -- Locked --> E[Return ACCOUNT_LOCKED]
  D -- OK --> F{bcrypt compare}
  F -- Mismatch --> G[Increment counter\nReturn INVALID_CREDENTIALS]
  F -- Match --> H[Reset counter\nCreate session\nReturn Session]
\`\`\`

## Signature
`authenticate(email: string, password: string): Session | AuthError`

## Algorithm
1. Look up user by email in UserRepository. If not found, return `AuthError.INVALID_CREDENTIALS`.
2. Check lockout status via `checkLockout(email)`. If locked, return `AuthError.ACCOUNT_LOCKED`.
3. Compare password against stored bcrypt hash (cost factor 12). If mismatch, increment failure counter and return `AuthError.INVALID_CREDENTIALS`.
4. On success, reset failure counter. Create session with 24h expiry. Return session.

## Variables
- `user: User | null` — result of UserRepository lookup
- `lockout: LockoutStatus` — current lockout state for this email

## Error cases
- `AuthError.INVALID_CREDENTIALS` — wrong email or password (do not distinguish which)
- `AuthError.ACCOUNT_LOCKED` — 5+ consecutive failures

## Side effects
Writes to failure counter store on failure. Writes session on success.

> **Review needed** — confirm bcrypt cost factor (12) matches the production security policy
```

---

## Scanning Items

```bash
# List all items of a type
ls book/src/srs/
ls book/src/sad/

# Read a specific item
cat book/src/srs/SRS-007.md

# All draft items across all types
grep -rl "^\`draft\`" book/src/

# Items with a specific tag
grep -rl "#auth" book/src/

# All pending review points
grep -rl "Review needed" book/src/

# Find next available ID for a type (e.g. SRS)
ls book/src/srs/ | grep "^SRS-" | sort | tail -1
```

---

## Referencing Existing Items Efficiently

When writing a new item that needs to reference existing items, use these patterns to quickly locate relevant items without reading every file.

### Find items by tag

```bash
# All items tagged #auth
grep -rl "#auth" book/src/

# Items tagged #auth that are reviewed (ready to reference)
for f in $(grep -rl "#auth" book/src/); do
  grep -l "^\`reviewed\`" "$f"
done
```

### Find items by ID reference

```bash
# Which SDD items already reference SAD-003?
grep -rl "\[SAD-003\]" book/src/sdd/

# Which AT items already reference SRS-007?
grep -rl "\[SRS-007\]" book/src/at/
```

### Find the next available ID

```bash
# Next SRS ID
ls book/src/srs/ | grep "^SRS-[0-9]" | sort -t- -k2 -n | tail -1

# Next SDD ID
ls book/src/sdd/ | grep "^SDD-[0-9]" | sort -t- -k2 -n | tail -1
```

### Read a specific item quickly

```bash
# Read just the header fields of an item
head -25 book/src/srs/SRS-007.md

# Read only the Traces section
grep -A10 "^## Traces" book/src/sad/SAD-003.md
```

### Find all items in a component's scope

When writing SDD items for a new SAD component, find what SRS items it must satisfy:

```bash
# Items that reference SAD-003 upstream
grep -rl "\[SAD-003\]" book/src/srs/   # SRS items pointing to this component
grep -rl "\[SAD-003\]" book/src/sdd/   # SDD items already under this component
grep -rl "\[SAD-003\]" book/src/sit/   # SIT items covering this component
```

### Check traceability gaps before writing

Before creating a new item, verify what already exists to avoid duplicates:

```bash
# Does any SRS item already cover this customer requirement?
grep -rl "\[CuRS-002\]" book/src/srs/

# Does any SDD item already design this function?
grep -rl "authenticate" book/src/sdd/

# Does any UT item already test this SDD item?
grep -rl "\[SDD-010\]" book/src/ut/
```
