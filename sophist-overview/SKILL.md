---
name: sophist-overview
description: |
  Generate a concise overview of a SOPHIST-documented project. Triggers: "sophist-overview", "show me the project overview", "summarize the project", "what does this project do", "give me an overview of the SOPHIST docs", "what's in the book", or any request to understand a project's purpose, scope, or current documentation state. Reads all SOPHIST layers and produces a human-readable summary covering purpose, requirements, architecture, design, and test coverage. Use this skill whenever someone wants a bird's-eye view of a project that has a .sophist/ directory.
---

# sophist-overview: Project Overview

**Goal**: Read all SOPHIST layers and produce a clear, concise overview of the project — what it does, how it is built, and where the documentation currently stands.

---

## Step 1: Read the project goal and book structure

```bash
cat .sophist/src/goal.md 2>/dev/null
cat .sophist/src/SUMMARY.md
```

If `goal.md` exists, read it first — it provides the stated purpose of the project and anchors everything else in the overview.

This tells you which items exist across all layers.

---

## Step 2: Read key items per layer

Read the index files for each layer to understand traceability and item counts:

```bash
cat .sophist/src/curs/index.md
cat .sophist/src/srs/index.md
cat .sophist/src/sad/index.md
cat .sophist/src/sdd/index.md
cat .sophist/src/at/index.md
cat .sophist/src/sit/index.md
cat .sophist/src/ut/index.md
```

Then read the actual item files (all of them if the project is small; key ones if it's large). Focus especially on:
- All CuRS items (they define the project's purpose)
- Reviewed SRS items (they define what is committed to)
- SAD-001 (it describes the directory structure and overall architecture)

---

## Step 3: Check item states

Count items per state to understand documentation maturity:

```bash
grep -r "^\`draft\`\|^\`reviewed\`\|^\`done\`\|^\`deprecated\`" .sophist/src/ \
  | sed 's/.*:\`//' | sed 's/\`.*//' | sort | uniq -c
```

---

## Step 4: Produce the overview

Write a structured overview in this format:

---

```
# Project Overview: <project name>

## Goal
<contents of goal.md verbatim, or "No goal set — run sophist-goal to define one." if the file is missing>

## What it does
<2–4 sentences describing the software from a user's perspective, drawn from the CuRS items>

## Customer requirements (<N> items)
<one bullet per CuRS item: ID · title · state>

## Software requirements (<N> items)
<one bullet per reviewed SRS item; group draft items with a count only>

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
Tip: run `grep -r "Review needed" .sophist/src/ | grep -v "^Binary"` to find them.

## Next step
<one clear recommendation: which sophist-* skill to run next, and why>
```

---

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-overview/`) and write:

| File | Contents |
|------|----------|
| `00-coverage.md` | Item counts per layer and state (draft / reviewed / done / deprecated) — the raw data behind the overview tables |
| `01-gaps.md` | Traceability gaps found: items missing upstream or downstream traces, layers with no items yet, review points blocking progress |

---

## Constraints

- Do not modify any files — this is a read-only skill.
- Keep the overview factual and grounded in what the documents say. If something is ambiguous or missing, say so rather than inferring.
- If `.sophist/` does not exist, tell the user to run `sophist-init` first.
