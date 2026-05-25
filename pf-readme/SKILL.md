---
name: pf-readme
description: |
  Write or update README.md files for project directories — reads the code, grills the user to understand each directory's purpose, then writes concise markdown documentation. Works on any directory: src/, tests/, scripts/, etc.
  Use when the user wants to document directory structure, add per-directory READMEs, or update existing ones. Triggers: "pf-readme", "document directories", "write directory readme", "add readme", "explain directory structure", "document this folder", "readme for src", "readme for tests".
---

Read `../pf/references/caveman.md` and apply caveman style throughout.

# PF README

Write per-directory README.md files. Read code, grill user, write docs.

## Step 1: Resolve scope

If user names a directory → target that one. Otherwise scan:

```bash
find . -mindepth 1 -maxdepth 2 -type d | grep -v -E '(node_modules|\.git|__pycache__|\.pf|venv|dist|build)' | sort
```

List found directories. Ask via `AskUserQuestion` (multi-select): which to document, or "All".

## Step 2: Check project state

```bash
find . -mindepth 1 -maxdepth 3 -type f | grep -v -E '(node_modules|\.git|__pycache__|\.pf|venv|dist|build)' | wc -l
```

If project is empty (0–3 files) → grill about the project first (plain text, one at a time):
- What is this project? What does it do?
- Why does it exist? What problem does it solve?
- Who will use it?
- What are the planned top-level directories and their purpose?

Use answers to inform all subsequent READMEs. Write root `./README.md` as well.

For each target directory:

```bash
ls -la <dir>/
```

Read key files — entry points, index, main module, any existing README. Note: file types, naming patterns, what's exported or defined.

## Step 3: Grill

For each directory, one question at a time (plain text):
- What is the main purpose of `<dir>/`?
- What must a new contributor know before touching this?
- Any conventions, naming rules, or gotchas?
- What does NOT belong here?

User can say **"wrap up"** to skip to writing.

## Step 4: Write README

Save: `<dir>/README.md`

```markdown
# <dir>/

<one-line purpose>

## What's here

<bullet list — key files/subdirs and what each does>

## Conventions

<rules, naming patterns, what belongs / doesn't belong>

## Notes

<gotchas, non-obvious details — omit section if none>
```

Present tense. No filler. Skip empty sections.

Print after each write:
```
README: <dir>/README.md
```

## Step 5: Done

List all files written. Suggest commit message.
