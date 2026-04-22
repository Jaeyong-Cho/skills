---
name: sophist-codereview
description: |
  Use this skill to align source code and SOPHIST documents in either direction. Two modes: (1) Spec → Code — human implemented from spec, AI verifies conformance, marks items done. (2) Code → Spec — human edited source directly, AI detects divergences via git diff, judges whether the code or the spec is correct, updates spec items when the code is right, reports deviations when the code is wrong.
  Triggers: "review my code", "check my implementation", "does my code match the spec", "sophist code review", "I finished implementing SDD-010", "I edited the code directly", "sync the docs with my changes", "I made a quick fix", "update the spec to match my code".
---

# sophist-codereview: Review Code Against SOPHIST

**Goal**: Verify that source code and SOPHIST documents are aligned. Two directions are possible:

- **Spec → Code** (normal): human implemented from spec — verify code matches.
- **Code → Spec** (direct edit): human edited code directly — find what diverged, judge whether the code or the spec is correct, and update whichever is wrong.

Read before starting:
- `references/items.md` — item format, traceability
- `references/structure.md` — SAD file location conventions, SDD signature conventions
- `.sophist/src/goal.md` — project goal (if it exists); useful context when judging whether a divergence matters

---

## Step 1: Identify scope and mode

### 1a. Detect direct code edits

Before anything else, check if the human edited source files directly without going through the spec cycle:

```bash
git diff HEAD --name-only          # unstaged changes
git diff --cached --name-only      # staged changes
git status --short                 # overall picture
```

If modified source files correspond to existing SOPHIST items → treat this as **Code → Spec** mode. The human's edits are the source of truth for *intent*; the spec is the source of truth for *design contract*. Your job is to reconcile them.

If the human says "I just implemented SDD-010" with no prior direct edits → **Spec → Code** mode.

When in doubt, check both: find the scope, compare code to spec, then classify each divergence (Step 5c).

### 1b. Identify scope

Ask the human (or infer from context) which items are in scope:
- `"I edited auth.py directly"` → find all SDD items under the SAD that owns `auth.py`
- `"I implemented SDD-010"` → read `.sophist/src/sdd/SDD-010.md` directly
- `"I finished the auth module"` → find all SDD items under SAD-003:
  `grep -rl "SAD-003" .sophist/src/sdd/`
- `"review everything"` → full review of all `reviewed` and `done` items

```bash
# Find all reviewed SDD items
grep -rl "^\`reviewed\`" .sophist/src/sdd/ | sort

# Find all done SDD items (direct edits may have made done items diverge)
grep -rl "^\`done\`" .sophist/src/sdd/ | sort

# Find SDD items for a specific SAD component
grep -rl "\[SAD-003\]" .sophist/src/sdd/
```

---

## Step 2: Read SOPHIST items in scope

Read each relevant item file directly:

```bash
# Read a specific SDD item
cat .sophist/src/sdd/SDD-010.md

# Read its parent SAD item (find via trace reference in the SDD file)
grep "← \[SAD-" .sophist/src/sdd/SDD-010.md
# → then: cat .sophist/src/sad/SAD-003.md

# Read all SDD items under a given SAD component
grep -rl "\[SAD-003\]" .sophist/src/sdd/ | sort | xargs -I{} cat {}

# Read linked UT items (find via trace)
grep "→ \[UT-" .sophist/src/sdd/SDD-010.md
# → then: cat .sophist/src/ut/UT-010.md
```

Build a checklist from each item's sections:
- SAD `## Location` → expected file path in `src/`
- SDD `## Signature` → expected function signature
- SDD `## Algorithm` → expected implementation steps
- SDD `## Error cases` → expected error handling
- SDD `## Traces` → `[UT-*]` links → test items to verify

---

## Step 3: Read the source code

```bash
# Verify file exists at SAD-specified location
ls src/<path>/<FileName>

# Read the file
cat src/<path>/<FileName>
```

Read all files relevant to the items in scope.

---

## Step 4: Check SAD conformance

For each SAD item in scope, verify:

| Check | Pass criterion |
|-------|---------------|
| File location | Source file exists at the path specified in SAD `## Location` |
| Responsibility | The file/class contains only what SAD's `## Responsibility` describes |
| Interface | Every method listed in SAD `## Interface` exists with a matching signature |
| Dependencies | The code depends only on the SAD-specified dependencies |

Report each deviation with:
- SAD item ID and field
- What the document says
- What the code has
- Severity: `mismatch` (wrong) | `missing` (not implemented) | `extra` (not in spec)

---

## Step 5: Check SDD conformance

For each SDD item in scope, verify:

| Check | Pass criterion |
|-------|---------------|
| Signature | Function name, parameter names, types, and return type match SDD `## Signature` |
| Algorithm | Each numbered step in SDD `## Algorithm` is identifiable in the code |
| Error cases | Every error case in SDD `## Error cases` is handled |
| Side effects | Side effects match SDD `## Side effects` declaration |

Flag deviations by SDD item ID. Do not suggest fixes — ask the human to decide.

Example finding:
```
SDD-010 — AuthService.authenticate()
  MISMATCH signature: SDD specifies `authenticate(email: string, password: string)`
                      Code has      `authenticate(credentials: {email, password})`
  MISSING error case: SDD-010 specifies AuthError.ACCOUNT_LOCKED — not found in code
  EXTRA logic: Code checks `user.isActive` — not specified in SDD-010
               → Should this be a new SDD item, or was this intentional?
```

---

## Step 5b: Check debug strategy coverage

For each SAD item in scope, check whether `## Debug strategy` exists and is implemented:

| Check | Pass criterion |
|-------|---------------|
| `## Debug strategy` present in SAD | Section exists with healthy trace, key observables, failure signatures, and diagnostic process |
| Healthy trace implemented | Log calls exist at the component entry, each outbound call, and return — matching the healthy trace description |
| Key observables logged | Variables listed under "Key observables" appear in at least one log message |
| Failure signatures covered | Log messages exist that would produce the described failure signature for each failure mode |

For each SDD item in scope, check whether `## Debug trace` exists and is implemented:

| Check | Pass criterion |
|-------|---------------|
| `## Debug trace` present in SDD | Section exists with happy path, error paths, and key variables |
| Happy path trace implemented | Log messages in the code match the happy path trace in order |
| Error paths covered | Each error path in `## Debug trace` has at least one log call before the raise/return |
| Key variables captured | Variables listed under "Key variables" appear in at least one log message |
| Debug data files written | Each row in `## Debug data` tables (SAD and SDD) has a corresponding `debugger.write()` call at the specified trigger point, with the exact filename and fields from the spec |
| Debug data guarded | Every `debugger.write()` call is safe: the Debugger no-ops if `--debug-output-dir` is unset — no separate guard needed |
| Log format includes source location | Debugger formatter emits `filename:line_number` in every log line — configured at formatter setup, not at individual call sites |

Flag missing sections as `missing-debug-spec`:
```
SAD-003 — AuthService
  MISSING debug-spec: no ## Debug strategy section — developer cannot tell from the spec
  what logs to look for when this component fails.
```

---

## Step 5c: Check module depth

For each SAD component in scope, evaluate whether the implemented code is a **deep module** (Ousterhout, *A Philosophy of Software Design*):

| Check | Pass criterion |
|-------|---------------|
| Interface vs. implementation ratio | The public API surface (number of functions × parameter complexity) is substantially smaller than the internal implementation complexity |
| Information hiding | Internal data structures, algorithms, and external dependencies are not visible or required by callers |
| No pass-through | The component is not merely delegating calls to another module without adding its own logic |
| Caller knowledge | Callers can use the component correctly without understanding how it works internally |

Flag shallow modules with severity `shallow`:
```
SAD-003 — AuthService
  SHALLOW: authenticate() and checkLockout() are always called together by callers.
  → Consider whether lockout checking should be absorbed into authenticate() so callers
    don't need to orchestrate the two-step sequence.
```

Do not suggest specific refactors — describe the shallowness and ask the human to decide.

---

## Step 5d: Classify divergences (Code → Spec mode)

For every deviation found in steps 4–5b, judge whether **the code is right** (spec is stale) or **the code is wrong** (code is a bug or unintended deviation).

Use this heuristic:

| Signal | Likely verdict |
|--------|---------------|
| Change is a subset/superset of the spec (added null check, added missing error case, renamed param to clearer name) | **Code is right** — spec is stale |
| Change is consistent with the SAD component's Responsibility and the SRS intent | **Code is right** — spec is stale |
| Change is a bug fix (the old spec described incorrect behavior) | **Code is right** — spec is stale |
| Change contradicts a core invariant or removes required error handling | **Code is wrong** — report as deviation |
| Change adds responsibility that belongs to a different SAD component | **Code is wrong** — report as deviation |
| Change is structurally different from the algorithm for unclear reasons | **Ambiguous** — ask the human before acting |

When ambiguous, ask one focused question rather than listing options. Prefer to trust the human's intent when the change is coherent.

### When code is right: update the spec

For each "code is right" divergence, update the SOPHIST items to match the code:

- **Signature changed**: rewrite `## Signature` in the SDD item
- **Algorithm step changed or added**: update the numbered step; if steps were reordered, renumber
- **New error case added**: add a row to `## Error cases`
- **Side effect changed**: update `## Side effects`
- **File moved**: update `## Location` in the SAD item
- **Interface changed**: update `## Interface` in the SAD item

After updating: if the change was trivial (variable rename, wording, added null check that doesn't alter the algorithm), keep the item state as-is. If the change was structural (algorithm logic, interface shape, error contract), set the item back to `draft` — it needs a review pass before being treated as authoritative again.

Also check whether the linked UT items still match the updated spec. If a test's `## Input` or `## Expected output` is now wrong, update it.

### When code is wrong: report as deviation

Use the same format as steps 4–5: item ID, what the spec says, what the code has, severity. Do not fix the code — the human decides.

---

## Step 6: Check test presence

For each implemented SDD item, read the linked UT item file and verify a corresponding test stub exists in the test directory.

Each test item has its own directory: `tests/ut/ut-{NNN}/`, `tests/at/at-{NNN}/`, `tests/sit/sit-{NNN}/`.

```bash
# Read the UT item to know what function/case to look for
cat .sophist/src/ut/UT-010.md

# Check test stub directory and file exist
ls tests/ut/ut-010/
```

For AT and SIT items in scope:
```bash
ls tests/at/at-005/
ls tests/sit/sit-003/
```

Report missing test files or test cases by item ID.

---

## Step 7: Check for undocumented code

Look for significant code that has no corresponding SDD item:

```bash
# List all functions/methods in the source file
grep -n "def \|function \|async \|^\s*[a-zA-Z].*(" src/<path>/<file>

# List all SDD items that reference this SAD component
grep -rl "\[SAD-003\]" .sophist/src/sdd/ | xargs ls
```

Compare functions found in source against SDD items. Any non-trivial function without a SDD item is either:
- A private helper (may be acceptable — flag for awareness)
- Missing SDD coverage (should be documented with a new SDD item)

Ask the human whether undocumented functions need SDD items added.

---

## Step 8: Mark conformant items as `done`

For each item where no deviations were found, update its `## State` from `` `reviewed` `` to `` `done` ``:

```bash
# Example: mark SDD-010 done
sed -i '' 's/^`reviewed`$/`done`/' .sophist/src/sdd/SDD-010.md
```

Do this for SDD items, their parent SAD items (if all SDD items under that SAD are done), and the linked UT/AT/SIT items when their test stubs are confirmed present.

For items with deviations, leave state as `reviewed` and list what needs to be resolved before they can be marked `done`.

---

## Step 9: Report

```
## Code Review: Auth Module
Scope: SAD-003, SDD-010, SDD-011, SDD-012, AT-005, SIT-003, UT-010, UT-011, UT-012

### SAD Conformance

| Item | Check | Result |
|------|-------|--------|
| SAD-003 | File location: src/auth/AuthService.ts | ✅ Present |
| SAD-003 | Interface: authenticate() | ✅ Present |
| SAD-003 | Interface: checkLockout() | ❌ Missing — method not found in file |

### SDD Conformance

| Item | Check | Result |
|------|-------|--------|
| SDD-010 | Signature | ⚠️ Mismatch — see detail below |
| SDD-010 | Algorithm step 3 (bcrypt compare) | ✅ |
| SDD-010 | Error: ACCOUNT_LOCKED | ❌ Missing |
| SDD-011 | Signature | ✅ |
| SDD-011 | All algorithm steps | ✅ |

### Module Depth

| Component | Depth Assessment |
|-----------|-----------------|
| SAD-003   | ✅ Deep — callers only call authenticate(); lockout logic hidden inside |

### Deviations (require human decision)

**SDD-010 — signature mismatch**
  SDD: `authenticate(email: string, password: string): Session | AuthError`
  Code: `authenticate(credentials: Credentials): Session | AuthError`
  → Is this an intentional change? If yes, SDD-010 needs updating (sophist-fast).

**SDD-010 — ACCOUNT_LOCKED not handled**
  → Was this omitted intentionally or accidentally?

**SAD-003 — checkLockout() not implemented**
  → Is this item still pending?

### Undocumented Code

- `normalizeEmail(email: string)` — no SDD item
  → Private helper? Add as SDD item if non-trivial logic.

### Test Coverage

| Item | Directory | Status |
|------|-----------|--------|
| UT-010 | tests/ut/ut-010/ | ✅ stub present |
| UT-011 | tests/ut/ut-011/ | ✅ stub present |
| UT-012 | tests/ut/ut-012/ | ❌ directory missing |
| AT-005 | tests/at/at-005/ | ✅ stub present |
| SIT-003 | tests/sit/sit-003/ | ❌ directory missing |

### Spec updates applied (Code → Spec mode)

| Item | Field updated | Change |
|------|--------------|--------|
| SDD-010 | Signature | param renamed `credentials` → `email, password` |
| SDD-010 | Algorithm step 2 | added null check before bcrypt compare |

Items set back to `draft` (structural change):
- SDD-010 — algorithm changed, needs re-review before treated as authoritative

### Ready to Promote

No items are ready to promote — resolve deviations first.
```

---

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-codereview/`) and write:

| File | Contents |
|------|----------|
| `00-scope.md` | Items reviewed, mode detected (Spec→Code or Code→Spec), and scope rationale |
| `01-deviations.md` | Every divergence found — item ID, field, what spec says, what code has, severity classification, and verdict (code-right / code-wrong / ambiguous) |
| `02-spec-updates.md` | Each spec field updated (Code→Spec mode) — old value, new value, and whether item was reset to draft |
| `03-depth-assessment.md` | Module depth evaluation per SAD component — depth verdict and any shallow flags |

---

## Constraints

- **Never write or rewrite source code.** Even to fix a mismatch.
- **Never generate test code.** Report missing tests; the human writes them.
- **Never silently accept deviations.** Every mismatch must be classified and resolved — either the spec is updated to match the code, or the deviation is reported for the human to fix.
- **When updating the spec to match code**: trivial changes (rename, added null check) keep item state; structural changes (algorithm, interface, error contract) set the item back to `draft`.
- **When ambiguous**, ask one focused question rather than making a unilateral decision about which side is correct.
