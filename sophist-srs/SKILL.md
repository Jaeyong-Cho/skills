---
name: sophist-srs
description: |
  SRS review skill. Use this to review SRS items, apply inline answers from markdown files, and cascade to create SAD and SIT items.
  Triggers: "sophist-srs", "review SRS", "I answered the SRS items", "check SRS review points", "update SRS", "show SRS pending".
  When called with no specific items — shows all pending SRS review points so the human knows what to answer.
  When called after the human has answered review points inline — applies those answers, marks items reviewed, and creates the corresponding SAD and SIT items.
---

# sophist-srs: Review SRS Items and Cascade to Architecture

**Goal**: Surface all pending SRS review points, apply any inline answers the human has written in the item files, mark answered items as `reviewed`, update AT items if content changed, and cascade by creating corresponding SAD and SIT items.

Read before starting:
- `references/items.md` — item format, states, traceability link conventions
- `references/review-points.md` — how review points work and how answers are indicated
- `.sophist/src/goal.md` — project goal (if it exists); use it as orientation when writing SAD items during cascade

---

## Step 1: Find all draft SRS items

```bash
grep -rl "^\`draft\`" .sophist/src/srs/
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

## Step 5b: Surface and apply AT review points

Find all draft AT items:

```bash
grep -rl "^\`draft\`" .sophist/src/at/
```

For each draft AT item, check if it has a pending `> **Review needed**` blockquote.

**Show pending AT review points** alongside the SRS pending list:

```
## Pending AT Review Points

### AT-005: Login flow — happy path
> Clarify whether the test should verify session token in response body or cookie

### AT-006: Account lockout scenario
> Confirm whether test should use real time delay or a mock clock
```

**Apply answers** the human has written inline using the same pattern as Step 3:
- If blockquote contains `> **Answer**: <text>` — incorporate and remove the blockquote
- If blockquote removed entirely — accept as-is

---

## Step 6: Cascade — create or update SAD and SIT items

For each SRS item newly marked `reviewed`, handle downstream items in two cases:

### Debugger cross-cutting concern

When cascading SRS items to SAD, check whether a debugger SRS item exists:

```bash
grep -rl "#debugger" .sophist/src/srs/ 2>/dev/null
```

If any reviewed SRS item describes behavior that crosses component boundaries (multi-step flows, component interactions), and no debugger SRS item exists, add a note in the report suggesting the human capture one via sophist-curs. The debugger SRS item should specify: debug levels (INFO = component boundary crossings; DEBUG = internal algorithm steps; VERBOSE = fine-grained traces) and output control (`--debug-output-dir <path>` for file output, omit for stdout), both passed as CLI options. Once that SRS item is reviewed, sophist-srs will cascade it into a Debugger SAD component.

### No `→ [SAD-` trace yet — create new items

Create the corresponding SAD and SIT items. Read `references/cascade.md` for templates and the full process.

Key principles:
- Group closely related SRS items into one SAD component when they belong to the same module
- Write the SAD item based on what the reviewed SRS tells you the system must do — the architecture should serve the requirements, not the other way around
- Create a SIT item for each SAD component that interacts with other components
- After creating SAD and SIT, go back to each SRS item and add `→ [SAD-{NNN}](../sad/SAD-{NNN}.md): <why>` to its Traces section

**Design each SAD component as a deep module** (Ousterhout, *A Philosophy of Software Design*):
- A deep module has a **simple interface** that hides a **large, complex implementation**. The interface cost to callers should be far less than the value the component provides.
- **Pull complexity downward**: if a design choice forces callers to understand internal detail, absorb that complexity into the component instead.
- **Prefer general-purpose interfaces**: an interface slightly more general than today's use case is usually simpler, more stable, and serves future requirements without change.
- **Avoid pass-through components**: a component that merely delegates to another without adding its own logic is shallow — merge it or give it real responsibility.
- **Information hiding**: hide data structures, algorithms, storage technology, and external dependencies. Only expose what callers genuinely need to know.

For each new SAD component, ask: *Is the interface simpler than the implementation? Could two adjacent components merge into one deeper one? Does the interface expose any internal detail callers shouldn't need?* If the answer reveals a shallow design, redesign before creating SDD items — shallow interfaces are far cheaper to fix at the architecture layer than after implementation.

### `→ [SAD-` trace already exists — update existing items

Read each linked SAD item and compare it against what the now-reviewed SRS says. If the SRS content changed during Step 3 (a value was corrected, a behavior was clarified, a constraint was added), update the SAD item to stay aligned:

- Revise **Responsibility** if the component's purpose or scope changed
- Revise **Interface** if new methods are implied or signatures changed
- Revise **Dependencies** if new relationships were revealed
- Update the **Diagram** if component relationships changed
- If the SAD item was in `reviewed` state and the changes are substantial, reset it to `` `draft` `` — it needs re-review since the requirement that informed it has changed

Also follow each SAD item's `→ [SIT-` traces and update the linked SIT items if the SRS change affected the integration boundary (scenario, expected behavior, or sequence diagram).

---

## Step 7: Update tags and indexes

- Update `.sophist/src/tags.md` for any new tags used in new SAD or SIT items
- Update `.sophist/src/sad/index.md` traceability table
- Update `.sophist/src/sit/index.md` traceability table
- Update `SUMMARY.md` with new SAD and SIT entries

---

## Step 8: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
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

### Still Pending (answer these inline, then run sophist-srs again)
| ID | Type | Review Question |
|----|------|----------------|
| SRS-008 | SRS | Is lockout duration fixed or configurable? |
| AT-006 | AT | Confirm whether test should use real time delay or mock clock |

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
then run **sophist-sad** to apply answers, mark SAD items reviewed, and generate SDD items.
```

---

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-srs/`) and write:

| File | Contents |
|------|----------|
| `00-draft-items.md` | List of all draft SRS items found, each with status (answered / pending) and the review question text |
| `01-answers-applied.md` | For each answered item: the original question, the human's answer, and what content field was updated |
| `02-sad-cascade.md` | Each SAD and SIT item created or updated — ID, title, which SRS items drove it, and the key design decision made |
| `03-review-points.md` | All items still pending with their unanswered questions |

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
docs(srs): <short description under 72 chars>

Why: <which SRS review points were answered and what requirement decision was made>
What: <which SRS/SAD/SIT/AT items were created or updated>
```

Keep `Why` and `What` to one or two sentences each — enough for someone reading `git log` to understand the change without opening the diff.
