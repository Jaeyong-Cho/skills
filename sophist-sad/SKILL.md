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
- `../sophist-shared/items.md` — item format, states, traceability link conventions
- `../sophist-shared/review-points.md` — how review points work and how answers are indicated
- `.sophist/src/goal.md` — project goal (if it exists); use it as orientation when writing SDD items during cascade

---

## Steps 1–4: Find, surface, apply, and mark items

- **Step 1**: `grep -rl "^\`draft\`" .sophist/src/sad/` — read each draft item and classify as answered or pending
- **Step 2**: List every pending item so the human knows what still needs their attention
- **Step 3**: For each answered item — incorporate `#### Answer` content into Interface, Location, Responsibility, Dependencies, or Diagram; remove the entire `### Review needed` section; accept removed sections as-is.
  - When an answer changes the component interface or responsibility, also update the mermaid diagram to stay in sync.
  - **Mermaid syntax safety**: Use `<br/>` for line breaks (not `\n`). Quote any label containing `[`, `]`, `(`, `)`, `{`, `}`, or `:` using `["..."]` — bare brackets break the parser.
  - When an answer reshapes a component's interface, evaluate it against Deep Module principles (Ousterhout): does the revised interface hide more complexity, or does it leak internal details to callers? If it pushes complexity outward, flag a review point asking whether the component can absorb that complexity instead.
- **Step 4**: Change `## State` from `` `draft` `` to `` `reviewed` `` for each item with all review points resolved.

---

## Step 5: Update SIT items

For each SAD item whose interface or component boundaries changed during Step 3, read its linked SIT item(s) via the `→ [SIT-` trace. Update the SIT's sequence diagram, components under test, and expected behavior if they no longer reflect the revised interface. Keep SIT state as `draft`.

---

## Step 5b: Surface and apply SIT review points

Find all draft SIT items:

```bash
grep -rl "^\`draft\`" .sophist/src/sit/
```

For each draft SIT item, check if it has a pending `### Review needed` section.

**Show pending SIT review points** alongside the SAD pending list:

```
## Pending SIT Review Points

### SIT-002: AuthService ↔ UserRepository interaction
> Confirm whether tests should use a real database or an in-memory stub

### SIT-003: SessionService ↔ RedisAdapter interaction
> Is the Redis connection shared across test cases or freshly initialized each time?
```

**Apply answers** the human has written inline using the same pattern as Step 3:
- If section contains `#### Answer` — read it, incorporate into Scenario, Expected behavior, or Diagram, remove the entire `### Review needed` section
- If section removed entirely — accept as-is

---

## Step 6: Cascade — create or update SDD and UT items

For each SAD item newly marked `reviewed`, handle downstream items in two cases:

### Debugger cross-cutting concern

Before cascading to SDD, check whether a Debugger SAD item exists:

```bash
grep -rl "#debug" .sophist/src/sad/ 2>/dev/null
```

If one or more of the reviewed SAD items has a Dynamic View `sequenceDiagram` (i.e., it participates in cross-component message flows), and no Debugger SAD item exists yet, and there is an SRS item tagged `#debug` that traces here — create the Debugger SAD item first. It is a shared infrastructure component; its `## Interface` section defines the Debugger API:
- Log methods: `info(msg)`, `debug(msg)`, `verbose(msg)`, `warning(msg)`, `error(msg)`
- Data write: `write(filename, data, purpose)` — writes to `--debug-output-dir` when set, regardless of `--debug-level`; appends sequence index on filename collision; logs path+purpose+write event to main log
- Subprocess log routing: `subprocess_log_path(name)` — returns a unique log file path for subprocess stdout/stderr capture; returns `None` when `--debug-output-dir` is not set; caller logs path and timing to main log
- CLI options: `--debug-level` and `--debug-output-dir`

All other SAD components' SDD items will import from it. Treat it like any other SAD item: write it, add a review point for the human to confirm the interface, and let sophist-impl wire it in during implementation.

When writing the Debugger SAD item's `## Debug strategy`, include the data model table for the Debugger's own output files (the main log file and any internal state writes). Each non-Debugger SAD component's `## Debug strategy` section must also include a data model table (filename, format, when written, purpose, contents) for the files it writes via `debugger.write()`.

If no debugger SRS item exists at all, skip this — it means runtime observability has not yet been specified at the requirements layer. Note it in the report so the human can decide whether to add it via sophist-curs.

### No `→ [SDD-` trace yet (or only a `TBD` placeholder) — create new items

Create the corresponding SDD and UT items. Read `references/cascade.md` for templates and the full process.

Key principles:
- Create one SDD item per function listed in the SAD item's `## Interface` section
- Write the algorithm based on what the SAD component's responsibility and the upstream SRS requirements say — the SDD should be specific enough to implement without guessing
- Create at least one UT item per SDD item; add more for significant error paths and edge cases
- After creating SDD and UT items, go back to each SAD item and replace the `TBD` SAD-to-SDD trace with the real link

**Write `## Debug strategy` for every SDD item created.** Based on the function's Algorithm and Error cases, draft:

- **Happy path**: the sequence of DEBUG-level log messages for a successful execution — one message per significant Algorithm step (entry, key decisions, return)
- **Error paths**: for each Error case, what log messages and variable values confirm that specific error fired
- **Key variables**: which variables from `## Variables` are most diagnostic — the ones that distinguish correct from incorrect execution
- **Analysis guide**: how to read the data files and log sequence to diagnose a failure in this function
- **Debug data model**: a table for structured data files this function writes via `debugger.write()`:

  | File | Format | When written | Purpose | Contents |
  |------|--------|-------------|---------|----------|

  Leave the table empty (`_none_`) if this function writes no data files. Add a `### Review needed` if uncertain what data to capture.

**Refactoring signal**: Before creating SDD items, check whether the area being cascaded is messy or is the third instance of a pattern:

- If the SAD review revealed that callers must manage ordering constraints, pass internal details, or call multiple methods in sequence → the interface is leaky. This is a "before feature" refactoring signal.
- If two or more existing SAD components already have a similar Interface structure to this one → Rule of Three.

In either case, automatically invoke **sophist-refact** before cascading:

> Refactoring signal detected before cascading SDD items from SAD-NNN. Running sophist-refact now. SDD items written against a leaky interface lock that leakage into every downstream function signature.

Run the full sophist-refact workflow. When it completes, resume SDD cascade here. The human may say "skip refact" to proceed without refactoring.

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

- Update `.sophist/src/tags.md` for any new tags used in new SDD or UT items
- Update `.sophist/src/sdd/index.md` traceability table
- Update `.sophist/src/ut/index.md` traceability table
- Update `SUMMARY.md` with new SDD and UT entries

---

## Step 8: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
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

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-sad/`) and write:

| File | Contents |
|------|----------|
| `00-draft-items.md` | List of all draft SAD items found, each with status (answered / pending) and the review question text |
| `01-answers-applied.md` | For each answered item: the original question, the human's answer, and which field (Interface / Location / Responsibility / Diagram) was updated |
| `02-sdd-cascade.md` | Each SDD and UT item created or updated — ID, title, parent SAD, and the key algorithm/signature decision made |
| `03-review-points.md` | All items still pending with their unanswered questions |

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
docs(sad): <short description under 72 chars>

Why: <which SAD review points were answered and what design decision was made>
What: <which SAD/SDD/UT/SIT items were created or updated>
```

Keep `Why` and `What` to one or two sentences each — enough for someone reading `git log` to understand the change without opening the diff.
