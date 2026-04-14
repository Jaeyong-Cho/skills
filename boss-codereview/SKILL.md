---
name: boss-codereview
description: |
  Use this skill after the human has written source code and wants AI to review it against BOSS documents. Triggers: "review my code", "check my implementation", "does my code match the spec", "boss code review", "I finished implementing SDD-010". AI checks conformance to SDD (function signatures, algorithms, error handling), alignment with SAD (file locations, component responsibilities), and presence of test stubs. Conformant items are marked `done`. AI never rewrites or generates code — it reports findings and asks questions.
---

# boss-codereview: Review Human-Written Code Against BOSS

**Goal**: Verify that human-written source code conforms to the reviewed SDD and SAD items. Identify deviations, missing items, and test coverage gaps. Report findings with references to specific document items. Write no code.

Read before starting:
- `references/items.md` — item format, traceability
- `references/structure.md` — SAD file location conventions, SDD signature conventions

---

## Step 1: Identify scope

Ask the human (or infer from context) which items have been implemented:
- `"I implemented SDD-010"` → read `book/src/sdd/SDD-010.md` directly
- `"I finished the auth module"` → find all SDD items under SAD-003:
  `grep -rl "SAD-003" book/src/sdd/`
- `"review everything"` → full review of all `reviewed` items

```bash
# Find all reviewed SDD items
grep -rl "^\`reviewed\`" book/src/sdd/ | sort

# Find all reviewed SAD items
grep -rl "^\`reviewed\`" book/src/sad/ | sort

# Find SDD items belonging to a specific SAD component (e.g. SAD-003)
grep -rl "\[SAD-003\]" book/src/sdd/
```

---

## Step 2: Read BOSS items in scope

Read each relevant item file directly:

```bash
# Read a specific SDD item
cat book/src/sdd/SDD-010.md

# Read its parent SAD item (find via trace reference in the SDD file)
grep "← \[SAD-" book/src/sdd/SDD-010.md
# → then: cat book/src/sad/SAD-003.md

# Read all SDD items under a given SAD component
grep -rl "\[SAD-003\]" book/src/sdd/ | sort | xargs -I{} cat {}

# Read linked UT items (find via trace)
grep "→ \[UT-" book/src/sdd/SDD-010.md
# → then: cat book/src/ut/UT-010.md
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

## Step 5b: Check module depth

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

## Step 6: Check test presence

For each implemented SDD item, read the linked UT item file and verify a corresponding test stub exists in the test directory.

```bash
# Read the UT item to know what function/case to look for
cat book/src/ut/UT-010.md

# Check test stub file exists
ls tests/ut/

# Check test case exists for function
grep -rn "authenticate\|UT-010" tests/ut/
```

For AT and SIT items in scope:
```bash
ls tests/at/
ls tests/sit/
grep -rn "AT-005" tests/at/
grep -rn "SIT-003" tests/sit/
```

Report missing test files or test cases by item ID.

---

## Step 7: Check for undocumented code

Look for significant code that has no corresponding SDD item:

```bash
# List all functions/methods in the source file
grep -n "def \|function \|async \|^\s*[a-zA-Z].*(" src/<path>/<file>

# List all SDD items that reference this SAD component
grep -rl "\[SAD-003\]" book/src/sdd/ | xargs ls
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
sed -i '' 's/^`reviewed`$/`done`/' book/src/sdd/SDD-010.md
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
  → Is this an intentional change? If yes, SDD-010 needs updating (boss-update).

**SDD-010 — ACCOUNT_LOCKED not handled**
  → Was this omitted intentionally or accidentally?

**SAD-003 — checkLockout() not implemented**
  → Is this item still pending?

### Undocumented Code

- `normalizeEmail(email: string)` — no SDD item
  → Private helper? Add as SDD item if non-trivial logic.

### Test Coverage

| Item | Test File | Status |
|------|-----------|--------|
| UT-010 | tests/ut/auth.test.ts | ✅ stub present |
| UT-011 | tests/ut/auth.test.ts | ✅ stub present |
| UT-012 | tests/ut/auth.test.ts | ❌ no test case found |
| AT-005 | tests/at/login.test.ts | ✅ stub present |
| SIT-003 | tests/sit/          | ❌ no file found |

### Ready to Promote

No items are ready to promote — resolve deviations first.
```

---

## Constraints

- **Never write or rewrite source code.** Even to fix a mismatch.
- **Never generate test code.** Report missing tests; the human writes them.
- **Never silently accept deviations.** Every mismatch is reported and requires a human decision.
- **If the code is better than the spec**, report it as an extra and ask whether SDD should be updated — do not assume the spec is wrong.
