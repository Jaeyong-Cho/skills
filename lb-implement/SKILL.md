---
name: lb-implement
description: |
  Use this skill to implement source code from approved IMPLEMENT flags in the literate book. Triggers: "implement the book", "code up the IMPLEMENT flags", "do the implementation", "implement the pending items", "write the code for the book", "implement X from the book". This is Workflow 4 of the literate programming development cycle. Only processes IMPLEMENT flags — the design is already approved; this skill writes the code exactly as the book describes.
---

# lb-implement: Implement from the Book

**Goal**: For each `IMPLEMENT` flag in the book, write the corresponding source code exactly as described. The design is already approved — do not make design decisions here.

Read before starting:
- `references/flags.md` — IMPLEMENT flag semantics
- `references/source-refs.md` — how source references are formatted in the book

---

## Step 1: Scan for IMPLEMENT flags

```bash
grep -rn "<!-- IMPLEMENT:" book/src/
```

List every flag with its file and line number. Report to the user before acting.

---

## Step 2: For each IMPLEMENT flag

### 2a. Read the flag and its context

Read the flag description carefully. Then read 60+ lines of surrounding book content to understand:
- What the function/class must do
- What inputs and outputs are expected
- What invariants or constraints apply
- How it fits into the surrounding design

### 2b. Locate the target file

The flag description should name the file and symbol:  
`src/services/AuthService.ts :: AuthService.refreshToken`

Check whether the file exists:
```bash
ls path/to/file 2>/dev/null || echo "file does not exist"
```

If the file doesn't exist, create it with the appropriate module structure for the codebase (check existing files for conventions — imports, export style, class structure).

### 2c. Check for existing symbol

```bash
grep -n "refreshToken\|AuthService" path/to/file
```

- If the symbol exists and needs modification: edit in place
- If the symbol doesn't exist: add it in the appropriate location within the file

### 2d. Write the code

Implement **exactly what the book describes**. Do not:
- Add features not mentioned in the book
- Refactor surrounding code
- Make architectural decisions not already present in the book

If the flag description is ambiguous or contradicts existing code, **do not guess**. Place a `DRAFT` flag in the book asking for clarification and skip this item.

### 2e. Remove the IMPLEMENT flag

After successfully implementing, delete the `<!-- IMPLEMENT: ... -->` line from the book markdown.

---

## Step 3: Verify

After all implementations:

```bash
# Check symbols exist
grep -n "functionName" path/to/file

# Build the book (ensures no broken references)
cd book && mdbook build 2>&1 | tail -20
```

If the project has a build or type-check step, run it:
```bash
# e.g. for TypeScript:
npx tsc --noEmit 2>&1 | tail -20
```

---

## Step 4: Report

For each IMPLEMENT flag processed:

```
FLAG: src/services/AuthService.ts :: AuthService.refreshToken
FILE: src/services/AuthService.ts
ACTION: Added refreshToken() method — validates token within 1h expiry window, issues new JWT
STATUS: IMPLEMENT flag removed from book/src/authentication/tokens.md:34

FLAG: src/middleware/rateLimit.ts :: rateLimitMiddleware  
FILE: src/middleware/rateLimit.ts (created)
ACTION: Created file; implemented token bucket rate limiter with Redis backend
STATUS: IMPLEMENT flag removed from book/src/rate-limiting.md:67

SKIPPED: book/src/authentication/sessions.md:12
REASON: Flag description ambiguous — "update session store" doesn't specify what to update
ACTION: Placed DRAFT flag asking for clarification
```

End with: X implemented, Y skipped (with reasons).

---

## Output State

All unambiguous `IMPLEMENT` flags resolved. Source code written to match the book exactly. `IMPLEMENT` flags removed. Ambiguous flags escalated to `DRAFT`. Book builds cleanly.

---

## Constraint

The book is the source of truth. If the book says X, implement X. If you think X is the wrong approach, do not silently implement Y — place a `DRAFT` flag explaining the concern and wait for human decision.
