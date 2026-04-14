---
name: boss-sdd
description: |
  SDD review skill. Use this to review SDD items, apply inline answers from markdown files, update UT items, and mark SDD items reviewed.
  Triggers: "boss-sdd", "review SDD", "I answered the SDD items", "check SDD review points", "update SDD", "show SDD pending".
  When called with no specific items — shows all pending SDD review points.
  When called after the human has answered review points inline — applies those answers, marks items reviewed, updates UT items, and signals readiness to implement.
---

# boss-sdd: Review SDD Items and Finalize Detailed Design

**Goal**: Surface all pending SDD review points, apply any inline answers the human has written in the item files, mark answered items as `reviewed`, and update corresponding UT items to reflect any changes. When all SDD items are reviewed, the design is ready for implementation.

Read before starting:
- `references/items.md` — item format, states, traceability link conventions
- `references/review-points.md` — how review points work and how answers are indicated

---

## Step 1: Find all draft SDD items

```bash
grep -rl "^\`draft\`" book/src/sdd/
```

Read each draft SDD item file.

For each item, determine its status:

- **Answered**: the `> **Review needed**` blockquote has been removed, or contains `> **Answer**:` text added by the human
- **Pending**: the blockquote exists with only the original question

---

## Step 2: Show pending review points

List every pending SDD item clearly:

```
## Pending SDD Review Points

### SDD-010: AuthService.authenticate()
> Confirm bcrypt cost factor (12) matches your production security policy

### SDD-011: AuthService.checkLockout()
> Is the failure counter stored in memory (reset on restart) or persisted?
```

If there are no pending items, note that and move to Step 3.

---

## Step 3: Apply inline answers to answered items

For each answered SDD item:

**If the blockquote contains `> **Answer**: <text>`:**
- Read the answer
- Incorporate it into the relevant field — Signature, Algorithm, Variables, Error cases, or Side effects
- Remove the entire blockquote block

**If the blockquote has been removed entirely:**
- Accept the current file content as the human's approved version

When an answer changes an algorithm step, rewrite that specific step clearly. When it changes an error case or side effect, update those sections. Keep the algorithm numbered and concrete — the SDD must remain implementable without guessing after your edits.

If an answer reveals that the algorithm is more complex than first written (e.g., the human says "the counter is persisted, not in-memory"), update the algorithm steps, variables, and side effects to reflect that accurately.

---

## Step 4: Mark answered items as `reviewed`

For each item where all review points are resolved:

Change `## State` from `` `draft` `` to `` `reviewed` ``.

---

## Step 5: Update UT items

For each SDD item whose algorithm, error cases, or signature changed during Step 3, read its linked UT item(s) via the `→ [UT-` trace.

Check whether existing UT items:
- Still test the right function with the right signature
- Cover error cases that were added or changed
- Have input/output values that match the revised algorithm

Update UT items that are now misaligned. If a new error case or behavior was added that has no UT item yet, create one using the UT template from `references/items.md` (see the UT item format in the SDD-specific section).

Keep UT state as `draft` — they follow their own review if needed.

---

## Step 5b: Surface and apply UT review points

Find all draft UT items:

```bash
grep -rl "^\`draft\`" book/src/ut/
```

For each draft UT item, check if it has a pending `> **Review needed**` blockquote.

**Show pending UT review points** alongside the SDD pending list:

```
## Pending UT Review Points

### UT-010: authenticate — happy path
> Confirm expected session token format (JWT string vs object with exp field)

### UT-012: checkLockout — account locked
> Should this test mock the current time or use a fixed counter threshold?
```

**Apply answers** the human has written inline using the same pattern as Step 3:
- If blockquote contains `> **Answer**: <text>` — incorporate into Case, Input, or Expected output, then remove the blockquote
- If blockquote removed entirely — accept as-is

---

## Step 6: Update indexes and tags

- Update `book/src/sdd/index.md` traceability table for any state changes
- Update `book/src/ut/index.md` if new UT items were added
- Update `book/src/tags.md` if new tags were used
- Update `SUMMARY.md` if new UT items were created

---

## Step 7: Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix broken links before reporting.

---

## Step 8: Report

```
## SDD Review Summary

### Promoted to Reviewed
| ID | Title |
|----|-------|
| SDD-010 | AuthService.authenticate() |
| SDD-011 | AuthService.checkLockout() |

### Still Pending (answer these inline, then run boss-sdd again)
| ID | Type | Review Question |
|----|------|----------------|
| SDD-012 | SDD | Which session store adapter is used — Redis or in-process? |
| UT-010 | UT | Confirm expected session token format |

### UT Items Updated
| ID | What changed |
|----|-------------|
| UT-010 | Updated expected output to match revised error type name |

### UT Items Created
| ID | Title | Tests |
|----|-------|-------|
| UT-013 | checkLockout — counter persisted across restarts | SDD-011 |

---

## Ready to Implement

All SDD items are reviewed. Implement the functions described in the SDD items, following
the signatures and algorithm steps exactly. When done, run **boss-codereview** to verify
your implementation against the reviewed design.
```

Only show the "Ready to Implement" section if all SDD items linked from reviewed SAD items are now in `reviewed` state. If some are still `draft`, omit it and note which items remain.
