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

Daily goals live inside `today.md` — not as separate files. `goals/` holds weekly and above only.

```
<repo-root>/
├── book.toml
├── SUMMARY.md
├── today.md              # daily journal + daily goal at top
├── patterns.md
├── Journal/
│   └── README.md
├── wiki/
│   └── README.md
├── goals/
│   ├── goal.md           # overall/lifetime goals
│   └── YYYY/
│       ├── goal.md       # yearly
│       ├── goal-MM.md    # monthly
│       └── goal-MM-WNN.md # weekly
└── archive/
    ├── archive.md
    └── YYYY/
        ├── archive.md
        ├── archive-MM.md
        └── archive-MM-WNN.md
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
- [Stats](stats.md)
- [Archive](archive/archive.md)
```

`pofe-review` will append new entries automatically.

---

## Step 5: Create seed files

**today.md** — daily goal at top: single concrete actions executable today. Each task states which weekly deliverable it fulfills and why doing it today is the right move. Long-running independent tasks are marked `*(bg)*` and listed under `> Trigger first` so they start at the top of the day and run in parallel with other work.
```markdown
<!-- today: YYYY-MM-DD -->

## Goals

> [Weekly](goals/YYYY/goal-MM-WNN.md) · [Monthly](goals/YYYY/goal-MM.md)

> Trigger first (background):
> - Task name *(~Xh)* — start now; runs while other work proceeds

### (Topic)
- [ ] Long-running task *(High)* *(bg)* — rationale *(→ Weekly: deliverable name)*
  - [ ] Sub-step one
- [ ] Specific action *(High)* *(ai: how AI helps here)* — why this action completes/advances the weekly deliverable *(→ Weekly: deliverable name)*
  - [ ] Sub-step one
  - [ ] Sub-step two
- [ ] Specific action *(Medium)* — rationale *(→ Weekly: deliverable name)*
  - [ ] Sub-step one

## Adjustment Log

---

<!-- Write freely below. No format required. -->

```

**stats.md**:
```markdown
# Work Statistics

## All Time

| Type | Sessions | Est. Hours | Last Active |
|------|----------|------------|-------------|

## YYYY

| Type | Sessions | Est. Hours |
|------|----------|------------|

## YYYY-MM

| Type | Sessions | Est. Hours |
|------|----------|------------|

## YYYY-WNN

| Type | Sessions | Est. Hours |
|------|----------|------------|

## Insights

_Not enough data yet._

## Automation Candidates

_Not enough data yet._

*Last updated: YYYY-MM-DD*
```

**goals/goal.md** — abstract, direction-setting. Each goal is a title + the effect of achieving it. No task lists here.
```markdown
# Goals

## (Goal Title)
**Effect**: What achieving this means — the long-term impact on your life, career, or work.

## (Goal Title)
**Effect**: ...
```

**goals/YYYY/goal.md** (current year) — major milestones that move each total goal forward this year. Each milestone states what success looks like and why it matters toward the total goal.
```markdown
# YYYY

> [Total](../goal.md)

## (Topic)
- [ ] Milestone description — why this milestone matters for the total goal *(→ Total: Goal Title)*

## Adjustment Log
```

**goals/YYYY/goal-MM.md** (current month) — concrete objectives measurable within a month. Each task states which yearly milestone it advances and why it is the right step now.
```markdown
# YYYY-MM

> [Yearly](goal.md)

## Tasks

### (Topic)
- [ ] Concrete objective *(High)* — why this month's work moves the yearly milestone forward *(→ Yearly: milestone name)*
- [ ] Concrete objective *(Medium)* — rationale *(→ Yearly: milestone name)*

## Adjustment Log
```

**goals/YYYY/goal-MM-WNN.md** (current week — compute WNN from today's date) — specific deliverables completable in 1–3 days. Each task explains which monthly objective it serves and why it is the right piece this week.
```markdown
# YYYY WNN · Mon DD – Sun DD

> [Monthly](goal-MM.md) · [Yearly](goal.md)

## Tasks

### (Topic)
- [ ] Specific deliverable *(High)* — why this deliverable advances the monthly objective *(→ Monthly: objective name)*
- [ ] Specific deliverable *(Medium)* — rationale *(→ Monthly: objective name)*

## Adjustment Log
```

**archive/archive.md**, **archive/YYYY/archive.md**, **archive/YYYY/archive-MM.md**, **archive/YYYY/archive-MM-WNN.md** — create with empty structure:
```markdown
# Archive · (period)

## Achievements
<!-- Format: YYYY-MM-DD — what was done — why it matters for the final goal #tag *(→ Total: goal title)* -->

## Goal Completion
| Goal | Status | Notes |
|------|--------|-------|

## Patterns Observed
```

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
> - Set your goals in `goals/YYYY/goal-MM-WNN.md` and `goals/YYYY/goal-MM.md`.
> - Each day, write your daily goals at the top of `today.md`, then journal freely below.
> - Run `/pofe-review` at end of day to archive, update goals, extract knowledge, and seed tomorrow.
> - Run `/pofe-adjust` mid-day if priorities change.
> - Run `mdbook serve` to preview the book.
