---
name: pofe-init
description: |
  Initialize a POFE knowledge base — a personal productivity system combining daily journaling, goal management, achievement tracking, wiki, and work pattern analysis, all rendered via mdbook. Run once per repo. Use whenever the user wants to set up a journal, knowledge base, personal productivity system, or goal-tracking repo from scratch.
  Triggers: "init pofe", "set up knowledge base", "initialize journal", "create knowledge base", "start my productivity system", or any request to bootstrap a personal journal/wiki/goal system.
---

# pofe-init: Initialize the POFE Knowledge Base

**Goal**: Bootstrap a clean repo with mdbook structure, daily journal, wiki, goal hierarchy, achievement archive, and work pattern tracking. Run once.

---

## Step 1: Install tooling

```bash
which mdbook || cargo install mdbook
which mdbook-mermaid || cargo install mdbook-mermaid
```

If `cargo` is not available:
> Install Rust: https://www.rust-lang.org/tools/install  
> Then: `cargo install mdbook mdbook-mermaid`

---

## Step 2: Create directory structure

```
<repo-root>/
├── book.toml
├── SUMMARY.md
├── today.md
├── patterns.md
├── Journal/
│   └── README.md
├── wiki/
│   └── README.md
├── goals/
│   ├── goal.md                    # overall/lifetime goals
│   └── YYYY/
│       ├── goal.md                # yearly
│       ├── goal-MM.md             # monthly
│       ├── goal-MM-WNN.md         # weekly
│       └── goal-MM-DD.md          # daily
└── archive/
    ├── archive.md                 # all-time achievements
    └── YYYY/
        ├── archive.md             # yearly
        ├── archive-MM.md          # monthly
        └── archive-MM-WNN.md      # weekly
```

Add `book/` to `.gitignore`.

---

## Step 3: Write book.toml

```toml
[book]
title = "POFE"
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

- [Goals](goals/goal.md)
- [Journal](Journal/README.md)
- [Wiki](wiki/README.md)
- [Patterns](patterns.md)
- [Archive](archive/archive.md)
```

`pofe-review` will append new entries automatically.

---

## Step 5: Create seed files

**today.md** — fill in today's actual date:
```markdown
<!-- today: YYYY-MM-DD -->
<!-- Write freely below. No format required. -->

```

**patterns.md**:
```markdown
# Work Patterns

## Category Frequency
| Category | Total | Last 30d | Trend |
|----------|-------|----------|-------|

## Automation Opportunities

## Insights

*Last updated: YYYY-MM-DD*
```

**goals/goal.md**:
```markdown
# Goals

## Tasks

### (add your topics here)
- [ ] ...
```

**goals/YYYY/goal.md** (current year):
```markdown
# YYYY

## Tasks

### (topic)
- [ ] ...
```

**goals/YYYY/goal-MM.md** (current month):
```markdown
# YYYY-MM

> [Yearly](goal.md)

## Tasks

### (topic)
- [ ] ...
```

**goals/YYYY/goal-MM-WNN.md** (current week, compute WNN from today's date):
```markdown
# YYYY WNN · Mon DD – Sun DD

> [Monthly](goal-MM.md) · [Yearly](goal.md)

## Tasks

### (topic)
- [ ] ...

## Adjustment Log
```

**goals/YYYY/goal-MM-DD.md** (today):
```markdown
# YYYY-MM-DD

> [Monthly](goal-MM.md) · [Weekly](goal-MM-WNN.md)

## Tasks

### (topic)
- [ ] ...

## Adjustment Log
```

**archive/archive.md**, **archive/YYYY/archive.md**, **archive/YYYY/archive-MM.md**, **archive/YYYY/archive-MM-WNN.md** — create with empty structure using the archive format (see pofe-review for format details).

**Journal/README.md**, **wiki/README.md** — brief one-line intro.

---

## Step 6: Initialize git

If not already a repo:
```bash
git init
git add .
```

Show the suggested first commit message — do not commit:
```
chore: initialize POFE knowledge base
```

---

## Step 7: Tell the user what's next

> POFE initialized.
> - Write freely in `today.md` throughout the day.
> - Fill in your goals in `goals/YYYY/goal-MM-DD.md` before starting work.
> - Run `/pofe-review` at end of day to archive, extract knowledge, and plan tomorrow.
> - Run `/pofe-adjust` mid-day if priorities change.
> - Run `mdbook serve` to preview the book.
