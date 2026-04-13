---
name: boss-srs
description: |
  SRS review skill. Use this to review SRS items, apply inline answers from markdown files, and cascade to create SAD and SIT items.
  Triggers: "boss-srs", "review SRS", "I answered the SRS items", "check SRS review points", "update SRS", "show SRS pending".
  When called with no specific items — shows all pending SRS review points so the human knows what to answer.
  When called after the human has answered review points inline — applies those answers, marks items reviewed, and creates the corresponding SAD and SIT items.
---

# boss-srs: Review SRS Items and Cascade to Architecture

**Goal**: Surface all pending SRS review points, apply any inline answers the human has written in the item files, mark answered items as `reviewed`, update AT items if content changed, and cascade by creating corresponding SAD and SIT items.

Read before starting:
- `references/items.md` — item format, states, traceability link conventions
- `references/review-points.md` — how review points work and how answers are indicated

---

## Step 1: Find all draft SRS items

```bash
grep -rl "^\`draft\`" book/src/srs/
```

Read each draft SRS item file.

For each item, determine its status:

- **Answered**: the `> **Review needed**` blockquote has been removed, or the blockquote now contains `> **Answer**:` text added by the human
- **Pending**: the blockquote exists with only the original question — no answer yet

---

## Step 2: Show pending review points

List every pending SRS item clearly so the human knows what still needs their attention:

```
## Pending SRS Review Points

### SRS-007: User authentication via email and password
> verify lockout threshold (5 attempts) and whether unlock is automatic or manual

### SRS-008: Account lockout policy
> Is lockout duration fixed (30 minutes) or configurable?
```

If there are no pending items, note that and move to Step 3.

---

## Step 3: Apply inline answers to answered items

For each answered SRS item:

**If the blockquote contains `> **Answer**: <text>`:**
- Read the answer
- Incorporate it into the relevant content field — rewrite the sentence or value that the review question was about
- Remove the entire blockquote block (both question and answer lines)

**If the blockquote has been removed entirely:**
- Accept the current file content as the human's approved version
- No content change needed — the human has already edited the item directly

After applying an answer, the item file should have no remaining `> **Review needed**` block. If there were multiple questions in one block, address each separately; if some are answered and some aren't, update what's answered and rewrite the remaining questions as a fresh blockquote.

The goal is that each item accurately reflects the human's intent. Rewrite clearly — don't just append.

---

## Step 4: Mark answered items as `reviewed`

For each item where all review points are now resolved:

Change `## State` from `` `draft` `` to `` `reviewed` ``.

---

## Step 5: Update AT items

For each SRS item whose content changed during Step 3, read its linked AT item(s) via the `→ [AT-` trace. Check whether the AT's preconditions, steps, expected result, or failure criterion still match the updated SRS. Update them if they don't. Keep AT state as `draft` — AT items follow their own review cycle when needed.

---

## Step 6: Cascade — create SAD and SIT items

For each SRS item newly marked `reviewed` that has no `→ [SAD-` trace yet, create the corresponding architectural items.

Read `references/cascade.md` for the SAD and SIT item templates and the full process.

Key principles:
- Group closely related SRS items into one SAD component when they belong to the same module
- Write the SAD item based on what the reviewed SRS tells you the system must do — the architecture should serve the requirements, not the other way around
- Create a SIT item for each SAD component that interacts with other components
- After creating SAD and SIT, go back to each SRS item and add `→ [SAD-{NNN}](../sad/SAD-{NNN}.md): <why>` to its Traces section

---

## Step 7: Update tags and indexes

- Update `book/src/tags.md` for any new tags used in new SAD or SIT items
- Update `book/src/sad/index.md` traceability table
- Update `book/src/sit/index.md` traceability table
- Update `SUMMARY.md` with new SAD and SIT entries

---

## Step 8: Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix broken markdown links before reporting.

---

## Step 9: Report

```
## SRS Review Summary

### Promoted to Reviewed
| ID | Title |
|----|-------|
| SRS-007 | ... |

### Still Pending (answer these inline, then run boss-srs again)
| ID | Review Question |
|----|----------------|
| SRS-008 | Is lockout duration fixed or configurable? |

### SAD Items Created
| ID | Title | Traces from SRS |
|----|-------|-----------------|
| SAD-003 | AuthService component | SRS-007, SRS-008 |

### SIT Items Created
| ID | Title |
|----|-------|
| SIT-002 | AuthService ↔ UserRepository interaction |

### AT Items Updated
| ID | What changed |
|----|-------------|
| AT-005 | Updated expected result to match revised lockout threshold |

---

Next: Open the SAD item files, write your answers to the review points inline,
then run **boss-sad** to apply answers, mark SAD items reviewed, and generate SDD items.
```
