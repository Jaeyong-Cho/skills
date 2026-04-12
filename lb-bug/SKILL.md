---
name: lb-bug
description: |
  Use this skill when the user reports a bug, unexpected behavior, crash, or incorrect output. Triggers: "there's a bug", "bug report", "this isn't working", "unexpected behavior in X", "X is broken", "the output is wrong", "crash in Y". This is Workflow 2 of the literate programming development cycle. The skill diagnoses whether the bug is a book problem (wrong design), a code problem (code diverged from book), or both — and fixes whichever is wrong.
---

# lb-bug: Handle a Bug Report

**Goal**: Diagnose the bug. Determine whether the book is wrong, the code diverged from the book, or both. Fix whichever is wrong. Mark all changes for human review.

Read before starting:
- `shared/references/flags.md` — DRAFT / FIX semantics
- `shared/references/source-refs.md` — how to locate and verify symbols

---

## Steps

### 1. Locate the relevant book section

Search the book for the feature or component involved:

```bash
grep -rn "<keyword>" book/src/
```

Read the chapter. Understand what the book says the behavior should be.

### 2. Locate the relevant source code

```bash
grep -rn "<keyword>" src/
```

Read the implementation. Understand what the code actually does.

### 3. Diagnose

Compare book vs code vs reported behavior:

| Situation | Root cause | Action |
|-----------|-----------|--------|
| Book describes wrong behavior | Design flaw | Fix the book; mark `DRAFT`; add `FIX` for downstream code |
| Code diverged from correct book | Implementation drift | Fix the source code directly; add `FIX` in book noting the divergence |
| Both book and code are wrong | Design + drift | Fix book first (it's source of truth); mark `DRAFT`; add `FIX` for code |
| Bug is in uncharted territory (no book coverage) | Missing documentation | Write the missing chapter; mark `DRAFT`; add `FIX` for the code fix |

### 4a. If the book is wrong

Rewrite the incorrect section. Every changed section gets a `DRAFT` flag:

```markdown
<!-- DRAFT: corrected the session invalidation design — the denylist IS stateful, not stateless as previously written -->
```

If the code also needs updating as a consequence, place a `FIX` flag in the relevant book section:

```markdown
<!-- FIX: book now says denylist must be persisted to Redis — src/services/AuthService.ts currently stores it in-memory; update to use Redis -->
```

### 4b. If the code diverged from the book

Fix the source code directly to match the book. Verify the fix:

```bash
grep -n "functionName" path/to/file
```

Add a `FIX` flag in the book at the relevant section to note the divergence was found and resolved:

```markdown
<!-- FIX: code had diverged — AuthService.logout() was not invalidating tokens in Redis as the book specified; fixed in src/services/AuthService.ts -->
```

This flag stays until the human reviews and removes it.

### 4c. If both are wrong

Fix the book first. Mark `DRAFT`. Then add `FIX` flags for the code — **do not fix the code until the book is reviewed**, because the correct behavior isn't confirmed yet.

### 5. Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

### 6. Report

Summarize:
- What the bug was
- Root cause (book wrong / code diverged / both / undocumented)
- What was changed and where
- Which flags were placed and why
- What the user needs to review

---

## Output State

Root cause identified. Book or code (or both) corrected. Human review requested via `DRAFT` and `FIX` flags. If both were wrong, code is NOT yet fixed — waiting for book review first.
