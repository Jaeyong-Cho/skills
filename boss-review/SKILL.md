---
name: boss-review
description: |
  Use this skill after the human has reviewed draft items and wants to promote their state, or when checking traceability consistency across documents. Triggers: "I reviewed the items", "mark SRS-007 as reviewed", "check traceability", "promote these items", "boss review". AI does not judge content correctness — it processes state promotions requested by the human and validates structural consistency.
---

# boss-review: Process Review and Validate Consistency

**Goal**: Find items with inline review marks, apply the human's answers to those items, promote states as directed, and surface traceability inconsistencies. AI does not judge content correctness — that is the human's responsibility.

Read before starting:
- `references/items.md` — item states, traceability link format
- `references/review-points.md` — review checklist per document layer

---

## Step 1: Find items with review marks

Do NOT read all document files. Use grep to find only the items that need attention:

```bash
# Find all items with pending review marks
grep -rl "Review needed" book/src/

# Find all draft items
grep -rl "^\`draft\`" book/src/
```

Read **only** the specific item files returned by these searches. Do not read anything else.

---

## Step 2: Apply the human's answers to review marks

The human will have provided answers in the conversation — either:
- Inline answers written directly into the item file (the blockquote is already gone or modified)
- Answers stated in their message (e.g. "unlock is manual", "threshold is 3 not 5")

For each item file that still has a `> **Review needed**` block:

1. Read the full item file
2. Extract the question(s) from the blockquote
3. If the human has answered the question in the conversation:
   - Update the item content to reflect the answer (e.g. change the threshold value)
   - Remove the `> **Review needed**` blockquote
4. If the human has NOT answered the question yet, present the question clearly and wait for their answer before modifying the file

Format open questions as:

```
### SRS-007 — Needs Your Answer

> verify lockout threshold (5 attempts) and whether unlock is automatic or manual

**What AI found**: The threshold value "5" is not derived from any CuRS item — it was an AI assumption. SDD-003 has no configurable unlock behavior.
**Decision needed from you**: What is the correct threshold? Is unlock time-based or admin-initiated?
```

Rules:
- Apply all answers the human has already provided — do not re-ask resolved questions
- If the answer conflicts with another item, flag the conflict before updating
- If multiple questions exist in one block, handle each separately
- Never skip a `> **Review needed**` block

---

## Step 3: Process state promotions

The human specifies which items to promote. Accept any of these forms:
- `"mark SRS-007 as reviewed"`
- `"SRS-007, SAD-003, SDD-010 → reviewed"`
- `"all draft SRS items are reviewed"`

For each promoted item:
1. Change the content under `## State` from `` `draft` `` to `` `reviewed` ``
2. Remove the `> **Review needed**` blockquote block for that item
3. Do not change any other content

**Rule**: AI never promotes items on its own. Only process promotions explicitly requested by the human.

---

## Step 4: Validate traceability

Check every item file's `## Traces` section for these structural rules:

### 4a. Link validity

Every link target must resolve to an existing file.

```bash
# Find all trace links in SAD items and verify the referenced SRS files exist
grep -rh "\[SRS-" book/src/sad/ | grep -o "SRS-[0-9]*" | sort | uniq | while read id; do
  test -f "book/src/srs/${id}.md" && echo "OK: ${id}" || echo "MISSING: ${id}"
done

# Same for SDD → SAD references
grep -rh "\[SAD-" book/src/sdd/ | grep -o "SAD-[0-9]*" | sort | uniq | while read id; do
  test -f "book/src/sad/${id}.md" && echo "OK: ${id}" || echo "MISSING: ${id}"
done
```

### 4b. Symmetry check

If item A traces → B, then B should trace ← A.

Check pairs:
- CuRS → SRS: each CuRS item should have at least one SRS tracing back to it
- SRS → SAD: each SRS item should trace to at least one SAD item
- SRS → AT: each reviewed SRS item should have at least one AT
- SAD → SDD: each SAD item (other than directory structure) should trace to SDD items
- SAD → SIT: each SAD item with an interface should trace to a SIT
- SDD → UT: each SDD item should trace to at least one UT

```bash
# Example: check which SRS items are referenced by any SAD item
grep -rh "\[SRS-" book/src/sad/ | grep -o "SRS-[0-9]*" | sort | uniq
# Compare against all SRS files:
ls book/src/srs/ | grep "^SRS-"
```

Report any missing or broken traces without silently fixing them.

### 4c. Orphan detection

```bash
# SRS items with no upstream CuRS trace
for f in book/src/srs/SRS-*.md; do
  grep -q "← \[CuRS-" "$f" || echo "ORPHAN (no CuRS): $f"
done

# SDD items with no upstream SAD trace
for f in book/src/sdd/SDD-*.md; do
  grep -q "← \[SAD-" "$f" || echo "ORPHAN (no SAD): $f"
done
```

Report orphans for human decision — do not delete or add traces without instruction.

---

## Step 5: Check reviewed-items readiness

For any item the human is promoting to `reviewed`, verify the review checklist from `references/review-points.md` is addressable. Also check that the `> **Review needed**` blockquote has been removed by the human before promoting — if it is still present, ask whether the question has been resolved.

- SRS: Is the requirement testable? Is AT linked?
- SAD: Is file path specified? Is interface defined?
- SDD: Is signature complete? Is algorithm step-by-step?
- Tests: Is pass/fail criterion objective?

If a mandatory field is missing, flag it and ask before promoting.

---

## Step 6: Update index traceability tables

After processing promotions, update the traceability summary table in each affected `index.md`. Links point directly to item files:

```markdown
## Traceability Summary

| SRS | ← CuRS | → SAD | → AT |
|-----|--------|-------|------|
| [SRS-001](./SRS-001.md) | [CuRS-001](../curs/CuRS-001.md) | [SAD-001](../sad/SAD-001.md) | [AT-001](../at/AT-001.md) |
| [SRS-002](./SRS-002.md) | [CuRS-001](../curs/CuRS-001.md) | [SAD-002](../sad/SAD-002.md) | [AT-002](../at/AT-002.md) |
```

---

## Step 7: Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix broken markdown links or build errors before reporting.

---

## Step 8: Report

```
## State Changes

| ID | Old State | New State |
|----|-----------|-----------|
| SRS-007 | draft | reviewed |
| SAD-003 | draft | reviewed |
| SDD-010 | draft | reviewed |

## Traceability Issues Found

### Broken Links
- SAD-003 traces → SDD-011, but SDD-011 does not exist

### Missing Traces (should verify)
- SRS-008 has no AT item yet

### Orphans
- UT-005 traces ← SDD-009, but SDD-009 has no → UT-005 trace

## All Items Status

| Type | Total | Draft | Reviewed | Done |
|------|-------|-------|----------|------|
| CuRS | 3  | 0 | 3 | 0 |
| SRS  | 7  | 1 | 6 | 0 |
| SAD  | 5  | 1 | 4 | 0 |
| SDD  | 12 | 2 | 10 | 0 |
| AT   | 7  | 1 | 6 | 0 |
| SIT  | 5  | 0 | 5 | 0 |
| UT   | 12 | 2 | 10 | 0 |
```

---

## Constraints

- **Never change item content.** Only state and DRAFT flag removal.
- **Never promote without explicit human instruction.**
- **Report traceability issues; do not silently fix them.** Gaps in traceability are design decisions — the human must decide.
