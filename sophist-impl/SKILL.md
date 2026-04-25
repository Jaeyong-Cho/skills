---
name: sophist-impl
description: |
  SOPHIST implementation skill. Use this to implement source code for a specific SOPHIST item (SDD, SAD component, or a named feature). Reads the full upstream context (SDD → SAD → SRS → CuRS) and downstream test items (UT), then writes code that strictly follows the spec. Automatically instruments code with diagram-traced log calls at SAD and SDD level. When a conflict or ambiguity blocks implementation, writes a review point on the relevant item instead of guessing.
  Triggers: "sophist-impl", "implement SDD-010", "implement SAD-003", "implement the auth module", "write the code for SDD-012", "sophist implement", "implement this item".
  Use this whenever the human wants AI to write source code driven by SOPHIST documents — even if they say "just implement it" or "write the code" while a SOPHIST book is present.
---

# sophist-impl: Implement Code from SOPHIST Items

**Goal**: Write source code that exactly matches reviewed SOPHIST items — the right file location, the right function signature, the right algorithm steps.

If `.sophist/src/goal.md` exists, read it for context — it describes the project's purpose and can help resolve ambiguities about intent when the spec leaves room for interpretation. Instrument every implementation with appropriate log calls so runtime behavior is observable and traceable back to the spec. When something in the spec is unclear or contradictory, write a review point on the item rather than guessing. Never deviate silently.

---

## Debug model

Debug instrumentation is **essential**. Always perform Steps 5–6 and place debug calls in Step 7 — even if the human says nothing about it (e.g. "implement SDD-010"). Only skip Steps 5–6 if the human **explicitly asks not to instrument debugging**.

The project uses a single **Debugger** component that owns all debug output: structured log lines and structured data files both go through it. This keeps `--debug-output-dir` and `--debug-level` in one place — components never touch the filesystem or routing directly.

### Authoritative source: SOPHIST book items

Look for a Debugger SAD item tagged `#debug` in the SOPHIST book (Step 6a below). **If one exists, its `## Interface` and linked SDD items are the binding spec** — use their exact signatures. The default model below is a fallback only when no Debugger items exist yet.

### Default Debugger model (fallback)

When no Debugger SAD/SDD items exist, read `../sophist-shared/debugger-spec.md` for the full interface specification and reference Python implementation. Then suggest to the human that it should be captured as SOPHIST items via sophist-curs.

---

## Step 1: Determine scope

Infer the target from the human's message:

- `"implement SDD-010"` → single SDD item
- `"implement SAD-003"` → all SDD items under that SAD component
- `"implement the auth module"` → find the relevant SAD component by tag or keyword, then all its SDDs
- `"implement everything ready"` → all reviewed SDD items not yet `done`

```bash
# Find reviewed SDD items not yet done
grep -rl "^\`reviewed\`" .sophist/src/sdd/ | sort

# Find all SDD items under a SAD component
grep -rl "\[SAD-003\]" .sophist/src/sdd/

# Find SDD items by keyword
grep -rl "authenticate" .sophist/src/sdd/
```

If the scope is ambiguous, ask: "I found these items — implement all of them, or just some?"

---

## Step 2: Check readiness

Only implement items in `reviewed` state. If a target item is still `draft`, stop and tell the human:

```
SDD-010 is still `draft` — it has unanswered review points. Run sophist-sdd first to resolve them before implementing.
```

For each item in scope, also trace upward:
- Read the parent SAD item (via `← [SAD-` trace)
- Confirm the SAD item is `reviewed` — its Location and Interface are the source of truth for file path and function signatures

---

## Step 3: Read the full context

For each SDD item to implement, build a complete picture before writing a single line:

**Upstream** (why this code exists):
```bash
# Read the SDD item
cat .sophist/src/sdd/SDD-{NNN}.md

# Read its parent SAD (for file location, component responsibility)
grep "← \[SAD-" .sophist/src/sdd/SDD-{NNN}.md
cat .sophist/src/sad/SAD-{MMM}.md

# Read the SRS items traced from that SAD (for the requirement intent)
grep "← \[SRS-" .sophist/src/sad/SAD-{MMM}.md
cat .sophist/src/srs/SRS-{KKK}.md
```

**Downstream** (what tests must pass):
```bash
# Read linked UT items
grep "→ \[UT-" .sophist/src/sdd/SDD-{NNN}.md
cat .sophist/src/ut/UT-{NNN}.md
```

You don't need to read CuRS unless the SRS intent is genuinely unclear. The SDD and its parent SAD are the primary implementation contract.

---

## Step 3b: Refactoring signal — check before writing

Before touching any code, look at the implementation target through a refactoring lens:

**Rule of Three**: Scan the source directory for functions that implement a similar pattern to the one you're about to write:

```bash
grep -rn "def \|function \|async " src/ | grep -i "<keyword>"
```

If two or more existing functions already solve the same kind of problem — same multi-step flow, same error pattern, same data transformation — you're about to create the third instance. Flag it:

> Rule of Three: this pattern already exists in `src/X.py` and `src/Y.py`. Consider running **sophist-refact** before implementing, to consolidate the pattern into a shared module. The human may still proceed — this is a signal, not a blocker.

**Before feature**: If the target file exists and the code you need to extend is messy (hard to read, no clear structure, mixed concerns), flag it:

> Messy area detected in `<file>:<line>`. Refactoring first would make this implementation cleaner. Consider running **sophist-refact**. The human may still proceed.

If either signal is present, automatically invoke **sophist-refact** before writing any new code:

> Refactoring signal detected. Running sophist-refact now before implementing. Clean code first makes the implementation straightforward.

Run the full sophist-refact workflow. When it completes, resume implementation here. The human may say "skip refact" to proceed directly to implementation.

---

## Step 4: Check the existing file

Before writing, check if the file already exists at the SAD-specified Location:

```bash
ls src/<path-from-sad-location>
```

- **File exists**: read it. You may be adding a function to an existing file, not creating from scratch. Preserve everything that's already there.
- **File doesn't exist**: create it with the right imports and structure implied by the SAD component.

---

## Step 5: Read the debug strategy

Before writing any business logic, read the debug specifications in the SOPHIST items. These tell you exactly what to log and why — use them as the binding spec for log placement, the same way `## Algorithm` is the binding spec for code logic.

**From the SAD item — `## Debug strategy`**: read the healthy trace, key observables, failure signatures, and diagnostic process. These define the `INFO`-level log points — the component boundary events that a developer needs to reconstruct what happened.

**From the SDD item — `## Debug trace`**: read the happy path trace, error path traces, and key variables. These define the `DEBUG`-level log points — the internal moments that distinguish correct execution from a bug.

If a `## Debug strategy` or `## Debug trace` section is missing from the spec, write a review point on that item and fall back to reading the diagrams:
- **SAD Dynamic View** (`sequenceDiagram`): entry points, outbound calls, and returns → `INFO`-level moments.
- **SDD Dynamic View** (`flowchart TD` or `sequenceDiagram`): key decisions, error branches → `DEBUG`-level moments.

No step-by-step annotation of diagram nodes is required. The debug sections in the spec replace the need to guess.

---

## Step 6: Ensure the Debugger exists

*(Skip this step entirely if debug instrumentation was not requested.)*

### 6a: Find the Debugger specification in the SOPHIST book

```bash
grep -rl "#debug" .sophist/src/sad/ 2>/dev/null
grep -rl "Debugger" .sophist/src/sad/ 2>/dev/null | head -5
```

**If a Debugger SAD item exists**: read it and its linked SDD items — they are the binding spec for the Debugger's interface and algorithm. Follow them exactly; do not substitute the default model.

**If no Debugger SAD item exists**: use the default model from the "Debug model" section above. After implementing, suggest creating a Debugger CuRS → SRS → SAD → SDD chain via sophist-curs.

### 6b: Check and set up the Debugger in source code

```bash
grep -rl "Debugger\|debugger" src/ 2>/dev/null | head -10
```

**If a Debugger already exists**: use it. Confirm it exposes both log methods (`info`, `debug`, `verbose`, `warning`, `error`) and `write(filename, data)`. If it only has log methods (old Logger), add `write()` to it rather than creating a second component.

**If none exists**: create a single Debugger class/module. Adapt the language, style, file name, and class structure to the project — the Python snippet below illustrates the required behaviors; it is **one example, not a prescription**:

```python
# Example: debugger.py (Python) — adapt name, structure, and idioms to your project's language
import json, logging, os
from datetime import datetime

class Debugger:
    _LEVELS = {"OFF": 0, "INFO": 1, "DEBUG": 2, "VERBOSE": 3}

    def __init__(self, debug_level: str = "OFF", debug_output_dir: str | None = None):
        self._threshold = self._LEVELS.get(debug_level.upper(), 0)
        self._dir = debug_output_dir
        self._log = self._make_logger(debug_output_dir)

    def _make_logger(self, output_dir: str | None) -> logging.Logger:
        log = logging.getLogger("app.debugger")
        log.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s")
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            h = logging.FileHandler(os.path.join(output_dir, f"{datetime.now():%Y%m%d-%H%M%S}.log"))
        else:
            h = logging.StreamHandler()
        h.setFormatter(fmt)
        log.addHandler(h)
        return log

    def info(self, msg: str) -> None:
        if self._threshold >= 1: self._log.info(msg)

    def debug(self, msg: str) -> None:
        if self._threshold >= 2: self._log.debug(msg)

    def verbose(self, msg: str) -> None:
        if self._threshold >= 3: self._log.debug(f"[VERBOSE] {msg}")

    def warning(self, msg: str) -> None:
        if self._threshold >= 1: self._log.warning(msg)

    def error(self, msg: str) -> None:
        if self._threshold >= 1: self._log.error(msg)

    def write(self, filename: str, data, purpose: str = "") -> None:
        """Write structured debug data to --debug-output-dir.
        No-op if dir is unset. Triggered by --debug-output-dir alone,
        regardless of --debug-level. Appends -N index on filename collision.
        Logs file path, purpose, and write event to main log."""
        if not self._dir:
            return
        try:
            os.makedirs(self._dir, exist_ok=True)
            # Resolve collision: append -1, -2, ... before extension
            base, ext = os.path.splitext(filename)
            candidate = os.path.join(self._dir, filename)
            idx = 1
            while os.path.exists(candidate):
                candidate = os.path.join(self._dir, f"{base}-{idx}{ext}")
                idx += 1
            with open(candidate, "w") as f:
                if filename.endswith(".json"):
                    json.dump(data, f, indent=2)
                else:
                    f.write(str(data))
            # Log metadata to main log
            self._log.info(f"[debug-write] path={candidate} purpose={purpose or 'unspecified'}")
        except Exception:
            pass  # debug output must never crash the program

    def subprocess_log_path(self, name: str) -> str | None:
        """Return a unique log file path for a subprocess to write stdout/stderr to.
        Returns None when --debug-output-dir is not set (caller skips capture).
        Caller must log the returned path and start time before launching the subprocess,
        and log completion (exit code, duration) after it exits."""
        if not self._dir:
            return None
        os.makedirs(self._dir, exist_ok=True)
        return os.path.join(self._dir, f"{name}-{datetime.now():%Y%m%d-%H%M%S}.log")
```

Construct the Debugger once at application entry from the CLI options, then pass it to every component that needs it. Components call `debugger.info(...)`, `debugger.write(...)` — they never access `--debug-output-dir` directly.

---

## Step 7: Implement

Write the code following the SDD exactly, inserting log calls at each extracted checkpoint:

| SDD field | What it drives |
|-----------|---------------|
| `## Signature` | Function name, parameter names, types, return type — match exactly |
| `## Algorithm` | Each numbered step becomes identifiable code — don't collapse or reorder steps |
| `## Variables` | Use the variable names and types listed |
| `## Error cases` | Every error case must be handled — no silent omissions |
| `## Side effects` | Honor what's declared; if "none", don't add any |

### Placing Debugger calls

**Use the debug spec as the primary guide.**

- The SAD `## Debug strategy` specifies `debugger.info()` points and component-level `debugger.write()` calls.
- The SDD `## Debug trace` specifies `debugger.debug()` points and function-level `debugger.write()` calls.

Place calls exactly where those specs say — at the same trigger points, carrying the same fields.

If neither section exists, fall back to diagram-guided placement as described in Step 5.

**`debugger.write()` calls** follow the `## Debug data` table row by row:
- Use the exact filename from the table — do not invent names.
- Pass the exact fields listed — add nothing, omit nothing.
- Pass the table's `purpose` / `contents` value as the `purpose` argument so the main log records it.
- Respect the trigger: `on entry` means the very first line of the function body; `on error` means immediately before raising; `on return` means just before returning.
- No separate guard needed — `debugger.write()` is already a no-op when `--debug-output-dir` is unset. It activates automatically when only `--debug-output-dir` is set, regardless of `--debug-level`.
- Filename collision is handled automatically — the implementation appends `-N` before the extension if the file already exists.

**Subprocess log routing**: when the SDD invokes an external process, get a path from `debugger.subprocess_log_path(name)` and direct the subprocess stdout/stderr there. Log the path and start time to the main log before launching, and log exit code and duration after:
```
debugger.info(f"[subprocess:{name}] log={log_path} start={timestamp}")
# ... run subprocess ...
debugger.info(f"[subprocess:{name}] exit={code} duration={elapsed}s")
```
If `subprocess_log_path()` returns `None` (no output dir set), skip capture and let output go to the parent's stdout/stderr.

Insert all Debugger calls at the exact point in the code where the corresponding step executes — not before, not after.

**Level mapping** — use the level that fits the importance of the event, not a rigid rule:

| Level | When to use |
|-------|-------------|
| `INFO` | Component entry/exit, inter-component calls and responses, significant state transitions — events visible in normal operation |
| `DEBUG` | Internal decisions (branch taken, validation result), sub-computations, intermediate values — needed when diagnosing a specific bug |
| `VERBOSE` | Fine-grained traces: loop iterations, large data structures, micro-steps. Use only when `DEBUG` alone isn't enough |
| `WARNING` | Something unexpected happened that the function recovered from |
| `ERROR` | An operation failed — log immediately before raising or returning an error |

There is no 1:1 requirement to log every arrow or node in the diagram. Read the SAD and SDD to understand the important steps, then **place logs at the locations where a developer would actually want to know what happened** — entry points, key decisions, error paths, and inter-component calls. Lean on your judgment: a function with 3 obvious steps doesn't need 3 log lines; a complex conditional tree does.

**Non-duplication**: Don't emit two log lines that say the same thing at the same code location. If an `INFO` at function entry already captures the parameters, don't add a `DEBUG` that repeats "received email and password". One informative log beats two redundant ones.

**Variable values are required**: Every log message must carry the runtime values that make it useful for debugging. Use the actual variable names from the SDD `## Variables` section. Format them readably inline — e.g. `f"email={email}, user_id={user.id}"`. For sensitive values (passwords, tokens, credentials), log only a safe representation (e.g., `token[:8]+"..."`, `"[redacted]"`).

**Example** (Python, auth scenario):

```python
import logging
logger = logging.getLogger(__name__)

def authenticate(email: str, password: str) -> str:
    logger.info(f"authenticate: email={email}")

    if not _is_valid_email(email):
        logger.debug(f"invalid email format: email={email}")
        raise AuthError("invalid email format")

    logger.debug(f"fetching user from UserStore: email={email}")
    user = user_store.find_by_email(email)

    if not bcrypt.checkpw(password.encode(), user.password_hash):
        logger.debug(f"password mismatch for user_id={user.id}, incrementing fail_count")
        _handle_failed_attempt(user)
        raise AuthError("invalid credentials")

    token = session_store.create_session(user.id)
    logger.info(f"authenticate complete: user_id={user.id}")
    return token
```

The logs capture the important moments (entry, validation failure, credential failure, success) with the relevant variable values. There's no mechanical step-by-step logging of every diagram node — just the information a developer needs to trace what actually happened.

**When implementing a SAD component** (multiple SDD items in the same file): write all functions for that component in one pass, so imports and shared state are coherent.

**When you hit an ambiguity** — something the SDD says that could be interpreted two ways, or a contradiction with the SAD — do not pick the more convenient interpretation and move on. Instead:

1. Stop implementing that function
2. Add a review point to the SDD item:
   ```markdown
   > **Review needed** — <describe the ambiguity: what the two interpretations are, and why it matters for the implementation>
   ```
3. Write a placeholder in the code:
   ```python
   # TODO: blocked on SDD-010 review point — [brief description]
   raise NotImplementedError("pending SDD review")
   ```
4. Continue with other functions

---

## Step 8: Create test stubs

For each UT item linked from the implemented SDDs, check if a test stub exists:

```bash
ls tests/ut/ut-{NNN}/
```

Each test item gets its own directory — `tests/ut/ut-{NNN}/`, `tests/sit/sit-{NNN}/`, `tests/at/at-{NNN}/`. If the directory doesn't exist, create it.

If no stub file exists in the directory, create one — a minimal test function that names the case and has a `pass`/`todo` body. Do not write the test assertions; the human does that after reviewing the UT item.

```python
# tests/ut/ut-010/test_authenticate.py

# UT-010: authenticate — happy path
def test_authenticate_happy_path():
    pass  # TODO: implement per UT-010

# tests/ut/ut-011/test_authenticate.py

# UT-011: authenticate — wrong password
def test_authenticate_wrong_password():
    pass  # TODO: implement per UT-011
```

For SIT stubs (`tests/sit/sit-{NNN}/`) and AT stubs (`tests/at/at-{NNN}/`), apply the same pattern only if the SAD or SRS item is in scope.

---

## Step 9: Build check

```bash
# Language-appropriate check — pick the right one for the project
cd .sophist && mdbook build 2>&1 | tail -20

# For Python
python -m py_compile src/<file>

# For TypeScript
npx tsc --noEmit
```

Fix syntax errors. Do not fix logic errors by diverging from the spec — if the spec leads to a syntax error, that's a review point too.

---

## Step 10: Report

```
## Implementation Report

### Implemented
| SDD | Function | File |
|-----|----------|------|
| SDD-010 | AuthService.authenticate() | src/auth/auth_service.py |
| SDD-011 | AuthService.checkLockout() | src/auth/auth_service.py |

### Log Points Instrumented
| Level | Location | Message summary |
|-------|----------|-----------------|
| INFO  | authenticate() entry | email |
| DEBUG | email validation failure | email |
| INFO  | authenticate() return | user_id |
| ... | ... | ... |

### Test Stubs Created
| UT | Directory |
|----|-----------|
| UT-010 | tests/ut/ut-010/ |
| UT-011 | tests/ut/ut-011/ |

### Blocked — Review Points Added
| Item | Problem |
|------|---------|
| SDD-012 | Algorithm step 3 refers to "the session store" but SAD-004 lists two possible adapters without specifying which. Added review point to SDD-012. |

### Next steps
- Answer the review point in SDD-012, then run **sophist-sdd** to apply it
- Run **sophist-codereview** to verify conformance when all items are unblocked
- Write test assertions in the stubs, following each UT item's Input/Expected output
- Pass `--debug-level=INFO` for production (boundary events only), `--debug-level=DEBUG` for diagnosing issues
```

---

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-impl/`) and write:

| File | Contents |
|------|----------|
| `00-scope.md` | Which SDD items were in scope, how scope was determined |
| `01-context.md` | Upstream context read: SAD location/interface, SRS intent summary |
| `02-log-points.md` | Every log call placed — level, function, message, and which diagram step drove it |
| `03-ambiguities.md` | Any review points written, the ambiguity described, and the placeholder left in code |

These files are for debugging the skill's decisions — why a particular log level was chosen, which diagram step maps to which log call, and what was blocked.

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
feat(<scope>): <short description under 72 chars>

Why: <which SDD item(s) drove this implementation and why they're needed>
What: <which files were created or modified and what they now do>
```

Use `feat` for new functionality, `fix` for corrections to existing implementation. The `scope` is the primary SDD item ID or component name (e.g., `sdd-010`, `auth-service`). Keep `Why` and `What` to one or two sentences each.

---

## Constraints

- **Follow the SDD exactly.** If the SDD says `bcrypt`, use bcrypt. If it says 12 rounds, use 12. Do not substitute equivalent libraries or adjust parameters without a review point.
- **Log output destination is configurable.** When creating a new logger, honour `--debug-output-dir`: if provided, write to that directory; if absent, write to stdout. Never hard-code one destination.
- **Log messages must be traceable to diagram steps.** Reference the diagram label text so a reader can identify which step fired, but enrich it with actual variable values — don't copy the label verbatim if doing so omits the runtime context. Traceability comes from the item ID and step number, not from word-for-word label repetition.
- **Logging level reflects importance.** SAD boundary events (component entry, inter-component calls, returns) belong at `INFO`. Internal algorithm steps, decisions, and error paths belong at `DEBUG`. Use `VERBOSE` only for truly fine-grained traces. Use `WARNING`/`ERROR` for unexpected or failed conditions.
- **Never promote item state.** Leave all items as `reviewed`. sophist-codereview is the step that moves items to `done`.
- **Never silently deviate.** Any gap between the spec and what you wrote must appear in the report.
- **Never delete existing code** unless an SDD item explicitly describes replacing it. When in doubt, ask.
