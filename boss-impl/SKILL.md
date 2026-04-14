---
name: boss-impl
model: haiku
description: |
  BOSS implementation skill. Use this to implement source code for a specific BOSS item (SDD, SAD component, or a named feature). Reads the full upstream context (SDD → SAD → SRS → CuRS) and downstream test items (UT), then writes code that strictly follows the spec. When a conflict or ambiguity blocks implementation, writes a review point on the relevant item instead of guessing.
  Triggers: "boss-impl", "implement SDD-010", "implement SAD-003", "implement the auth module", "write the code for SDD-012", "boss implement", "implement this item".
  Use this whenever the human wants AI to write source code driven by BOSS documents — even if they say "just implement it" or "write the code" while a BOSS book is present.
---

# boss-impl: Implement Code from BOSS Items

**Goal**: Write source code that exactly matches reviewed BOSS items — the right file location, the right function signature, the right algorithm steps. When something in the spec is unclear or contradictory, write a review point on the item rather than guessing. Never deviate silently.

---

## Step 1: Determine scope

Infer the target from the human's message:

- `"implement SDD-010"` → single SDD item
- `"implement SAD-003"` → all SDD items under that SAD component
- `"implement the auth module"` → find the relevant SAD component by tag or keyword, then all its SDDs
- `"implement everything ready"` → all reviewed SDD items not yet `done`

```bash
# Find reviewed SDD items not yet done
grep -rl "^\`reviewed\`" book/src/sdd/ | sort

# Find all SDD items under a SAD component
grep -rl "\[SAD-003\]" book/src/sdd/

# Find SDD items by keyword
grep -rl "authenticate" book/src/sdd/
```

If the scope is ambiguous, ask: "I found these items — implement all of them, or just some?"

---

## Step 2: Check readiness

Only implement items in `reviewed` state. If a target item is still `draft`, stop and tell the human:

```
SDD-010 is still `draft` — it has unanswered review points. Run boss-sdd first to resolve them before implementing.
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
cat book/src/sdd/SDD-{NNN}.md

# Read its parent SAD (for file location, component responsibility)
grep "← \[SAD-" book/src/sdd/SDD-{NNN}.md
cat book/src/sad/SAD-{MMM}.md

# Read the SRS items traced from that SAD (for the requirement intent)
grep "← \[SRS-" book/src/sad/SAD-{MMM}.md
cat book/src/srs/SRS-{KKK}.md
```

**Downstream** (what tests must pass):
```bash
# Read linked UT items
grep "→ \[UT-" book/src/sdd/SDD-{NNN}.md
cat book/src/ut/UT-{NNN}.md
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

## Step 5: Implement

Write the code following the SDD exactly:

| SDD field | What it drives |
|-----------|---------------|
| `## Signature` | Function name, parameter names, types, return type — match exactly |
| `## Algorithm` | Each numbered step becomes identifiable code — don't collapse or reorder steps |
| `## Variables` | Use the variable names and types listed |
| `## Error cases` | Every error case must be handled — no silent omissions |
| `## Side effects` | Honor what's declared; if "none", don't add any |

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

This is the right behavior because the spec is the source of truth. If the spec is unclear, fixing the spec is more valuable than guessing — a wrong guess here can cascade into UT failures and a sad review cycle later.

---

## Step 6: Create test stubs

For each UT item linked from the implemented SDDs, check if a test stub exists:

```bash
ls tests/ut/
grep -rn "UT-{NNN}\|{functionName}" tests/ut/
```

If no stub exists, create one — a minimal test function that names the case and has a `pass`/`todo` body. Do not write the test assertions; the human does that after reviewing the UT item.

```python
# UT-010: authenticate — happy path
def test_authenticate_happy_path():
    pass  # TODO: implement per UT-010

# UT-011: authenticate — wrong password
def test_authenticate_wrong_password():
    pass  # TODO: implement per UT-011
```

For SIT stubs (`tests/sit/`) and AT stubs (`tests/at/`), apply the same pattern only if the SAD or SRS item is in scope.

---

## Step 7: Build check

```bash
# Language-appropriate check — pick the right one for the project
cd book && mdbook build 2>&1 | tail -20

# For Python
python -m py_compile src/<file>

# For TypeScript
npx tsc --noEmit
```

Fix syntax errors. Do not fix logic errors by diverging from the spec — if the spec leads to a syntax error, that's a review point too.

---

## Step 8: Report

```
## Implementation Report

### Implemented
| SDD | Function | File |
|-----|----------|------|
| SDD-010 | AuthService.authenticate() | src/auth/auth_service.py |
| SDD-011 | AuthService.checkLockout() | src/auth/auth_service.py |

### Test Stubs Created
| UT | File |
|----|------|
| UT-010 | tests/ut/test_auth_service.py |
| UT-011 | tests/ut/test_auth_service.py |
| UT-012 | tests/ut/test_auth_service.py |

### Blocked — Review Points Added
| Item | Problem |
|------|---------|
| SDD-012 | Algorithm step 3 refers to "the session store" but SAD-004 lists two possible adapters (Redis and in-process) without specifying which. Added review point to SDD-012. |

### Next steps
- Answer the review point in SDD-012, then run **boss-sdd** to apply it
- Run **boss-codereview** to verify conformance when all items are unblocked
- Write test assertions in the stubs, following each UT item's Input/Expected output
```

---

## Constraints

- **Follow the SDD exactly.** If the SDD says `bcrypt`, use bcrypt. If it says 12 rounds, use 12. Do not substitute equivalent libraries or adjust parameters without a review point.
- **Never promote item state.** Leave all items as `reviewed`. boss-codereview is the step that moves items to `done`.
- **Never silently deviate.** Any gap between the spec and what you wrote must appear in the report.
- **Never delete existing code** unless an SDD item explicitly describes replacing it. When in doubt, ask.
