---
name: sophist-debug
description: |
  Debug a failing run using output written to a debug directory. Reads log files and structured data files produced by the Debugger component, cross-references them against the SOPHIST spec (SAD ## Debug strategy, SDD ## Debug trace), locates the deviation point where actual execution diverged from the healthy trace, identifies the root cause, and proposes a resolution strategy grounded in the spec.
  Triggers: "sophist-debug", "debug this", "read the debug output", "analyze the logs", "what went wrong", "find the root cause", "the run failed, here are the logs", "investigate the debug directory", "analyze --debug-output-dir output", "look at the debug files", "debug output is in <path>", any mention of a directory containing debug logs or debug data files.
  Use this whenever the user provides a path to debug output, mentions a failing run with debug artifacts, or asks why something went wrong in a SOPHIST-instrumented system.
---

# sophist-debug: Root Cause Analysis from Debug Output

**Goal**: Turn raw debug output into a specific root cause and an actionable resolution strategy. The SOPHIST spec — `## Debug strategy` in SAD items and `## Debug trace` in SDD items — describes exactly what a healthy execution looks like. This skill compares the actual run against that spec to find precisely where things went wrong and why.

The guiding principle: **every deviation from the healthy trace is a diagnostic signal**. A missing log entry means a step didn't fire. An unexpected error entry means an error case fired. A data file with wrong values means a variable had the wrong value at that point in the algorithm.

If `.sophist/src/goal.md` exists, read it — understanding what the project is trying to do helps distinguish a critical failure from a minor edge-case deviation.

---

## Step 1: Locate and inventory the debug directory

Get the path from the human's message (e.g., `--debug-output-dir .sophist/debug/` or a specific timestamped run directory). If not specified, check the default:

```bash
ls .sophist/debug/ 2>/dev/null | sort -r | head -5
```

List the directory contents to understand what was captured:

```bash
ls -lh <debug-output-dir>/
```

Classify each file:
- **Log file** (`.log`, `debug.log`, `app.log`, etc.) — the primary trace
- **Entry data files** (`*-entry.json`) — input state at function entry
- **Error data files** (`*-error.json`) — state captured at point of failure
- **Return/result data files** (`*-return.json`, `*-result.*`) — output state
- **Other structured data** (`.json`, `.csv`, etc.) — intermediate state

Report the inventory before proceeding:
```
Debug directory: <path>
Log file: <name> (<size>, <line count>)
Data files: <list with sizes>
```

---

## Step 2: Read the log file

Read the log from top to bottom. The format is:
```
<timestamp> <level> <filename>:<line_number> <message>
```

Extract:

1. **Entry point** — the first `INFO` log entry (SAD-level boundary crossing — the entry into the failing component)
2. **Full sequence** — all log entries in order
3. **Last successful entry** — the last log line before the first `ERROR` or `WARNING`
4. **Error entries** — all `ERROR` and `WARNING` lines with their `filename:line_number`
5. **Exit point** — the last log entry in the file (did the component return normally or crash?)

Build a compact trace table:
```
#  | timestamp | level   | source              | message
---|-----------|---------|---------------------|--------
1  | 10:01.001 | INFO    | auth.py:23          | AuthService.authenticate() called email=foo@bar.com
2  | 10:01.002 | DEBUG   | auth.py:31          | fetching user record
3  | 10:01.003 | ERROR   | auth.py:45          | user not found: foo@bar.com
```

---

## Step 3: Read the structured data files

For each data file in the debug directory, read it and record the key values:

```bash
cat <debug-output-dir>/<filename>
```

For each file, note:
- **What it captured**: entry state, intermediate state, or error state
- **Key field values**: the ones most likely to distinguish correct from incorrect behavior
- **Anything unexpected**: null where a value was expected, wrong type, out-of-range value

---

## Step 4: Find the relevant SOPHIST components

Map the log entries to SOPHIST items using the `filename:line_number` fields in the log.

```bash
# Find the SAD item whose Location matches the source file in the logs
grep -rl "<source-file-from-log>" .sophist/src/sad/ 2>/dev/null

# Or search by component name inferred from the log messages
grep -rl "<ComponentName>" .sophist/src/sad/ 2>/dev/null
```

For each SAD component identified:

```bash
# Read the SAD item
cat .sophist/src/sad/SAD-{NNN}.md

# Find all SDD items under it
grep -rl "\[SAD-{NNN}\]" .sophist/src/sdd/ | sort | xargs -I{} cat {}
```

Build a list of: SAD item ID → source file → list of SDD item IDs for functions in scope.

---

## Step 5: Compare actual trace to the healthy trace

### SAD level — `## Debug strategy`

Read the `## Healthy trace` from each relevant SAD item. This describes the expected `INFO`-level log sequence for a correct execution.

Compare it to the actual `INFO`-level entries extracted in Step 2:

| Expected (healthy trace) | Actual (log file) | Match? |
|--------------------------|-------------------|--------|
| `AuthService.authenticate() called` | `AuthService.authenticate() called email=foo@bar.com` | ✅ |
| `user record fetched` | *(not found)* | ❌ missing |
| `password verified` | *(not found)* | ❌ missing |
| `session created` | *(not found)* | ❌ missing |

The first ❌ in the table is the **SAD-level deviation point** — the component's behavior diverged from the healthy trace at this step.

Also check the `## Failure signatures` in the SAD item. If the actual log matches a failure signature exactly, name it:
```
Failure signature matched: "user not found" → SAD-003 failure mode: "record lookup failed"
```

### SDD level — `## Debug trace`

For the SDD item corresponding to the function where the deviation occurred, read its `## Debug trace`.

Compare the **happy path** trace to the actual `DEBUG`-level log entries:

| Expected (happy path) | Actual (log file) | Match? |
|----------------------|-------------------|--------|
| `fetching user by email` | `fetching user record` | ✅ |
| `user record found, checking password` | *(not found)* | ❌ missing |

The first ❌ is the **SDD-level deviation point** — the specific algorithm step that didn't complete.

Then check the `## Error paths` in `## Debug trace`. If an error path trace matches the actual log sequence leading to the `ERROR` entry, that confirms which error case fired.

---

## Step 6: Read the data files against the spec

For each data file, find its corresponding row in the `## Debug data` table of the relevant SAD or SDD item:

```
| File                  | Format | When written | Contents                        |
|-----------------------|--------|-------------|--------------------------------|
| auth-entry.json       | JSON   | on entry    | email, session_id               |
| auth-error.json       | JSON   | on error    | ErrorType, email, lookup_query  |
```

Compare the spec's **Contents** column against the actual values in the file:

- **Missing fields**: a field the spec says should be there is absent → the Debugger was not wired correctly, or the error occurred before that variable was set
- **Null/empty values**: the variable existed but had no value → likely initialization or assignment bug
- **Unexpected values**: the variable has a value, but it's wrong → logic bug upstream of this point
- **Missing file entirely**: the trigger condition (`on entry`, `on error`, etc.) never fired → the code path that writes this file was not reached

These observations feed directly into the root cause.

---

## Step 7: Root cause analysis

Synthesize the findings from Steps 2–6 into a single root cause statement.

Structure:
1. **Failure mode**: which SAD failure signature fired (from `## Debug strategy`)
2. **Deviation point**: the specific SDD algorithm step that didn't complete (from `## Debug trace`)
3. **Evidence**: the log entries and data file values that confirm this
4. **Cause**: the specific condition that produced the deviation

Example:
```
Root cause: AuthService.authenticate() — user lookup returned empty result

Failure mode (SAD-003): "record lookup failed"
Deviation point (SDD-010, step 2): "fetch user by email" — the log shows the
  DB query was issued but no "user record found" entry follows. The auth-error.json
  confirms: lookup_query="SELECT * FROM users WHERE email=?" but the users table
  has email stored in lowercase while the input was "Foo@Bar.com" (mixed case).

Evidence:
  - Log line 3: ERROR auth.py:45 "user not found: Foo@Bar.com"
  - auth-entry.json: { "email": "Foo@Bar.com" }
  - auth-error.json: { "ErrorType": "UserNotFoundError", "lookup_query": "SELECT * FROM users WHERE email='Foo@Bar.com'" }

Cause: Email comparison is case-sensitive. The input is not normalized before
  the DB lookup. SDD-010 step 1 specifies "normalize email to lowercase" but
  the implementation skips this step.
```

If the root cause is ambiguous (multiple plausible explanations), list them ranked by likelihood and identify what additional data or log would distinguish them. Do not guess between equally likely causes.

---

## Step 8: Resolution strategy

Propose a resolution grounded in the spec. Structure by category:

### Code fix (most common)

If the code deviated from the SDD algorithm:
- Name the SDD item and step number that was missed or wrong
- Describe the fix in terms of the algorithm step: "SDD-010 step 1 — add `email = email.lower()` before the DB lookup"
- Note which UT item covers this case; if none does, flag that a new UT item is needed

### Spec fix (when the spec was wrong)

If the logs show the code did something reasonable but the spec didn't anticipate it:
- Name the SDD item and what the spec missed
- Recommend running `sophist-codereview` in Code → Spec mode to update the spec
- Flag if the algorithm change is structural (requires re-review of the SDD item)

### Debug spec gap (when the debug output wasn't enough to diagnose)

If the root cause required guessing because the debug output didn't capture enough state:
- Name the specific variable or decision point that was missing
- Recommend adding it to the `## Debug trace` / `## Debug data` table in the SDD item
- Recommend running `sophist-codereview` to verify the new instrumentation is added

### Infrastructure fix (Debugger not wired correctly)

If expected data files are missing or log format is wrong:
- Name the missing files and the trigger condition that should have written them
- Point to the `debugger.write()` call site that's missing or incorrectly guarded
- Note: `debugger.write()` is always a no-op when `--debug-output-dir` is unset — check that `--debug-output-dir` was actually set in the run that produced this output

---

## Step 9: Report

```
## Debug Analysis: <component name or run description>

### Inventory
Log: <filename> — <N> lines, <N> ERROR, <N> WARNING entries
Data files: <list>

### Trace comparison

**SAD-003 healthy trace vs actual** (INFO level)
| Step | Expected | Actual | |
|------|----------|--------|--|
| 1    | component entry logged | ✅ present | |
| 2    | user record fetched    | ❌ missing | ← deviation point |
| 3    | password verified      | ❌ missing | |

**SDD-010 happy path vs actual** (DEBUG level)
| Step | Expected | Actual | |
|------|----------|--------|--|
| 1    | normalize email | ❌ no log entry for this | ← root step |
| 2    | fetch user by email | ✅ present | |

**Error path matched**: SDD-010 error path "UserNotFoundError"

### Data file findings
| File | Expected fields | Finding |
|------|----------------|---------|
| auth-entry.json | email | email="Foo@Bar.com" — not normalized |
| auth-error.json | ErrorType, lookup_query | lookup_query shows raw mixed-case email |

### Root cause
SDD-010 step 1 (normalize email) was skipped. The DB lookup uses the raw
input email which is case-sensitive. Confirmed by auth-error.json.

### Resolution strategy

**Code fix — SDD-010, step 1**
Add `email = email.lower()` before the DB lookup call. SDD-010 step 1 already
specifies this — the implementation is missing it.

No spec change needed. SDD-010 algorithm is correct as written.

**Test gap**: UT item for mixed-case email input not found.
→ Add a UT item: `authenticate() with mixed-case email returns session`.

### Next steps
1. Fix SDD-010 step 1 implementation (`src/auth/auth_service.py:28`)
2. Add UT item for mixed-case email (run sophist-sdd to create it)
3. Re-run with `--debug-output-dir` to confirm healthy trace matches spec
```

---

## Constraints

- **Never modify source code directly.** Describe the fix precisely enough that the human or sophist-impl can apply it.
- **Never guess between equally likely root causes.** If the debug output is insufficient to distinguish, say so and describe what additional data would resolve the ambiguity.
- **Always ground the resolution in the spec.** A "fix" that contradicts the SDD algorithm is not a fix — it's a new deviation. If fixing the code requires changing the spec, flag that explicitly.
- **Report missing debug instrumentation as a finding.** If the debug output was insufficient to diagnose the problem, the debug spec (`## Debug trace`, `## Debug data`) needs updating — that is itself a deliverable of this analysis.
- **Do not run the program.** This skill is read-only: it reads debug artifacts and SOPHIST docs. It does not execute, rebuild, or re-run anything.
