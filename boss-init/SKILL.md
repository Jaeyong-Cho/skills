---
name: boss-init
description: |
  Use this skill to initialize a new BOSS book for a software project. Triggers: "init boss", "set up boss", "start the documentation", "create boss", or any request to begin V-model documentation for a project. If the project already has source code, also bootstraps initial CuRS, SRS, SAD, SDD, AT, SIT, and UT items from the existing codebase. Creates the mdbook structure, CSS theme override, all document chapters, tag registry, and project directory skeleton.
---

# boss-init: Initialize the BOSS Book

**Goal**: Set up `book/` with full V-Doc chapter structure, CSS theme override, empty tag registry, and project source/test directories. If the project already has source code, also generate initial draft BOSS items by reverse-engineering the existing codebase.

Read before starting:
- `references/items.md` — item format, ID system, states, tags
- `references/structure.md` — directory layout and per-document conventions

---

## Step 1: Install tooling (if needed)

```bash
which mdbook || cargo install mdbook
which mdbook-mermaid || cargo install mdbook-mermaid
```

If `cargo` is not available, tell the user to install it first:
- https://www.rust-lang.org/tools/install
- Then: `cargo install mdbook mdbook-mermaid`

---

## Step 2: Initialize mdbook

```bash
mdbook init book --title "<project-name>" --ignore git
mdbook-mermaid install book/
```

Replace `<project-name>` with the actual project name.

---

## Step 3: Generate theme and apply CSS override

```bash
cd book
mdbook init --theme
```

This creates `book/theme/` with the default theme files. Then open `book/theme/css/variables.css` and set the content width at the top of the `:root` block:

```css
:root {
    --content-max-width: 80%;
}
```

The full `:root` block will already contain many variables — add or replace only the `--content-max-width` line; leave everything else intact.

---

## Step 4: Configure book.toml

Replace `book/book.toml` with:

```toml
[book]
language = "en"
multilingual = false
src = "src"
title = "<project-name>"

[preprocessor.mermaid]
command = "mdbook-mermaid"

[output.html]
additional-js = ["mermaid.min.js", "mermaid-init.js"]
additional-css = ["theme/css/variables.css"]
```

---

## Step 5: Create SUMMARY.md

```markdown
# Summary

- [Tags](./tags.md)
- [Customer Requirements](./curs/index.md)
- [Software Requirements](./srs/index.md)
- [Architectural Design](./sad/index.md)
- [Detailed Design](./sdd/index.md)
- [Acceptance Tests](./at/index.md)
- [Integration Tests](./sit/index.md)
- [Unit Tests](./ut/index.md)
```

Item entries are added as nested lines under each section by **boss-update** as items are created.

---

## Step 6: Create tags.md

```markdown
# Tag Registry

All tags used across BOSS items. Consult this before creating new tags. Add new tags here before using them in items.

| Tag | Description | Item Count |
|-----|-------------|------------|

_No tags yet. Tags are added as items are created._
```

---

## Step 7: Create index stubs

Create one `index.md` per document type. Item files are created separately by **boss-update**.

**book/src/curs/index.md**:
```markdown
# Customer Requirements (CuRS)

Raw customer intent captured verbatim or near-verbatim. CuRS items are the upstream source for SRS items.
Each CuRS item records what the customer said, not what will be built.

## Traceability Summary

| CuRS | → SRS |
|------|-------|

_No items yet. Add customer requirements using **boss-update**._
```

**book/src/srs/index.md**:
```markdown
# Software Requirements Specification (SRS)

Formal requirements derived from CuRS. Each item must be testable.
Each item traces to one or more CuRS items and to one or more SAD items.

## Traceability Summary

| SRS | ← CuRS | → SAD | → AT |
|-----|--------|-------|------|

_No items yet._
```

**book/src/sad/index.md**:
```markdown
# Software Architectural Design (SAD)

Component structure, directory layout, file names, and inter-component interfaces.
SAD items must be specific enough for a human to create the files and directories without ambiguity.

## Directory Structure

_To be filled in by SAD-001._

## Traceability Summary

| SAD | ← SRS | → SDD | → SIT |
|-----|-------|-------|-------|

_No items yet._
```

**book/src/sdd/index.md**:
```markdown
# Software Detailed Design (SDD)

Function signatures, algorithms, variable names, and error handling.
SDD items must be specific enough for a human to write the function body without guessing.

## Traceability Summary

| SDD | ← SAD | → UT |
|-----|-------|------|

_No items yet._
```

**book/src/at/index.md**:
```markdown
# Acceptance Tests (AT)

Black-box tests that verify SRS items from the user's perspective.

## Traceability Summary

| AT | ← SRS |
|----|-------|

_No items yet._
```

**book/src/sit/index.md**:
```markdown
# Software Integration Tests (SIT)

Tests that verify SAD-level component interactions.

## Traceability Summary

| SIT | ← SAD |
|-----|-------|

_No items yet._
```

**book/src/ut/index.md**:
```markdown
# Unit Tests (UT)

Tests that verify individual functions and classes defined in SDD.

## Traceability Summary

| UT | ← SDD |
|----|-------|

_No items yet._
```

---

## Step 8: Create project source directories

```bash
mkdir -p src
mkdir -p tests/at tests/sit tests/ut
```

---

## Step 9: Build check

```bash
cd book && mdbook build 2>&1
```

Fix all errors before reporting.

---

## Step 10: Bootstrap documents from existing code (if applicable)

**Only do this step if the project already has source code** (i.e., `src/` contains non-empty files, or there are source files in the project root beyond scaffolding).

The goal is to reverse-engineer a first draft of all BOSS layers from the existing codebase, so the team has a documentation baseline to review and refine rather than starting from scratch.

### 10a. Survey the codebase

```bash
find . -not -path './book/*' -not -path './.git/*' \
  -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" \
  -o -name "*.rs" -o -name "*.java" -o -name "*.c" -o -name "*.cpp" \
  | head -60
```

Read key files: entry points, main modules, public interfaces, README if present, any existing tests. Build a mental model of:
- What the software does (user-facing behaviour)
- How it is structured (components and their responsibilities)
- What the important functions and data structures are
- What tests already exist

### 10b. Write CuRS items

Infer 1–3 customer-level requirements from the observable purpose of the software. Each CuRS captures *what the software does for its users*, not implementation details.

Create `book/src/curs/CuRS-{NNN}.md` for each. Use the item template from `references/items.md`. Mark state `draft`. Add a review point asking the team to confirm the inferred customer intent.

Add entries to `SUMMARY.md` and `book/src/curs/index.md`.

### 10c. Derive SRS items

For each CuRS, derive testable software requirements. Each SRS item must trace back to a CuRS and describe a specific, measurable behaviour the software shall provide.

Create `book/src/srs/SRS-{NNN}.md` for each. Mark state `draft`. Link to the CuRS that motivated it.

Add entries to `SUMMARY.md` and `book/src/srs/index.md`.

### 10d. Write SAD items

Describe the architectural components you observed: directories, modules, key interfaces. SAD-001 must describe the directory structure. Subsequent items describe each significant component.

Create `book/src/sad/SAD-{NNN}.md` for each. Mark state `draft`. Trace to the SRS items that each component satisfies.

Add entries to `SUMMARY.md` and `book/src/sad/index.md`.

### 10e. Write SDD items

For each significant function or class in the codebase, create an SDD item describing its signature, behaviour, and error handling. Focus on the public API surface first; private helpers only if they are complex.

Create `book/src/sdd/SDD-{NNN}.md` for each. Mark state `draft`. Trace to the SAD component.

Add entries to `SUMMARY.md` and `book/src/sdd/index.md`.

### 10f. Write AT, SIT, UT items

- **AT**: One acceptance test per SRS item, based on the observable behaviour. If automated tests already exist, map them to AT items.
- **SIT**: One integration test per SAD component boundary. If existing integration tests exist, map them.
- **UT**: One unit test per SDD item covering the core logic path. If existing unit tests exist, map them.

Create the item files. Mark state `draft`. Trace back to the relevant SRS/SAD/SDD items respectively.

Add entries to `SUMMARY.md` and the respective `index.md` files.

### 10g. Update tags.md

Add tags used across all new items to the tag registry.

### 10h. Build check

```bash
cd book && mdbook build 2>&1
```

Fix all broken links before continuing.

---

## Step 11: Generate project overview

After all files are written and the build passes, run **boss-overview** to produce a full project overview. This gives the user an immediate bird's-eye view of what was just created.

---

## Step 12: Report

Tell the user:

**If no source code existed:**
```
BOSS initialized.

Book:    book/  (mdbook + mermaid)
Theme:   book/theme/css/variables.css (--content-max-width: 80%)
Chapters: CuRS · SRS · SAD · SDD · AT · SIT · UT
          Each item is a separate file within its chapter directory.
Tags:    book/src/tags.md (empty — populated as items are added)

Source:  src/
Tests:   tests/at/  tests/sit/  tests/ut/

Next step: Use boss-curs with your first customer requirement.
```

**If source code was found and documents were bootstrapped:**
```
BOSS initialized and bootstrapped from existing code.

Book:    book/  (mdbook + mermaid)
Chapters: CuRS · SRS · SAD · SDD · AT · SIT · UT
          <N> items created across all layers (all marked draft)
Tags:    book/src/tags.md

All items are draft — they represent AI's best reading of the existing code.
Review each layer and answer the review points before running the boss-* review skills.

Next step: Open book/src/curs/ and review the inferred customer requirements.
           Correct anything that doesn't match your actual intent, then run boss-srs.
```

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
chore(boss): <short description under 72 chars>

Why: <what prompted initializing the BOSS book — new project or existing codebase being documented>
What: <what was created — book structure, chapters, item count if bootstrapped from code>
```

Keep `Why` and `What` to one or two sentences each — enough for someone reading `git log` to understand the change without opening the diff.
