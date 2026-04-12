---
name: lb-init
description: |
  Use this skill to initialize a new literate programming book for a software repository. Triggers: "init the book", "set up the book", "create the book", "book doesn't exist yet", "start the mdbook", or any request to begin literate programming documentation for a project that has no book/ directory yet. Also triggers if the user mentions mdbook setup, book.toml, or mdbook-mermaid installation for a new project.
---

# lb-init: Initialize the Literate Book

Sets up the `book/` directory for a new program-as-book.

---

## Step 1: Install tooling (if needed)

```bash
which mdbook || cargo install mdbook
which mdbook-mermaid || cargo install mdbook-mermaid
```

If `cargo` is not available, note this and ask the user to install manually:
- https://www.rust-lang.org/tools/install (for cargo)
- `cargo install mdbook mdbook-mermaid`

---

## Step 2: Initialize

```bash
mdbook init book --title "<repo-name>" --ignore git
mdbook-mermaid install book/
```

Replace `<repo-name>` with the actual repository or project name.

---

## Step 3: Configure book.toml

Replace the generated `book/book.toml` with:

```toml
[book]
language = "en"
multilingual = false
src = "src"
title = "<repo-name>"

[preprocessor.mermaid]
command = "mdbook-mermaid"

[output.html]
additional-js = ["mermaid.min.js", "mermaid-init.js"]
```

---

## Step 4: Create initial files

Create only two files. Do **not** pre-create folders like `requirements/`, `architecture/`, or `design/` — the structure grows from the subject matter.

**book/src/SUMMARY.md**:
```markdown
# Summary

- [Introduction](./introduction.md)
```

**book/src/introduction.md**:
```markdown
# Introduction

<!-- DRAFT: initial introduction stub — fill in the problem story -->

## The Problem

*What problem does this program solve? Who has this problem, and how bad is it?*

## What We Tried Before

*What alternatives existed or were attempted? Why didn't they work?*

## The Core Idea

*What is the essential insight or approach of this solution?*
```

---

## Step 5: Build check

```bash
cd book && mdbook build 2>&1
```

Fix any errors before presenting to the user.

---

## Output

Tell the user:
- Book initialized at `book/`
- `introduction.md` has a `DRAFT` stub — fill in the problem story
- Topic chapters are added on demand using **lb-feature** as the program grows
- The structure (chapters, subdirectories) emerges from the subject matter, not from a template

---

## Next Steps for the User

1. Fill in `introduction.md` — answer the three stub questions
2. Remove the `DRAFT` flag when satisfied
3. Use **lb-feature** to add the first topic chapter
