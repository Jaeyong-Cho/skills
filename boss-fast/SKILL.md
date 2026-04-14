---
name: boss-fast
description: |
  Quick, surgical fixes OR rapid prototyping using BOSS documentation context — no full review workflow needed. Two modes:
  • FIX: small known correction to docs or code (rename, typo, tag, broken link, minor bug)
  • PROTOTYPE: generate a quick working spike/prototype for a specific item by reading just enough BOSS context (SDD → SAD → SRS), without the full rigor of boss-impl. Great for testing an approach before committing to it.
  Triggers: "boss-fast", "rename this item", "fix the title of SRS-007", "typo in SAD-003", "fix the link", "minor fix", "quick doc edit", "rename this function", "small code fix", "prototype SDD-010", "quick prototype for SAD-003", "spike this", "draft a quick impl for", "test this approach", "prototype mode", "write a rough version of", "just get something working for".
  Use this instead of boss-srs / boss-sad / boss-sdd / boss-curs / boss-impl when the change is small or you want a fast throwaway prototype to validate an idea.
---

# boss-fast: Quick Fix or Prototype

**Two modes** — pick based on what the user wants:

- **Fix mode**: apply a small, known correction to BOSS docs or source/test code
- **Prototype mode**: generate a rough working implementation for a BOSS item using its doc context as a spec, skipping full rigor in favour of speed

---

---

## Decide the mode

If the user mentions "prototype", "spike", "rough version", "quick impl", or "test this approach" → use **Prototype mode** (skip to the Prototype section below).

Otherwise → use **Fix mode** (follow Steps 1–5 below).

---

## FIX MODE

---

## Step 1: Clarify the fix

If the user hasn't specified exactly what to change, ask one targeted question. You need:

- **What to fix** — which item ID, file path, or function name
- **What field or location** — title, description, tag, trace link, function name, constant value, …
- **What the new value is**

If the user's message already has all three, skip this step.

---

## Step 2: Locate the file and read it

Read the relevant file before editing so you understand the current content.

For a BOSS item:
```bash
cat book/src/<layer>/<ID>.md
```

For source or test code, locate the file first if the path wasn't given:
```bash
grep -rn "<function or symbol name>" src/ tests/
```

---

## Step 3: Apply the fix

Make only the targeted edit. Don't touch unrelated fields or lines.

**Doc rules:**
- Preserve formatting: state backticks, tag backticks, trace arrow characters (←, →, ↔).
- Never promote `draft` → `reviewed` as a side effect — state changes are the human's job.

**Code rules:**
- Match the existing style (indentation, naming convention, etc.).
- If the fix is a rename, change every occurrence in that file — don't leave a mix of old and new names.

---

## Step 4: Update secondary references

### Doc fixes — what cascades

**If the item title (H1) changed:**

SUMMARY.md:
```bash
grep -n "<ID>" book/src/SUMMARY.md
```
Update the display text: `- [<ID>: <new title>](./<layer>/<ID>.md)`

index.md for this layer:
```bash
grep -n "<ID>" book/src/<layer>/index.md
```

Other items whose trace descriptions name this item by title:
```bash
grep -rl "\[<ID>\]" book/src/
```
Update only the description text; link targets (file paths) don't change.

**If a tag was added or removed:**

Update the item count in `book/src/tags.md`. If the tag is brand new, add a row for it.

**If a traceability link was fixed:**

Check the counterpart file — if you fixed `SRS-007 → SAD-003`, verify `SAD-003` has a matching `← SRS-007` entry and fix it if not.

### Code fixes — what cascades

**If a function or symbol was renamed:**

Check callers across the codebase:
```bash
grep -rn "<old name>" src/ tests/
```
Update all call sites. Also check whether the corresponding SDD item's `## Signature` field still matches — if it doesn't, update it too.

**If a test file was changed:**

Make sure the change doesn't break the relationship between the test and its BOSS UT/AT/SIT item. If the test ID comment or item reference in the file is now wrong, fix it.

---

## Step 5: Report

List every file changed and what changed in each, one line per file:

```
✓ book/src/srs/SRS-007.md      — title: "User auth" → "User authentication via email"
✓ book/src/SUMMARY.md          — updated display text for SRS-007
✓ book/src/srs/index.md        — updated link text in traceability table
✓ src/auth/AuthService.ts      — renamed checkLockout() → checkLockoutStatus()
✓ tests/ut/ut-010/test.ts      — updated call site for renamed function
```

If you noticed something else wrong but weren't asked about it, mention it briefly rather than fixing it silently.

---

## PROTOTYPE MODE

**Goal**: Read the minimum BOSS context needed for a specific item and write a rough, runnable implementation — fast. The output is a throwaway spike, not production code.

---

### P1: Identify the target item

The user should name a specific item (e.g. `SDD-010`, `SAD-003`). If they haven't, ask for one.

For an SDD item → the prototype is a function or class.
For an SAD item → the prototype is a component skeleton (file + basic interface).

---

### P2: Read just enough context

Read the target item and one level up — no more than needed:

```bash
# Target item
cat book/src/<layer>/<ID>.md

# Direct upstream (the "why" and interface contract)
# For SDD → read its parent SAD item
# For SAD → read the SRS items it traces to
```

Extract the key facts you need to write code:
- **Signature / Interface** — what the function or component exposes
- **Algorithm / Responsibility** — what it must do
- **Dependencies** — what it calls or receives
- **Error cases** — what it must handle

Stop reading when you have enough to write something runnable. Don't read the full chain (CuRS → SRS → SAD → SDD → UT) — that's boss-impl's job.

---

### P3: Write the prototype

Write lean, direct code. Rules for prototypes:

- **Goal is runnable, not perfect.** Stubs, hardcoded values, and simplified logic are fine if they let you test the core idea.
- **Mark assumptions.** When you skip something the spec asks for (e.g. error handling, persistence), leave a `// TODO: per <ID>` comment so it's obvious what was deferred.
- **Match the project's language.** Check existing `src/` files for the language and import style — use the same.
- **No new doc updates.** Don't touch BOSS items, SUMMARY.md, or index.md — this is throwaway code.

Place the prototype in a clearly temporary location:
```
prototypes/<ID>-spike.<ext>
```
or inline in the conversation if the user prefers.

---

### P4: Summarise what was skipped

After writing, list the spec requirements that were intentionally left out of the prototype:

```
Skipped for speed:
- Lockout counter persistence (SDD-010: Side effects)
- bcrypt cost factor config (SDD-010: Review needed)
- Full AuthError enum (SAD-003: Interface)

Next step: run boss-impl for SDD-010 to get the production version.
```

This keeps the human in control of what still needs to be done properly.
