---
name: sophist-sdd
description: |
  SDD review skill. Use this to review SDD items, apply inline answers from markdown files, update UT items, and mark SDD items reviewed.
  Triggers: "sophist-sdd", "review SDD", "I answered the SDD items", "check SDD review points", "update SDD", "show SDD pending".
  When called with no specific items — shows all pending SDD review points.
  When called after the human has answered review points inline — applies those answers, marks items reviewed, updates UT items, and signals readiness to implement.
---

# sophist-sdd: Review SDD Items and Finalize Detailed Design

**Goal**: Surface all pending SDD review points, apply any inline answers the human has written in the item files, mark answered items as `reviewed`, and update corresponding UT items to reflect any changes. When all SDD items are reviewed, the design is ready for implementation.

Read before starting:
- `references/items.md` — item format, states, traceability link conventions
- `references/review-points.md` — how review points work and how answers are indicated
- `.sophist/src/goal.md` — project goal (if it exists); use it for orientation when finalizing design decisions

---

## Step 1: Find all draft SDD items

```bash
grep -rl "^\`draft\`" .sophist/src/sdd/
```

Read each draft SDD item file.

For each item, determine its status:

- **Answered**: the `### Review needed` section has been removed, or it contains a `#### Answer` subsection added by the human
- **Pending**: the `### Review needed` header is present with only the original question — no `#### Answer` subsection yet

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

**If the section contains a `#### Answer` subsection:**
- Read the content under `#### Answer`
- Incorporate it into the relevant field — Signature, Algorithm, Variables, Error cases, or Side effects
- Remove the entire `### Review needed` section (including the `#### Answer` subsection)

**If the section has been removed entirely:**
- Accept the current file content as the human's approved version

When an answer changes an algorithm step, rewrite that specific step clearly. When it changes an error case or side effect, update those sections. Keep the algorithm numbered and concrete — the SDD must remain implementable without guessing after your edits.

If an answer reveals that the algorithm is more complex than first written (e.g., the human says "the counter is persisted, not in-memory"), update the algorithm steps, variables, and side effects to reflect that accurately.

---

**Refactoring signal**: After applying answers, scan the full SDD item list for repeated algorithm patterns:

```bash
grep -rl "^\`draft\`\|^\`reviewed\`" .sophist/src/sdd/ | sort
```

If two or more other SDD items share the same core structure as an item just answered — same multi-step flow, same variable names, same error cases — flag the Rule of Three:

> Repeated algorithm pattern detected across SDD-X, SDD-Y, and SDD-Z. Consider running **sophist-refact** to consolidate into a shared module. Three identical algorithm implementations mean three places to maintain and three places to introduce bugs.

This is a signal, not a blocker. Continue marking items reviewed.

---

## Step 4: Mark answered items as `reviewed`

For each item where all review points are resolved:

Change `## State` from `` `draft` `` to `` `reviewed` ``.

---

## Step 4b: Debugger SDD items

If any of the answered SDD items belong to a Debugger SAD component (tagged `#debugger`), the SDD items define the concrete Debugger implementation. Treat them exactly like any other SDD item — the `## Signature` defines what callers call; the `## Algorithm` describes how each method works. Make them specific enough to implement without guessing.

The Debugger SDD items must cover:
- Log methods (`info`, `debug`, `verbose`, `warning`, `error`) — algorithm routes to file or stdout based on `--debug-level` and whether `--debug-output-dir` is set
- `write(filename, data, purpose)` — algorithm: (1) no-op if `--debug-output-dir` unset; (2) resolve filename collision by appending sequence index (`-1`, `-2`, …) before extension if file exists; (3) write data inferred by extension; (4) log path+purpose+write event to main log. Active when `--debug-output-dir` is set regardless of `--debug-level`.
- `subprocess_log_path(name)` — returns a unique timestamped path inside `--debug-output-dir` for subprocess stdout/stderr; returns `None` when dir unset. Caller logs the returned path and start time to the main log before launching, and exit code + duration after.
- CLI option parsing for `--debug-level` and `--debug-output-dir`

The `## Debug trace` for `write()` and `subprocess_log_path()` should include the data model table for their own output (what the Debugger itself writes) and the analysis guide for interpreting the main log's write-event entries.

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
grep -rl "^\`draft\`" .sophist/src/ut/
```

For each draft UT item, check if it has a pending `### Review needed` section.

**Show pending UT review points** alongside the SDD pending list:

```
## Pending UT Review Points

### UT-010: authenticate — happy path
> Confirm expected session token format (JWT string vs object with exp field)

### UT-012: checkLockout — account locked
> Should this test mock the current time or use a fixed counter threshold?
```

**Apply answers** the human has written inline using the same pattern as Step 3:
- If section contains `#### Answer` — read it, incorporate into Case, Input, or Expected output, remove the entire `### Review needed` section
- If section removed entirely — accept as-is

---

## Step 6: Update indexes and tags

- Update `.sophist/src/sdd/index.md` traceability table for any state changes
- Update `.sophist/src/ut/index.md` if new UT items were added
- Update `.sophist/src/tags.md` if new tags were used
- Update `SUMMARY.md` if new UT items were created

---

## Step 7: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
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

### Still Pending (answer these inline, then run sophist-sdd again)
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
the signatures and algorithm steps exactly. When done, run **sophist-codereview** to verify
your implementation against the reviewed design.
```

Only show the "Ready to Implement" section if all SDD items linked from reviewed SAD items are now in `reviewed` state. If some are still `draft`, omit it and note which items remain.

---

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-sdd/`) and write:

| File | Contents |
|------|----------|
| `00-draft-items.md` | List of all draft SDD items found, each with status (answered / pending) and the review question text |
| `01-answers-applied.md` | For each answered item: the original question, the human's answer, and which SDD field was updated (Signature / Algorithm / Variables / Error cases / Side effects) |
| `02-ut-updates.md` | Each UT item updated or created — what changed and why (which SDD algorithm change drove it) |
| `03-review-points.md` | All items still pending with their unanswered questions |

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
docs(sdd): <short description under 72 chars>

Why: <which SDD review points were answered and what detailed design decision was made>
What: <which SDD/UT items were updated or created>
```

Keep `Why` and `What` to one or two sentences each — enough for someone reading `git log` to understand the change without opening the diff.
