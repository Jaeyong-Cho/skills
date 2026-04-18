---
name: sophist-curs
description: |
  Use this skill when the user provides new or changed customer requirements (CuRS) and wants the SOPHIST documents updated. Triggers: "sophist-curs", "update the docs with this requirement", "I have a new requirement", "add this to the spec", "the customer wants X", or any time the user describes what the software should do. AI drafts CuRS → SRS → AT items, marks them draft, and provides review points. No SAD/SDD/test stubs yet — those cascade after SRS review via sophist-srs.
---

# sophist-update: Capture Customer Input and Draft SRS

**Goal**: Translate customer intent into a CuRS item, derive SRS requirements, and create corresponding AT items. All new items are marked `draft` with review points. SAD and SDD are created later by sophist-srs and sophist-sad after each layer is reviewed.

Read before starting:
- `references/items.md` — item format, ID system, states, tags, traceability links
- `references/structure.md` — per-document conventions
- `references/review-points.md` — how to write review points

---

## Step 1: Orient — find next IDs and assess existing coverage

### 1a. Next available IDs

```bash
ls .sophist/src/curs/ | grep "^CuRS-[0-9]" | sort -t- -k2 -n | tail -1
ls .sophist/src/srs/  | grep "^SRS-[0-9]"  | sort -t- -k2 -n | tail -1
ls .sophist/src/at/   | grep "^AT-[0-9]"   | sort -t- -k2 -n | tail -1
```

### 1b. Similarity analysis

Before writing anything, understand what's already in the book. Search with several keyword angles — the user's exact words, synonyms, the feature area, and the actor/system involved:

```bash
grep -ril "<keyword1>" .sophist/src/curs/ .sophist/src/srs/
grep -ril "<keyword2>" .sophist/src/curs/ .sophist/src/srs/
```

Read the full content of every match. For each distinct concept in the user's input, classify the coverage:

| Coverage | Meaning | Action |
|----------|---------|--------|
| **Full duplicate** | An existing CuRS+SRS already captures this intent completely | **SKIP** — no new item needed; mention the existing ID |
| **Partial overlap** | An existing item covers part of it, or it extends/clarifies the existing one | **ENHANCE** — add a section or broaden the existing item's scope |
| **Changed intent** | The customer is explicitly revising a prior requirement | **UPDATE** — modify the existing item to reflect the new intent |
| **New territory** | No existing item covers this need | **NEW** — create a full CuRS → SRS → AT chain |

Present your coverage analysis to the user in a compact table before making any changes:

```
| Concept | Closest match | Coverage | Planned action |
|---------|--------------|----------|----------------|
| X       | CuRS-002     | partial  | ENHANCE CuRS-002 + SRS-004 |
| Y       | —            | none     | NEW CuRS-005 |
| Z       | CuRS-001     | full     | SKIP |
```

If any planned action is SKIP, explain briefly why the existing item already covers it. If UPDATE or ENHANCE, quote the relevant part of the existing item so the user can see the diff before you make it.

Proceed with changes only after presenting this table. If the user overrides an action (e.g., wants NEW instead of ENHANCE), follow their call.

### 1c. Read tag registry

```bash
cat .sophist/src/tags.md
```

---

## Step 2: Execute planned actions

Work through each concept according to the action decided in Step 1b.

### NEW — Write CuRS item(s)

Create `.sophist/src/curs/CuRS-{NNN}.md`. Record the customer's input accurately — do not over-interpret yet.

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

Add to `SUMMARY.md` under Customer Requirements and add a row to `.sophist/src/curs/index.md`.

### UPDATE — Revise an existing CuRS item

When the customer is explicitly changing a prior requirement, edit the existing `CuRS-{NNN}.md`:

1. Change `State` to `draft` if it was `reviewed`
2. Append the new customer input to the `## Input` section (keep the original — the history matters):
   ```markdown
   > "<original input>"

   **Updated {date}:** "<new customer words>"
   ```
3. Revise `## Why` and `## Context` if the motivation or scope changed
4. Add a new review point noting what changed and what downstream items (SRS, AT) may need revisiting
5. Follow the same UPDATE path for any SRS items that trace to this CuRS

### ENHANCE — Extend an existing CuRS item

When the customer input adds scope to something already captured (not a contradiction, just more detail):

1. Keep `State` unchanged unless you're adding something structurally new
2. Add a `## Additions` section (or append to `## Context`) with the new detail
3. If the new scope warrants a new SRS item, create it and add a trace from the existing CuRS
4. If the new scope fits within an existing SRS item, update that SRS item instead

### SKIP — No changes needed

When an existing item already covers the intent, don't create anything. Just note the relevant IDs in the report so the user knows the input was heard and is already tracked.

---

## Step 3: Derive SRS items

For each CuRS item, create one or more `.sophist/src/srs/SRS-{NNN}.md` files. Each SRS item must be testable — if you can't imagine an AT for it, split or reframe it.

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

Add to `SUMMARY.md` under Software Requirements and add a row to `.sophist/src/srs/index.md`.

Note: The `→ SAD` trace is intentionally absent here. sophist-srs creates the SAD items and adds that trace after you review the SRS.

---

## Step 4: Write AT items

For each SRS item, create `.sophist/src/at/AT-{NNN}.md`.

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

Add to `SUMMARY.md` under Acceptance Tests and add a row to `.sophist/src/at/index.md`.

---

## Step 5: Update tags.md

For every new tag used, add a row to the tag registry and update item counts for affected tags.

```bash
grep -rh "#[a-z]" .sophist/src/curs/ .sophist/src/srs/ .sophist/src/at/ \
  | grep -o "#[a-z-]*" | sort | uniq -c | sort -rn
```

---

## Step 6: Update traceability summaries

Update the traceability tables in `.sophist/src/curs/index.md`, `.sophist/src/srs/index.md`, and `.sophist/src/at/index.md`.

---

## Step 7: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
```

Fix all broken links before reporting.

---

## Step 8: Report review points

```
## Changes Summary

| ID | Title | Action | Reason |
|----|-------|--------|--------|
| CuRS-003 | ... | new     | no existing coverage |
| SRS-007  | ... | new     | derived from CuRS-003 |
| CuRS-001 | ... | enhance | user input adds scope to login flow |
| SRS-002  | ... | update  | revised timeout requirement |
| CuRS-002 | ... | skip    | already fully covered (user input rephrased same need) |

## Review Points

### Must Resolve
- [ ] SRS-007: <question — blocks downstream architecture work>

### Should Verify
- [ ] CuRS-003: <assumption made in transcription>

### For Awareness
- [ ] AT-005: <coverage note>

---

Next: Open the SRS and AT files, write your answers inline by removing or updating the
`> **Review needed**` blocks, then run **sophist-srs** to apply your answers, mark items
reviewed, and generate the corresponding SAD items.
```

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
docs(curs): <short description under 72 chars>

Why: <what triggered this change — the new or changed customer requirement>
What: <which CuRS/SRS items were created or updated>
```

Keep `Why` and `What` to one or two sentences each — enough for someone reading `git log` to understand the change without opening the diff.

---

## Constraints

- Write no source code and no SAD/SDD items — those belong to the cascade after review.
- SAD items will be created by sophist-srs once SRS items are reviewed.
- Every SRS item must be testable. If it isn't, either split it or flag it as a question.
- Use mermaid diagrams in SRS items when a multi-step user flow is involved. Use `<br/>` for line breaks — not `\n`. Quote labels containing `[`, `]`, `(`, `)`, or `:` using `["..."]` syntax.
