---
name: sophist-sad
description: |
  SAD review skill. Use this to review SAD items, apply inline answers from markdown files, and cascade to create SDD and UT items.
  Triggers: "sophist-sad", "review SAD", "I answered the SAD items", "check SAD review points", "update SAD", "show SAD pending".
  When called with no specific items — shows all pending SAD review points.
  When called after the human has answered review points inline — applies those answers, marks items reviewed, and creates the corresponding SDD and UT items.
---

# sophist-sad: Review SAD Items and Cascade to Detailed Design

**Goal**: Surface all pending SAD review points, apply any inline answers the human has written in the item files, mark answered items as `reviewed`, update SIT items if content changed, and cascade by creating corresponding SDD and UT items.

Read before starting:
- `references/items.md` — item format, states, traceability link conventions
- `references/review-points.md` — how review points work and how answers are indicated

---

## Step 1: Find all draft SAD items

```bash
grep -rl "^\`draft\`" book/src/sad/
```

Read each draft SAD item file.

For each item, determine its status:

- **Answered**: the `> **Review needed**` blockquote has been removed, or contains `> **Answer**:` text added by the human
- **Pending**: the blockquote exists with only the original question

---

## Step 2: Show pending review points

List every pending SAD item so the human knows what still needs their attention:

```
## Pending SAD Review Points

### SAD-003: AuthService component
> Should AuthService own session creation, or delegate to a separate SessionService?

### SAD-001: Project directory structure
> Confirm file extension and whether a monorepo layout is needed
```

If there are no pending items, note that and move to Step 3.

---

## Step 3: Apply inline answers to answered items

For each answered SAD item:

**If the blockquote contains `> **Answer**: <text>`:**
- Read the answer
- Incorporate it into the relevant content field — update the Interface, Location, Responsibility, Dependencies, or Diagram section as appropriate
- Remove the entire blockquote block

**If the blockquote has been removed entirely:**
- Accept the current file content as the human's approved version
- No content change needed

When incorporating an answer that changes the component's interface or responsibility, also check whether the component diagram (mermaid) needs updating — keep the diagram in sync with the text.

> **Mermaid line breaks**: Use `<br/>` for line breaks inside mermaid node labels — not `\n`. The `\n` character renders literally and will not create a new line.

When an answer reshapes a component's interface, evaluate it against Deep Module principles (Ousterhout, *A Philosophy of Software Design*): does the revised interface hide more complexity than before, or does it leak internal details to callers? If the answer pushes complexity outward (more parameters, more caller knowledge required, narrower purpose), flag a review point asking whether the complexity can be absorbed into the component instead.

---

## Step 4: Mark answered items as `reviewed`

For each item where all review points are resolved:

Change `## State` from `` `draft` `` to `` `reviewed` ``.

---

## Step 5: Update SIT items

For each SAD item whose interface or component boundaries changed during Step 3, read its linked SIT item(s) via the `→ [SIT-` trace. Update the SIT's sequence diagram, components under test, and expected behavior if they no longer reflect the revised interface. Keep SIT state as `draft`.

---

## Step 5b: Surface and apply SIT review points

Find all draft SIT items:

```bash
grep -rl "^\`draft\`" book/src/sit/
```

For each draft SIT item, check if it has a pending `> **Review needed**` blockquote.

**Show pending SIT review points** alongside the SAD pending list:

```
## Pending SIT Review Points

### SIT-002: AuthService ↔ UserRepository interaction
> Confirm whether tests should use a real database or an in-memory stub

### SIT-003: SessionService ↔ RedisAdapter interaction
> Is the Redis connection shared across test cases or freshly initialized each time?
```

**Apply answers** the human has written inline using the same pattern as Step 3:
- If blockquote contains `> **Answer**: <text>` — incorporate into Scenario, Expected behavior, or Diagram, then remove the blockquote
- If blockquote removed entirely — accept as-is

---

## Step 6: Cascade — create or update SDD and UT items

For each SAD item newly marked `reviewed`, handle downstream items in two cases:

### No `→ [SDD-` trace yet (or only a `TBD` placeholder) — create new items

Create the corresponding SDD and UT items. Read `references/cascade.md` for templates and the full process.

Key principles:
- Create one SDD item per function listed in the SAD item's `## Interface` section
- Write the algorithm based on what the SAD component's responsibility and the upstream SRS requirements say — the SDD should be specific enough to implement without guessing
- Create at least one UT item per SDD item; add more for significant error paths and edge cases
- After creating SDD and UT items, go back to each SAD item and replace the `TBD` SAD-to-SDD trace with the real link

**Before creating SDD items, evaluate the SAD component's depth** (Ousterhout, *A Philosophy of Software Design*):
- Count the functions in `## Interface` against the complexity in `## Responsibility`. If the interface is nearly as complex as the responsibility, the component is shallow — it won't pull its weight.
- If two or more interface functions always need to be called together, they likely belong inside the component, not exposed to callers.
- A function whose signature requires callers to understand internal data structures is leaking abstraction — add a review point to simplify before proceeding to SDD.
- The SDD algorithm should be substantially more complex than the function signature. If the algorithm is just one or two obvious steps, the function may be too fine-grained.

### `→ [SDD-` trace already exists — update existing items

Read each linked SDD item and compare it against what the now-reviewed SAD says. If the SAD content changed during Step 3 (interface revised, responsibility narrowed, dependency added), update the SDD item to stay aligned:

- Revise **Signature** if the function's parameters or return type changed
- Revise **Algorithm** if the component's responsibility changed how the function should work
- Revise **Error cases** or **Side effects** if the SAD introduced new constraints
- Update the **Diagram** if the control flow changed
- If the SDD item was in `reviewed` state and the changes are substantial, reset it to `` `draft` `` — it needs re-review since the design that informed it has changed

Also follow each SDD item's `→ [UT-` traces and update the linked UT items if the SDD changes affect inputs, expected outputs, or error paths that those tests cover. If the revised SDD introduces a new error case or behavior path with no existing UT, create one.

---

## Step 7: Update tags and indexes

- Update `book/src/tags.md` for any new tags used in new SDD or UT items
- Update `book/src/sdd/index.md` traceability table
- Update `book/src/ut/index.md` traceability table
- Update `SUMMARY.md` with new SDD and UT entries

---

## Step 8: Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix broken markdown links before reporting.

---

## Step 9: Report

```
## SAD Review Summary

### Promoted to Reviewed
| ID | Title |
|----|-------|
| SAD-003 | AuthService component |

### Still Pending (answer these inline, then run sophist-sad again)
| ID | Type | Review Question |
|----|------|----------------|
| SAD-001 | SAD | Confirm file extension and monorepo layout |
| SIT-002 | SIT | Use real database or in-memory stub? |

### SDD Items Created
| ID | Title | Parent SAD |
|----|-------|-----------|
| SDD-010 | AuthService.authenticate() | SAD-003 |
| SDD-011 | AuthService.checkLockout() | SAD-003 |

### UT Items Created
| ID | Title | Tests |
|----|-------|-------|
| UT-010 | authenticate — happy path | SDD-010 |
| UT-011 | authenticate — wrong password | SDD-010 |
| UT-012 | checkLockout — account locked | SDD-011 |

### SIT Items Updated
| ID | What changed |
|----|-------------|
| SIT-002 | Updated sequence diagram to reflect revised AuthService interface |

---

Next: Open the SDD item files, write your answers to the review points inline,
then run **sophist-sdd** to apply answers, mark SDD items reviewed, and update UT items.
```

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
docs(sad): <short description under 72 chars>

Why: <which SAD review points were answered and what design decision was made>
What: <which SAD/SDD/UT/SIT items were created or updated>
```

Keep `Why` and `What` to one or two sentences each — enough for someone reading `git log` to understand the change without opening the diff.
