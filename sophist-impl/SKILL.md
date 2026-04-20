---
name: sophist-impl
description: |
  SOPHIST implementation skill. Use this to implement source code for a specific SOPHIST item (SDD, SAD component, or a named feature). Reads the full upstream context (SDD → SAD → SRS → CuRS) and downstream test items (UT), then writes code that strictly follows the spec. Automatically instruments code with diagram-traced log calls at SAD and SDD level. When a conflict or ambiguity blocks implementation, writes a review point on the relevant item instead of guessing.
  Triggers: "sophist-impl", "implement SDD-010", "implement SAD-003", "implement the auth module", "write the code for SDD-012", "sophist implement", "implement this item".
  Use this whenever the human wants AI to write source code driven by SOPHIST documents — even if they say "just implement it" or "write the code" while a SOPHIST book is present.
---

# sophist-impl: Implement Code from SOPHIST Items

**Goal**: Write source code that exactly matches reviewed SOPHIST items — the right file location, the right function signature, the right algorithm steps. Instrument every implementation with log calls that correspond one-to-one with numbered steps in the SAD and SDD diagrams, so runtime logs are directly traceable back to the spec. When something in the spec is unclear or contradictory, write a review point on the item rather than guessing. Never deviate silently.

---

## Logging model

Diagram-traced logging is **essential**. Always perform Steps 5–6 and place log calls in Step 7 — even if the human says nothing about logging (e.g. "implement SDD-010"). Only skip Steps 5–6 and log call placement if the human **explicitly asks not to instrument logging**.

### Authoritative source: SOPHIST book items

The logging specification lives in the project's SOPHIST book. Step 6a (below) looks for a Logger SAD item tagged `#logging`. **If one exists, its `## Interface` and linked SDD items are the binding spec** — use their exact function signatures and follow their algorithm. The default model below is a fallback only when no logging items exist in the book yet.

### Default logging model (fallback)

When no Logger SAD/SDD items exist, apply this spec and suggest to the human that it should be captured as SOPHIST items via sophist-curs:

| Requirement | Detail |
|-------------|--------|
| **Output destination** | Configurable via `LOG_OUTPUT`: `stdout` (default), `file`, or `both` |
| **Enable/disable** | `LOG_LEVEL=OFF` (or `0`) turns logging off entirely |
| **Levels** | Standard levels in ascending detail: `INFO` → `DEBUG` → `VERBOSE` |
| **Level semantics** | `INFO` — SAD-level (component boundary crossings); `DEBUG` — SDD-level (internal algorithm steps); `VERBOSE` — very fine-grained traces if needed |

Higher levels are cumulative: `DEBUG` always includes `INFO` output.

`LOG_OUTPUT` and `LOG_LEVEL` are read from env vars or a config key, consistent with how the project reads other settings. When `LOG_OUTPUT=file`, write to a path the human specifies.

Each log call uses the project's standard logger at the appropriate level. The message must carry: the item ID and step number as a `[ITEM.N]` prefix, and the relevant runtime variable values. Use the project's existing logging library and style (e.g. Python `logging`, Node.js `winston`, Go `slog`), or establish a minimal one consistent with the language if none exists.

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

## Step 4: Check the existing file

Before writing, check if the file already exists at the SAD-specified Location:

```bash
ls src/<path-from-sad-location>
```

- **File exists**: read it. You may be adding a function to an existing file, not creating from scratch. Preserve everything that's already there.
- **File doesn't exist**: create it with the right imports and structure implied by the SAD component.

---

## Step 5: Understand the flow from diagrams

Before writing any business logic, read the diagrams to build a mental model of the flow. This determines where to place log calls — not mechanically, but at the locations that actually matter.

**SAD Dynamic View** (`sequenceDiagram`): read it to understand the component's entry points, what it calls downstream, and what it returns. These are the `INFO`-level moments — you'll log at function entry, at each outbound call, and at function return.

**SDD Dynamic View** (`flowchart TD` or `sequenceDiagram`): read it to understand the internal algorithm — the key decisions, error branches, and transformations. These are the `DEBUG`-level moments — log at branches and error paths that a developer would need to trace when debugging.

No step-by-step numbering or annotation of diagram nodes is required. Use the diagrams as a map to understand the important moments, then place logs where they are useful. The diagrams may already have step numbers from a previous pass; you can reference them mentally but don't need to add or match them.

---

## Step 6: Ensure logging infrastructure exists

*(Skip this step entirely if logging instrumentation was not requested.)*

### 6a: Find the logging specification in the SOPHIST book

Before touching source code, look for the logging system specification in the project's SOPHIST items:

```bash
# Find Logger SAD item by tag or keyword
grep -rl "#logging" .sophist/src/sad/ 2>/dev/null
grep -rl "Logger\|logging" .sophist/src/sad/ 2>/dev/null | head -5
```

**If a Logger SAD item exists** (any SAD item tagged `#logging` or named Logger/LogService):
- Read it — the `## Interface` section defines the logger's API (level methods, message format, configuration)
- Read its linked SDD items for precise parameter names, types, and configuration keys
- Follow that interface; do not substitute the default model below

**If no Logger SAD item exists**: the logging system has not been formally specified in SOPHIST yet. Use the default logging model below. After implementing, suggest to the human that a logging CuRS → SRS → SAD → SDD chain should be created via sophist-curs to formalize what was built.

### 6b: Check and set up the logging infrastructure in source code

```bash
# Look for existing logger setup — adapt search to the project's language
grep -rl "logging\|logger\|log_file\|FileHandler\|winston\|slog" src/ 2>/dev/null | head -10
```

**If a logging system exists**: use it as-is. Wire the SAD and SDD log calls through whatever interface it already exposes. Verify that it supports `LOG_OUTPUT` (stdout / file) and `LOG_LEVEL` — if it doesn't, add only the missing pieces rather than replacing it.

**If no logging system exists**: create a minimal one appropriate to the project's language and style. It must:
- Route output based on `LOG_OUTPUT`: `stdout` → write to stdout only, `file` → append to log file only, `both` → write to both
- Respect a `LOG_LEVEL` setting that maps to standard levels — read from an env var or config file consistent with how the project reads other settings. Supported levels in ascending verbosity: `OFF`, `INFO`, `DEBUG`, `VERBOSE`
- Expose the standard level methods (`info`, `debug`, `verbose`, or the project language's equivalent) so callers choose the level at the call site

Keep it simple. The goal is a reliable, configurable-output logger that lets callers use standard levels without worrying about routing or configuration.

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

### Placing log calls

Insert log calls at the exact point in the code where the corresponding diagram step executes — not before, not after.

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
- Set LOG_LEVEL=INFO for production (boundary events only), LOG_LEVEL=DEBUG for diagnosing issues
```

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
- **Log output destination is configurable.** When creating a new logger, honour `LOG_OUTPUT`: `stdout` (default), `file`, or `both`. Never hard-code one destination.
- **Log messages must be traceable to diagram steps.** Reference the diagram label text so a reader can identify which step fired, but enrich it with actual variable values — don't copy the label verbatim if doing so omits the runtime context. Traceability comes from the item ID and step number, not from word-for-word label repetition.
- **Logging level reflects importance.** SAD boundary events (component entry, inter-component calls, returns) belong at `INFO`. Internal algorithm steps, decisions, and error paths belong at `DEBUG`. Use `VERBOSE` only for truly fine-grained traces. Use `WARNING`/`ERROR` for unexpected or failed conditions.
- **Never promote item state.** Leave all items as `reviewed`. sophist-codereview is the step that moves items to `done`.
- **Never silently deviate.** Any gap between the spec and what you wrote must appear in the report.
- **Never delete existing code** unless an SDD item explicitly describes replacing it. When in doubt, ask.
