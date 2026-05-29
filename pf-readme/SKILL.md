---
name: pf-readme
description: |
  Write or update README.md files for project directories — reads the code, grills the user to understand each directory's purpose, then writes concise markdown documentation. Works on any directory: src/, tests/, scripts/, etc.
  Use when the user wants to document directory structure, add per-directory READMEs, or update existing ones. Triggers: "pf-readme", "document directories", "write directory readme", "add readme", "explain directory structure", "document this folder", "readme for src", "readme for tests".
---

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

If project is empty (0–3 files) → interview using the Socratic method. Purpose: understand what this project is, why it exists, who uses it, planned directory structure. Starting context: the empty project.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

Use answers to inform all READMEs. Write root `./README.md` as well.

For each target directory:

```bash
ls -la <dir>/
```

Read key files — entry points, index, main module, any existing README. Note: file types, naming patterns, what's exported or defined.

## Step 3: Grill

For each directory, interview using the Socratic method. Purpose: understand the purpose of `<dir>/`, what a new contributor must know, conventions and naming rules, what does NOT belong here. Starting context: the files read above.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time. When a question has clear discrete options, use the `AskUserQuestion` tool — list the options with your recommended one first marked "(Recommended)". For open-ended questions with no clear options, ask in plain text.

If a question can be answered by exploring the codebase, explore the codebase instead.

There is no maximum number of questions. Keep going until every branch of the decision tree is resolved — some plans need three questions, some need fifty. If the session feels too long, the user can stop at any time or say "wrap up" to summarise and move on. Natural-language steering is the intended control surface, not a numeric limit.

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
