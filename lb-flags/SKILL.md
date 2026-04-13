---
name: lb-flags
description: |
  Use this skill to process flags in the literate book. Triggers: "process the flags", "handle the DRAFTs", "work through the flags", "resolve the book flags", "check the flags", "there are DRAFTs to process", "fix the FIX flags". This is Workflow 3 of the literate programming development cycle. The skill scans all DRAFT and FIX flags in book/src/, understands human intent from context, and revises book content accordingly. IMPLEMENT flags are NOT processed here — they are handled by lb-implement.
---

# lb-flags: Process Book Flags

**Goal**: Scan the book for `DRAFT` and `FIX` flags. Understand human intent from surrounding context and edits. Revise book content. Do not touch `IMPLEMENT` flags.

Read before starting:
- `references/flags.md` — flag semantics and promotion rules
- `references/writing.md` — narrative style when revising sections

---

## Step 1: Scan all flags

```bash
grep -rn "<!-- DRAFT:\|<!-- IMPLEMENT:\|<!-- FIX:" book/src/
```

List every flag found with its file and line number. Report this list to the user before acting.

---

## Step 2: Process each flag

Process in this order: `FIX` first (correctness), then `DRAFT` (content quality).  
Skip all `IMPLEMENT` flags — note them in the report but do not act on them.

---

### DRAFT flags

A `DRAFT` flag means the human has seen this AI-written content and either:
- Left it as-is (wanting a revision based on adjacent edits they made), or
- Added a comment nearby explaining what they want changed

**How to determine what the human wants**:
1. Read 60+ lines above and below the flag
2. Look for inline edits the human made adjacent to the draft content
3. Look for any comment or note near the flag
4. If intent is genuinely unclear — place a new `DRAFT` flag asking a specific question; do not guess

**Action**:
- Revise the section based on the human's evident intent
- Replace the old `DRAFT` flag with a new `DRAFT` flag describing what was revised:

```markdown
<!-- DRAFT: revised token expiry section — reduced window from 24h to 1h per human edit; added note about refresh token flow -->
```

The human must re-review after any AI revision.

---

### FIX flags

A `FIX` flag means something is identified as wrong — either by the human or by a previous AI run.

**How to process**:
1. Read the flag description and 60+ lines of context
2. Check both the book and the relevant source code to determine ground truth
3. Decide what is actually wrong: book, code, or both

| What's wrong | Action |
|-------------|--------|
| Book is wrong | Fix the book prose/diagram; replace `FIX` with `DRAFT` (human reviews correction) |
| Code diverged from correct book | Fix the source code; remove the `FIX` flag; note the code change in report |
| Both wrong | Fix book first; replace `FIX` with `DRAFT`; add new `FIX` for the code change needed |

**Do not remove a `FIX` flag without either fixing the problem or escalating to `DRAFT`.**

---

## Step 3: Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix any build errors introduced during edits.

---

## Step 4: Report

For every flag found, report:

```
FILE: book/src/authentication/sessions.md:42
FLAG: DRAFT
ACTION: Revised — shortened expiry window from 24h to 1h, added refresh token note
NEW FLAG: DRAFT (awaiting re-review)

FILE: book/src/rate-limiting.md:88  
FLAG: FIX
ACTION: Book was wrong — token bucket description didn't match implementation; corrected prose
NEW FLAG: DRAFT (awaiting review of correction)

FILE: book/src/authentication/tokens.md:15
FLAG: IMPLEMENT
ACTION: Skipped — handled by lb-implement
```

End with a summary count: X DRAFT revised, Y FIX resolved, Z IMPLEMENT skipped.

---

## Output State

All `DRAFT` and `FIX` flags processed or escalated. New `DRAFT` flags placed for human re-review. `IMPLEMENT` flags untouched. Book builds cleanly.
