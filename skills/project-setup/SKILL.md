---
name: project-setup
description: Scaffold a new or existing project's baseline hygiene — README.md, INSTALL.md, a commit-msg hook enforcing Conventional Commits (feat(topic), fix(topic), ...), and a post-merge hook that flags dependency-manifest changes. Use when the user wants to set up a new repo, add commit message linting, or wire up git hooks.
---

# Project Setup

Scaffold the five baseline artifacts below in the target repo. Skip (don't overwrite) anything that already exists, and say so.

1. **Detect the project's language.** Look for `go.mod`, `package.json`, `pyproject.toml`/`requirements.txt`, or `Cargo.toml` at the repo root. Completion criterion: language(s) identified, or explicitly "none detected" if no recognized manifest exists.
2. **README.md** — create if missing. Sections: title, one-line description, `## Installation` (pointing to INSTALL.md), `## Usage` placeholder, `## License` placeholder. Completion criterion: file exists with all four sections.
3. **INSTALL.md** — create if missing. Contents: prerequisites, clone step, the install/build command matched to the language from step 1 (`go build ./...`, `npm install`, `pip install -r requirements.txt`, `cargo build`), and a "Verify" step (run tests). Completion criterion: file exists; its install command matches the detected language, or states "no manifest detected — add build/install steps manually" if none.
4. **Commit-msg hook.** Copy `hooks/commit-msg` from this skill into the target repo's `.githooks/commit-msg` (create `.githooks/` if missing), `chmod +x` it, then run `git config core.hooksPath .githooks`. It enforces Conventional Commits (`feat(topic): ...`, `fix(topic): ...`, plus `docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`), letting git's own `Merge ...`/`Revert ...` messages through unchecked. Completion criterion: `.githooks/commit-msg` is executable, `git config core.hooksPath` reports `.githooks`, and `hooks/commit-msg.test.sh` (copied alongside it) passes.
5. **Post-merge hook.** Copy `hooks/post-merge` the same way into `.githooks/post-merge`, `chmod +x` it — no separate `core.hooksPath` config needed, step 4 already set it. It diffs `ORIG_HEAD..HEAD` for manifest files (`go.mod`, `package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, and their lockfiles) and prints a reminder to reinstall when any changed. Completion criterion: file is executable.

Once complete, tell the user which of the five artifacts were created vs. already present (skipped). Note that `core.hooksPath` is a per-clone git config — each teammate's existing clone needs to run step 4's `git config` line too, or the repo should commit `.githooks/` and mention that setup step in the README.
