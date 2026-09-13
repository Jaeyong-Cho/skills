# Verification Structure

A project-level `verify/` interface makes the project's proof of correctness discoverable and executable without replacing its native test, lint, build, or continuous-integration tools.

## Required layout

```text
verify/
├── index.md
├── run.sh
├── prepare/index.md
├── prepare/run.sh
├── ut/index.md
├── ut/run.sh
├── it/index.md
├── it/run.sh
├── e2e/index.md
├── e2e/run.sh
├── style/index.md
├── style/run.sh
├── archi/index.md
└── archi/run.sh
```

Every directory under `verify/` contains `index.md`. Categories may add `<category>/<sub-category>/` directories when useful; avoid unexplained extra depth.

The preparation domain and five verification domains are:

- `prepare/` — deterministic environment, dependency, fixture, database, or service setup required before verification.
- `ut/` — isolated functions, classes, algorithms, parsers, state transitions, and local errors.
- `it/` — interactions between components, databases, processes, serialization boundaries, and service interfaces.
- `e2e/` — complete user-visible scenarios through realistic execution paths; use selectively.
- `style/` — formatting, naming, static analysis, forbidden APIs, complexity, and coding conventions.
- `archi/` — required structure, public interfaces, dependency direction, layer boundaries, and forbidden dependencies.

Use existing project mechanisms in this order:

```text
Reuse → Reference → Wrap → Extend → Create only when necessary
```

Do not move or duplicate existing tests merely to populate `verify/`. A domain runner may invoke a native command from its existing location.

## Runner contract

`verify/run.sh` and every domain `run.sh` (including `prepare/run.sh`) are executable. A runner exits non-zero when its domain fails and zero when it passes. Every item is independently invokable with one command:

```text
./verify/prepare/run.sh
./verify/ut/run.sh
./verify/it/run.sh
./verify/e2e/run.sh
./verify/style/run.sh
./verify/archi/run.sh
```

The root runner must also accept one selected item in one command (`./verify/run.sh <item>`, where `<item>` is `prepare`, `ut`, `it`, `e2e`, `style`, or `archi`). For any selected item other than `prepare`, it runs `prepare` to completion before starting that item. With no selected item, the root runner may provide `fast` and `full` modes, but must preserve the same preparation and ordering semantics.

The loop interface runs `prepare` first, then selects a maximum functional level:

- `ut`: run UT plus Style and Architecture.
- `it`: run UT → IT plus Style and Architecture.
- `e2e`: run UT → IT → E2E plus Style and Architecture.

No UT, IT, E2E, Style, or Architecture runner starts until preparation passes. After preparation passes, IT starts only after UT passes, and E2E starts only after IT passes. Style and Architecture are independent of the functional chain and each other; they may run in parallel. A failure prevents later functional levels from starting. Already-running independent checks may finish so their evidence is retained.

The root runner should preserve the same semantics when it exposes `fast` and `full` modes: fast verification is normally UT + Style + Architecture; full verification includes the selected project-native IT and E2E checks.

## Intent and failure output

Every `index.md` is a local manifest. It documents the directory's purpose and gives each direct child a short description. Prefer entries in this form:

```markdown
- [auth/](./auth/) — Authentication boundary checks.
- [run.sh](./run.sh) — Runs all integration verification.
```

A failed runner or verification loop reports, without inventing details:

```text
Intent: <why this directory or check exists>
Violated: <rule, expected behavior, or stable check name>
Command: <command that failed>
Evidence: <relevant output>
```

The intent comes from the nearest `index.md`. The violated rule comes from the failing check's own assertion, test name, rule identifier, or runner message. If the check supplies no stable rule, report `Violated: <domain> verification failed` and retain the raw evidence.

## Structural invariants

- `V-DIR-001`: every directory under `verify/` has `index.md`.
- `V-DIR-002`: `verify/` has `prepare/`, `ut/`, `it/`, `e2e/`, `style/`, and `archi/`.
- `V-RUN-001`: `verify/` has executable `run.sh`.
- `V-RUN-002`: every top-level domain, including `prepare/`, has executable `run.sh`.
- `V-IDX-001`: each `index.md` references every direct child directory.
- `V-IDX-002`: every local path referenced by an `index.md` exists.
- `V-IDX-003`: every referenced child has a short description.
- `V-IDX-004`: an index describes only its directory and direct children; stale and out-of-scope links are violations.
- `V-DEPTH-001`: implementations normally use `<category>/<sub-category>` below a domain; extra depth needs a reason.

The deterministic linter checks these invariants. It belongs to the skill tooling, not to a project's `verify/` directory.
