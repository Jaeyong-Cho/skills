---
name: boss-overview
description: |
  Generate a concise overview of a BOSS-documented project. Triggers: "boss-overview", "show me the project overview", "summarize the project", "what does this project do", "give me an overview of the BOSS docs", "what's in the book", or any request to understand a project's purpose, scope, or current documentation state. Reads all BOSS layers and produces a human-readable summary covering purpose, requirements, architecture, design, and test coverage. Use this skill whenever someone wants a bird's-eye view of a project that has a book/ directory.
---

# boss-overview: Project Overview

**Goal**: Read all BOSS layers and produce a clear, concise overview of the project — what it does, how it is built, and where the documentation currently stands.

---

## Step 1: Read the book structure

```bash
cat book/src/SUMMARY.md
```

This tells you which items exist across all layers.

---

## Step 2: Read key items per layer

Read the index files for each layer to understand traceability and item counts:

```bash
cat book/src/curs/index.md
cat book/src/srs/index.md
cat book/src/sad/index.md
cat book/src/sdd/index.md
cat book/src/at/index.md
cat book/src/sit/index.md
cat book/src/ut/index.md
```

Then read the actual item files (all of them if the project is small; key ones if it's large). Focus especially on:
- All CuRS items (they define the project's purpose)
- Reviewed SRS items (they define what is committed to)
- SAD-001 (it describes the directory structure and overall architecture)

---

## Step 3: Check item states

Count items per state to understand documentation maturity:

```bash
grep -r "^\`draft\`\|^\`review\`\|^\`reviewed\`\|^\`approved\`" book/src/ \
  | sed 's/.*:\`//' | sed 's/\`.*//' | sort | uniq -c
```

---

## Step 4: Produce the overview

Write a structured overview in this format:

---

```
# Project Overview: <project name>

## What it does
<2–4 sentences describing the software from a user's perspective, drawn from the CuRS items>

## Customer requirements (<N> items)
<one bullet per CuRS item: ID · title · state>

## Software requirements (<N> items)
<one bullet per reviewed/approved SRS item; group draft items with a count only>

## Architecture
<paragraph describing the component structure from SAD-001 and other SAD items>
<include a mermaid diagram if the architecture is non-trivial — use <br/> for line breaks inside node labels, not \n>

## Design
<brief paragraph on key design decisions from SDD items, if any are reviewed>

## Test coverage
| Layer | Items | Reviewed | Draft |
|-------|-------|----------|-------|
| AT    |       |          |       |
| SIT   |       |          |       |
| UT    |       |          |       |

## Documentation status
| Layer | Items | Reviewed | Draft |
|-------|-------|----------|-------|
| CuRS  |       |          |       |
| SRS   |       |          |       |
| SAD   |       |          |       |
| SDD   |       |          |       |

## Open review points
<list any unresolved > **Review needed** blocks that are blocking progress, grouped by layer>
Tip: run `grep -r "Review needed" book/src/ | grep -v "^Binary"` to find them.

## Next step
<one clear recommendation: which boss-* skill to run next, and why>
```

---

## Constraints

- Do not modify any files — this is a read-only skill.
- Keep the overview factual and grounded in what the documents say. If something is ambiguous or missing, say so rather than inferring.
- If `book/` does not exist, tell the user to run `boss-init` first.
