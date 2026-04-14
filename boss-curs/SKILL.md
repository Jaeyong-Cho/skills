---
name: boss-curs
description: |
  Use this skill when the user provides new or changed customer requirements (CuRS) and wants the BOSS documents updated. Triggers: "boss-curs", "update the docs with this requirement", "I have a new requirement", "add this to the spec", "the customer wants X", or any time the user describes what the software should do. AI drafts CuRS → SRS → AT items, marks them draft, and provides review points. No SAD/SDD/test stubs yet — those cascade after SRS review via boss-srs.
---

# boss-update: Capture Customer Input and Draft SRS

**Goal**: Translate customer intent into a CuRS item, derive SRS requirements, and create corresponding AT items. All new items are marked `draft` with review points. SAD and SDD are created later by boss-srs and boss-sad after each layer is reviewed.

Read before starting:
- `references/items.md` — item format, ID system, states, tags, traceability links
- `references/structure.md` — per-document conventions
- `references/review-points.md` — how to write review points

---

## Step 1: Orient — find next IDs and related existing items

### 1a. Next available IDs

```bash
ls book/src/curs/ | grep "^CuRS-[0-9]" | sort -t- -k2 -n | tail -1
ls book/src/srs/  | grep "^SRS-[0-9]"  | sort -t- -k2 -n | tail -1
ls book/src/at/   | grep "^AT-[0-9]"   | sort -t- -k2 -n | tail -1
```

### 1b. Find related existing items

Check for existing coverage to avoid duplicates and find items to link:

```bash
# Does any SRS item already cover this topic?
grep -ril "<keyword>" book/src/srs/

# Does any CuRS item express the same customer need?
grep -ril "<keyword>" book/src/curs/
```

Read the full content of any item that looks relevant. Present matching items to the user before creating new ones — they may want to amend an existing SRS rather than create a new one.

### 1c. Read tag registry

```bash
cat book/src/tags.md
```

---

## Step 2: Write CuRS item(s)

Create `book/src/curs/CuRS-{NNN}.md`. Record the customer's input accurately — do not over-interpret yet.

```markdown
# CuRS-{NNN}: <short title>

## State
`draft`

## Tags
`#tag1` `#tag2`

## Why
<one sentence — what business motivation or customer concern this addresses>

## Traces
- → [SRS-{NNN}](../srs/SRS-{NNN}.md): <which aspect of this customer input is being formalized>

## Input
> "<customer's words verbatim or near-verbatim>"

## Context
<when this was stated and any relevant background>

> **Review needed** — confirm this captures the customer's intent accurately; note any assumptions made
```

Add to `SUMMARY.md` under Customer Requirements and add a row to `book/src/curs/index.md`.

---

## Step 3: Derive SRS items

For each CuRS item, create one or more `book/src/srs/SRS-{NNN}.md` files. Each SRS item must be testable — if you can't imagine an AT for it, split or reframe it.

```markdown
# SRS-{NNN}: <requirement title>

## State
`draft`

## Tags
`#tag1` `#tag2`

## Why
<one sentence — why this requirement exists and what customer need it formalizes>

## Traces
- ← [CuRS-{NNN}](../curs/CuRS-{NNN}.md): <why this is a direct derivation of that customer input, including any added assumptions>
- → [AT-{NNN}](../at/AT-{NNN}.md): <what aspect of this requirement the acceptance test validates>

## Description

<Requirement text. Use "shall" for mandatory, "should" for preferred.>

> **Review needed** — <specific question: scope, ambiguity, or assumption to verify>
```

Add to `SUMMARY.md` under Software Requirements and add a row to `book/src/srs/index.md`.

Note: The `→ SAD` trace is intentionally absent here. boss-srs creates the SAD items and adds that trace after you review the SRS.

---

## Step 4: Write AT items

For each SRS item, create `book/src/at/AT-{NNN}.md`.

```markdown
# AT-{NNN}: <test title>

## State
`draft`

## Tags
`#tag1`

## Why
<one sentence — what requirement behavior this test verifies and why this scenario was chosen>

## Traces
- ← [SRS-{NNN}](../srs/SRS-{NNN}.md): <which "shall" statement this test verifies and why this scenario is sufficient>

## Preconditions
<system state before test>

## Steps
1. <action>
2. <action>

## Expected result
<observable outcome — specific and measurable>

## Failure criterion
<what makes this test fail>

> **Review needed** — <question about test scope or pass criterion>
```

Add to `SUMMARY.md` under Acceptance Tests and add a row to `book/src/at/index.md`.

---

## Step 5: Update tags.md

For every new tag used, add a row to the tag registry and update item counts for affected tags.

```bash
grep -rh "#[a-z]" book/src/curs/ book/src/srs/ book/src/at/ \
  | grep -o "#[a-z-]*" | sort | uniq -c | sort -rn
```

---

## Step 6: Update traceability summaries

Update the traceability tables in `book/src/curs/index.md`, `book/src/srs/index.md`, and `book/src/at/index.md`.

---

## Step 7: Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix all broken links before reporting.

---

## Step 8: Report review points

```
## Items Created

| ID | Title | Type |
|----|-------|------|
| CuRS-003 | ... | new |
| SRS-007  | ... | new |
| AT-005   | ... | new |

## Review Points

### Must Resolve
- [ ] SRS-007: <question — blocks downstream architecture work>

### Should Verify
- [ ] CuRS-003: <assumption made in transcription>

### For Awareness
- [ ] AT-005: <coverage note>

---

Next: Open the SRS and AT files, write your answers inline by removing or updating the
`> **Review needed**` blocks, then run **boss-srs** to apply your answers, mark items
reviewed, and generate the corresponding SAD items.
```

---

## Constraints

- Write no source code and no SAD/SDD items — those belong to the cascade after review.
- SAD items will be created by boss-srs once SRS items are reviewed.
- Every SRS item must be testable. If it isn't, either split it or flag it as a question.
- Use mermaid diagrams in SRS items when a multi-step user flow is involved.
