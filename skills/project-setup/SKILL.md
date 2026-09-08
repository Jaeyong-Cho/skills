---
name: project-setup
description: Scaffold a new or existing project's baseline hygiene — README.md, INSTALL.md, a commit-msg hook enforcing Conventional Commits (feat(topic), fix(topic), ...), a post-merge hook that flags dependency-manifest changes, and a main/develop branch strategy. Use when the user wants to set up a new repo, add commit message linting, wire up git hooks, or establish a branching model. Idempotent — safe to re-run on an existing repo, it only fills in whatever's missing.
---

# Project Setup

Scaffold the six baseline artifacts below in the target repo. This is idempotent: on an already-set-up repo, check each item independently and only apply the ones missing. Skip (don't overwrite) anything that already exists, and say so.

1. **Detect the project's language.** Look for `go.mod`, `package.json`, `pyproject.toml`/`requirements.txt`, or `Cargo.toml` at the repo root. Completion criterion: language(s) identified, or explicitly "none detected" if no recognized manifest exists.
2. **Commit-msg hook.** Copy `hooks/commit-msg` from this skill into the target repo's `.githooks/commit-msg` (create `.githooks/` if missing), `chmod +x` it, then run `git config core.hooksPath .githooks`. It enforces Conventional Commits (`feat(topic): ...`, `fix(topic): ...`, plus `docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`), letting git's own `Merge ...`/`Revert ...` messages through unchecked. Completion criterion: `.githooks/commit-msg` is executable, `git config core.hooksPath` reports `.githooks`, and `hooks/commit-msg.test.sh` (copied alongside it) passes.
3. **Post-merge hook.** Copy `hooks/post-merge` the same way into `.githooks/post-merge`, `chmod +x` it — no separate `core.hooksPath` config needed, step 4 already set it. It diffs `ORIG_HEAD..HEAD` for manifest files (`go.mod`, `package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, and their lockfiles) and prints a reminder to reinstall when any changed. Completion criterion: file is executable.
4. **Branch strategy.** Create a `develop` branch from `main` if one doesn't already exist (`git branch develop main`; don't switch to it). Then append a `## Branching` section to README.md (skip if that section already exists) documenting: `main` is releases only; `develop` is the integration branch; work happens on `<type>/<topic>` branches cut from `develop` and merged back into `develop` via PR, where `<type>` matches the commit-msg types (`feature`, `fix`, `refactor`, `docs`, `chore`, ...); `develop` merges into `main` for releases. Completion criterion: `develop` branch exists, and README.md has a `## Branching` section.

Once complete, tell the user which of the six artifacts were created vs. already present (skipped). Note that `core.hooksPath` is a per-clone git config — each teammate's existing clone needs to run step 4's `git config` line too, or the repo should commit `.githooks/` and mention that setup step in the README.

## Baml Setup
Set up BAML in this repo so I can write great agent first code.

Install the toolchain (pick one for this machine):
- Homebrew (macOS/Linux): brew install baml
- curl (macOS/Linux): curl -fsSL https://pkg.boundaryml.com/install.sh | sh -s
- Arch: yay -S baml-bin
- Windows: irm https://pkg.boundaryml.com/install.ps1 | iex

Then set up the project:
- baml init
- baml agent install
- baml run main

If this repo already has an app in another language, wire up the bridge so it
can call BAML directly. Run baml bridge add <target> once, then
baml bridge generate whenever the .baml files change. The add command prints
the host package to install. Targets:
- Python: python/pydantic
- TypeScript: typescript/node
- TS / Web: typescript/web
- Go: go (also pass --sdk-import-path <MODULE>/baml_sdk)
- Rust: rust
- Java: java
- Kotlin: java (the Gradle plugin adds the Kotlin layer)
- C#: csharp
- C++: cpp
- Swift: swift
- Pydantic v1: python/pydantic/v1

After that, use the BAML skill and baml describe to write and edit .baml files.