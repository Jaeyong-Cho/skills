---
name: journal-init
description: |
  Initialize a markdown-based personal knowledge base with mdbook for daily journaling, wiki management, and end-of-day review. Run once to set up the full repo structure. Use this skill whenever the user wants to set up a journal, knowledge base, or note-taking system — even if they don't say "journal-init" explicitly.
  Triggers: "init journal", "set up knowledge base", "initialize journal", "create knowledge base", "set up my journal repo", "start my knowledge system", or any request to bootstrap a personal journal/wiki from scratch.
---

# journal-init: Initialize the Knowledge Base

**Goal**: Bootstrap a clean git repo with mdbook structure, `Journal/` for daily entries, and `wiki/` for evergreen knowledge. Only run once per repo.

---

## Step 1: Install tooling

```bash
which mdbook || cargo install mdbook
which mdbook-mermaid || cargo install mdbook-mermaid
```

If `cargo` is not available, tell the user:
> Install Rust first: https://www.rust-lang.org/tools/install  
> Then: `cargo install mdbook mdbook-mermaid`

---

## Step 2: Create directory structure

```
<repo-root>/
├── book.toml
├── SUMMARY.md
├── today.md
├── Journal/
│   └── README.md
└── wiki/
    └── README.md
```

Add `book/` to `.gitignore` (mdbook build output).

---

## Step 3: Write book.toml

```toml
[book]
title = "Knowledge Base"
src = "."
language = "en"

[output.html]
git-repository-url = ""

[preprocessor.mermaid]
command = "mdbook-mermaid"
```

---

## Step 4: Write SUMMARY.md

```markdown
# Summary

- [Journal](Journal/README.md)
- [Wiki](wiki/README.md)
```

The `journal-review` skill will append new entries here automatically.

---

## Step 5: Write index pages

**Journal/README.md**
```markdown
# Journal

Daily work entries. One file per day: `Journal/YYYY/MM-DD.md`.
```

**wiki/README.md**
```markdown
# Wiki

Evergreen knowledge notes. Each file covers one topic and carries inline tags like `#tag`.
```

---

## Step 6: Initialize git

If the directory is not already a git repo:
```bash
git init
git add .
```

Show the user this suggested first commit message — do not commit automatically:
```
chore: initialize knowledge base with mdbook structure
```

---

## Step 5b: Write today.md

Create `today.md` at the repo root with this starter content:

```markdown
<!-- today: YYYY-MM-DD -->
<!-- Write freely below. No format required. -->

```

Fill in the actual date.

---

## Step 7: Tell the user what's next

> Knowledge base initialized.  
> - Write freely in `today.md` throughout the day — no format required.  
> - At the end of the day, run `/journal-review` to generate the report, archive today.md, seed tomorrow's plan, and get a commit message.  
> - Run `mdbook serve` anytime to preview the book in your browser.
