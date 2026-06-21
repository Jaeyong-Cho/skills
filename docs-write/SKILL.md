---
name: docs-write
description: Write program documentation (architecture, concepts, guides, tutorials) through Socratic grilling, then write to docs/src/. Use when user wants to document how something works, write a guide, explain architecture, or mentions "docs-write", "write docs", "document this", "write a guide".
---

# Docs Write (Program Documentation)

Document how the program works — architecture, concepts, guides, tutorials. Not API design (use api-write for that).

Read [deep-modules](references/deep-modules.md) and [archi](references/archi.md) before starting.

## Step 0: Doc type

Identify what kind of documentation this is:
- **Architecture** — how the system is structured and why
- **Concept** — explain a domain idea or design principle
- **Guide** — how to accomplish a specific task
- **Tutorial** — step-by-step walkthrough for a new user

If unclear, ask. The type determines the structure of the output.

## Step 1: Grill the content

Before asking anything, map what's ambiguous or missing about the topic. Rank by impact — which gaps, if left unclear, will confuse the reader most?

Ask only about the high-impact ambiguous ones, in order. Skip anything derivable from the codebase.

Ask one question at a time. When a question has clear discrete options, use `AskUserQuestion` — put your recommended option first and append "(Recommended)" to its label. For open-ended questions, ask in plain text and state your recommendation explicitly.

If a question can be answered by exploring the codebase, explore instead of asking.

User can say "wrap up" to stop early.

## Step 2: Write the doc

Confirm the filename with the user. Write to `src/<section>/<name>.md` — place it where it fits best in the existing SUMMARY.md structure.

If this is a new file, add it to `src/SUMMARY.md`. Follow this structure (paths relative to `src/`):

```md
# <Section>

## <Category>

- [Category](section/category.md)
  - [Doc Name](section/category/name.md)
```

If the category is new, create `src/<section>/<category>.md` as an index page with a one-paragraph overview. If the section or `##` category header doesn't exist in SUMMARY.md, create it. Insert new entries in alphabetical order within the category.

## Rules

- Grill first, write second.
- Write for the reader, not the author — assume they don't know the internals.
- No API method signatures here; those belong in api-write docs.
- Include diagrams (mermaid) where structure is easier to show than describe.
