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
- `../sophist-shared/workflow.md` — full pipeline order, item states, and which skill to run next
- `../sophist-shared/items.md` — item format, states, traceability link conventions
- `../sophist-shared/review-points.md` — how review points work and how answers are indicated
- `../sophist-shared/philosophy.md` — data structure design philosophy; apply when creating SAD items during cascade
- `.sophist/src/goal.md` — project goal (if it exists); use it as orientation when writing SAD items during cascade

---

## Steps 1–4: Find, surface, apply, and mark items

- **Step 1**: `grep -rl "^\`draft\`" .sophist/src/srs/` — read each draft item and classify as answered (no `### Review needed`, or has `#### Answer`) or pending
- **Step 2**: List every pending item so the human knows what still needs their attention
- **Step 3**: For each answered item — if `#### Answer` present, incorporate into the relevant content field (rewrite the sentence or value the review question was about), then remove the entire `### Review needed` section; if section removed entirely, accept as-is. Rewrite clearly — don't just append.
- **Step 4**: Change `## State` from `` `draft` `` to `` `reviewed` `` for each item with all review points resolved.

---

## Step 5: Update AT items

For each SRS item whose content changed during Step 3, read its linked AT item(s) via the `→ [AT-` trace. Check whether the AT's preconditions, steps, expected result, or failure criterion still match the updated SRS. Update them if they don't. Keep AT state as `draft` — AT items follow their own review cycle when needed.

---

## Step 5b: Surface and apply AT review points

Find all draft AT items:

```bash
grep -rl "^\`draft\`" .sophist/src/at/
```

For each draft AT item, check if it has a pending `### Review needed` section.

**Show pending AT review points** alongside the SRS pending list:

```
## Pending AT Review Points

### AT-005: Login flow — happy path
> Clarify whether the test should verify session token in response body or cookie

### AT-006: Account lockout scenario
> Confirm whether test should use real time delay or a mock clock
```

**Apply answers** the human has written inline using the same pattern as Step 3:
- If section contains `#### Answer` — read it, incorporate it, remove the entire `### Review needed` section
- If section removed entirely — accept as-is

---

## Step 6: Cascade — create or update SAD and SIT items

For each SRS item newly marked `reviewed`, handle downstream items in two cases:

### Debugger cross-cutting concern

When cascading SRS items to SAD, check whether a debugger SRS item exists:

```bash
grep -rl "#debug" .sophist/src/srs/ 2>/dev/null
```

If any reviewed SRS item describes behavior that crosses component boundaries (multi-step flows, component interactions), and no debugger SRS item exists, add a note in the report suggesting the human capture one via sophist-curs. The debugger SRS item should specify:
- Debug levels: `OFF`, `INFO` = component boundary crossings, `DEBUG` = internal algorithm steps, `VERBOSE` = fine-grained traces; passed as `--debug-level` CLI option
- Output control: `--debug-output-dir <path>` writes log file + data files to that directory; omit for stdout-only
- **Data files are written automatically when `--debug-output-dir` is set, regardless of `--debug-level`**
- Subprocess logs are captured to separate files when `--debug-output-dir` is set; the main log records each subprocess log file path and timing
- Write events are logged to the main log with file path, purpose, and write metadata; filename collisions are resolved with a sequence index
- Each SAD component's `## Debug strategy` section must include a data model table (filename, format, when written, purpose, contents)

Once that SRS item is reviewed, sophist-srs will cascade it into a Debugger SAD component.

**Refactoring signal**: Before creating new SAD items, scan existing components for overlap:

```bash
grep -ril "<requirement keyword>" .sophist/src/sad/
```

If two or more existing SAD components already serve the same general Responsibility as the new requirement, automatically invoke **sophist-refact**:

> Rule of Three / before feature: SAD-X and SAD-Y already cover similar ground. Running sophist-refact now to merge or deepen them before adding another component. Shallow SAD components compound downstream — each gets its own shallow SDD layer.

Run the full sophist-refact workflow. When it completes, resume creating SAD items here. The human may say "skip refact" to proceed without refactoring.

### No `→ [SAD-` trace yet — create new items

Before writing the SAD item, apply the data structure design philosophy from `../sophist-shared/philosophy.md`:

- What objects does this requirement operate on? Identify the independent data entities involved.
- What relations exist between those objects?
- What transformation does the required behaviour perform — what comes in, what comes out?

Let these answers shape the component's `## Responsibility` (what objects it owns) and `## Interface` (what objects it receives and produces). If the objects or their relations are unclear, add a `### Review needed` before continuing.

Create the corresponding SAD and SIT items. Read `references/cascade.md` for templates and the full process.

Key principles:
- Group closely related SRS items into one SAD component when they belong to the same module
- Write the SAD item based on what the reviewed SRS tells you the system must do — the architecture should serve the requirements, not the other way around
- Create a SIT item for each SAD component that interacts with other components
- After creating SAD and SIT, go back to each SRS item and add `→ [SAD-{NNN}](../sad/SAD-{NNN}.md): <why>` to its Traces section

**Write `## Debug strategy` for every SAD item created.** Based on the component's Responsibility and Interface, draft:

- **Healthy trace**: the sequence of INFO-level log messages that should appear during a successful operation through this component — component entry, key outbound calls, and return
- **Key observables**: which inputs, outputs, and internal state values are worth capturing in log messages at entry and exit
- **Failure signatures**: what the log output would look like for each failure mode (e.g., "if auth fails, expect `ERROR authenticate: invalid credentials user_id=X` with no session-created line after")
- **Diagnostic process**: one paragraph on how to use the logs to diagnose the most likely failure scenarios for this component
- **Debug data model**: a table for structured data files this component writes via `debugger.write()`:

  | File | Format | When written | Purpose | Contents |
  |------|--------|-------------|---------|----------|

  Leave the table empty (`_none_`) if this component writes no data files. If uncertain, add a `### Review needed` asking the human to confirm what data should be captured.

If a Debugger `#debug` SRS item is being cascaded, its SAD item's `## Debug strategy` describes the Debugger component's own output (main log file format and schema) rather than a data model table.

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
