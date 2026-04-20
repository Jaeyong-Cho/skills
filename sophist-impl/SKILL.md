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

Diagram-traced logging is **essential**. Even if the human does not ask for logging instrumentation (e.g. just says "implement SDD-010" with no mention of logging), do not skip Steps 5–6 and the log call placement in Step 7 entirely

When logging is requested (or already present in the project), the system must satisfy these requirements:
Check the existing logging system. Integrate with existing logging system to do following requirement.
Check the existing options, add option to support log-level and output destination.

| Requirement | Detail |
|-------------|--------|
| **Output destination** | Configurable: `stdout` only, `file` only, or `both` simultaneously |
| **Enable/disable** | `LOG_LEVEL=0` turns logging off entirely |
| **Levels** | `LOG_LEVEL=1` — SAD only (component boundary crossings); `LOG_LEVEL=2` — SAD + SDD (full detail) |

Higher levels are cumulative: `LOG_LEVEL=2` always includes SAD logs.

The output destination is read from a `LOG_OUTPUT` setting (env var or config key, consistent with how the project reads other settings). Accepted values: `stdout` (default), `file`, `both`. When `file`, write to a project-appropriate log path (e.g. `logs/sophist.log`) or a path the human specifies.

Each log call must carry: the level name (SAD or SDD), the item ID, the step number, and the diagram label text. The exact format and implementation are determined by the project's own conventions — use whatever logging library and style the project already uses, or establish a simple one consistent with the language if none exists.

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

## Step 5: Number and extract log points from diagrams

Before writing any business logic, enumerate every log checkpoint from the diagrams. This ensures log calls in the code match the spec exactly — no guessing, no drift.

### SAD log points (level 1)

Read the `## Dynamic View` of each parent SAD item. It contains a `sequenceDiagram`. Number each arrow in visual order (top to bottom):

```
sequenceDiagram
  Client->>AuthService: 1. authenticate(email, password)
  AuthService->>UserStore: 2. findByEmail(email)
  UserStore-->>AuthService: 3. user record
  AuthService->>SessionStore: 4. createSession(userId)
  SessionStore-->>AuthService: 5. session token
  AuthService-->>Client: 6. session token
```

**If the diagram does not already have `N.` step annotations, add them now** before proceeding. This keeps the diagram and the code permanently in sync.

Build a SAD log-point table:

| Step | Label (exact diagram text) |
|------|---------------------------|
| [1]  | Client → AuthService: authenticate(email, password) |
| [2]  | AuthService → UserStore: findByEmail(email) |
| ... | ... |

### SDD log points (level 2)

Read the `## Dynamic View` of each SDD item. It is typically a `flowchart TD` or `sequenceDiagram`. Number each node or arrow in visual order:

**Flowchart example:**
```
flowchart TD
  A["[1] receive email, password"]
  --> B["[2] validate email format"]
  --> C{"[3] email valid?"}
  C -- yes --> D["[4] fetch user from UserStore"]
  C -- no --> E["[5] raise AuthError: invalid email"]
  D --> F["[6] compare password with bcrypt hash"]
  F --> G{"[7] match?"}
  G -- yes --> H["[8] call createSession(userId)"]
  G -- no --> I["[9] increment failCount; check lockout"]
```

**If step labels are not yet embedded in the node text, add them** using `["[N] original label"]` syntax.

Build an SDD log-point table:

| Step | Label |
|------|-------|
| [1]  | receive email, password |
| [2]  | validate email format |
| ... | ... |

### Map log points to function scope

Identify which SDD function body each log point belongs to, and which SAD step(s) that function corresponds to. A function typically begins where a SAD arrow arrives at this component, and ends where the SAD arrow returns. This determines where in the code to place each `log_sad` vs `log_sdd` call.

---

## Step 6: Ensure logging infrastructure exists

*(Skip this step entirely if logging instrumentation was not requested.)*

Before implementing business logic, check whether the project already has a logging system:

```bash
# Look for existing logger setup — adapt search to the project's language
grep -rl "logging\|logger\|log_file\|FileHandler\|winston\|slog" src/ 2>/dev/null | head -10
```

**If a logging system exists**: use it as-is. Wire the SAD and SDD log calls through whatever interface it already exposes. Verify that it supports `LOG_OUTPUT` (stdout / file / both) and `LOG_LEVEL` — if it doesn't, add only the missing pieces rather than replacing it.

**If no logging system exists**: create a minimal one appropriate to the project's language and style. It must:
- Route output based on `LOG_OUTPUT`: `stdout` → print only, `file` → append to log file only, `both` → do both
- Respect a `LOG_LEVEL` setting (0 = off, 1 = SAD only, 2 = SAD+SDD) — read from an env var or config file consistent with how the project reads other settings
- Expose two call sites — one for SAD-level entries and one for SDD-level entries — so callers don't embed level logic

Keep it simple. The goal is not a sophisticated logging framework; it is a reliable configurable-output, two-level system that the implementation can call without worrying about where output goes.

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

Insert log calls at the exact point in the code where the corresponding diagram step executes — not before, not after:

- **`log_sad`** — at the function's entry point where the SAD diagram shows this component receiving a message, and at the return point where it sends a response. Use the SAD item ID and the step number from the `%% [N]` annotation.
- **`log_sdd`** — at each algorithm step inside the function body, in the same order as the SDD Dynamic View diagram. Use the SDD item ID and the step number from the node label.

**Example** (Python, auth scenario):

```python
from src.logging.sophist_logger import log_sad, log_sdd

def authenticate(email: str, password: str) -> str:
    log_sad("SAD-003", 1, "Client → AuthService: authenticate(email, password)")

    log_sdd("SDD-010", 1, "receive email, password")
    log_sdd("SDD-010", 2, "validate email format")
    if not _is_valid_email(email):
        log_sdd("SDD-010", 5, "raise AuthError: invalid email")
        raise AuthError("invalid email format")

    log_sdd("SDD-010", 4, "fetch user from UserStore")
    log_sad("SAD-003", 2, "AuthService → UserStore: findByEmail(email)")
    user = user_store.find_by_email(email)
    log_sad("SAD-003", 3, "UserStore → AuthService: user record")

    log_sdd("SDD-010", 6, "compare password with bcrypt hash")
    if not bcrypt.checkpw(password.encode(), user.password_hash):
        log_sdd("SDD-010", 9, "increment failCount; check lockout")
        _handle_failed_attempt(user)
        raise AuthError("invalid credentials")

    log_sdd("SDD-010", 8, "call createSession(userId)")
    log_sad("SAD-003", 4, "AuthService → SessionStore: createSession(userId)")
    token = session_store.create_session(user.id)
    log_sad("SAD-003", 5, "SessionStore → AuthService: session token")

    log_sad("SAD-003", 6, "AuthService → Client: session token")
    return token
```

The message text must be the exact label from the diagram — copy it, don't paraphrase. This is what makes the log traceable back to the spec without ambiguity.

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
| Level | Item | Step | Diagram label |
|-------|------|------|---------------|
| SAD | SAD-003 | [1] | Client → AuthService: authenticate(email, password) |
| SAD | SAD-003 | [2] | AuthService → UserStore: findByEmail(email) |
| SDD | SDD-010 | [2] | validate email format |
| SDD | SDD-010 | [6] | compare password with bcrypt hash |
| ... | ... | ... | ... |

### Diagram Annotations Added
| Item | Change |
|------|--------|
| SAD-003 | Added %% [N] step numbers to Dynamic View sequenceDiagram |
| SDD-010 | Added [N] labels to Dynamic View flowchart nodes |

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
- Set LOG_LEVEL=1 for production (SAD only), LOG_LEVEL=2 for debugging
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
- **Log messages must match the diagram labels exactly.** Copy the text from the diagram; do not paraphrase. Paraphrasing breaks the log-to-spec traceability.
- **Number diagrams before coding.** Step annotations (`%% [N]` in mermaid) must exist in the diagram before the corresponding log call is written in code. If the diagram lacks them, add them first.
- **Never promote item state.** Leave all items as `reviewed`. sophist-codereview is the step that moves items to `done`.
- **Never silently deviate.** Any gap between the spec and what you wrote must appear in the report.
- **Never delete existing code** unless an SDD item explicitly describes replacing it. When in doubt, ask.
