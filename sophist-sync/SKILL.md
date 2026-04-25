---
name: sophist-sync
description: |
  Sync existing .sophist documents to the current skill templates. Use this when sophist-* skills have been updated (new item sections added, templates changed) and existing items are missing the new fields.
  Triggers: "sophist-sync", "sync the docs", "update existing items to new template", "my items are missing sections", "add debug strategy to existing items", "bring items up to date", "sync existing sophist items", "the template changed", "items are outdated", "apply new template to existing items".
  Use this whenever sophist-* skills have been changed and existing items no longer match the current templates.
---

# sophist-sync: Sync Existing Items to Current Templates

**Goal**: Detect gaps between existing `.sophist` items and the current skill templates, then fill them by inferring content from each item's existing content. When a sophist-* skill adds a new section (e.g. `## Debug strategy`, `## Debug strategy`), this skill finds every item missing that section and writes it — not a blank template shell, but a real first draft reasoned from what the item already says.

If `.sophist/src/goal.md` exists, read it first — it gives you the project's purpose, which helps you infer missing sections more accurately.

The guiding principle: **infer, don't blank.** A `## Debug strategy` derived from the existing Dynamic View is immediately useful. An empty template is noise that misleads the human into thinking the section is done.

---

## Step 1: Determine scope

Ask the human (or infer from context) what prompted the sync:

- A specific section was added: "we added `## Debug strategy` to SAD items" → scan SAD only
- A specific layer is out of date: "sync all SDD items" → scan SDD only
- Full sync: "run a full sync" or no hint → scan all item types

If the human doesn't specify, default to a full scan and report before making changes.

---

## Step 2: Migrate old-format review points to header format

Before checking for missing sections, scan all item files in scope for old blockquote-style review points and convert them to the current header format.

```bash
grep -rl "> \*\*Review needed\*\*" .sophist/src/
```

For each file that matches, convert every occurrence:

**Old format (blockquote):**
```markdown
> **Review needed** — confirm this captures the customer's intent accurately
```

**New format (header):**
```markdown
### Review needed
confirm this captures the customer's intent accurately
```

**Old multi-question format:**
```markdown
> **Review needed**
> - Is the lockout threshold 5 attempts or configurable?
> - Should the error message distinguish "wrong password" from "user not found"?
```

**New format:**
```markdown
### Review needed
- Is the lockout threshold 5 attempts or configurable?
- Should the error message distinguish "wrong password" from "user not found"?
```

**Old inline answer (if present):**
```markdown
> **Answer**: 5 attempts fixed — not configurable.
```

**New format:**
```markdown
#### Answer
5 attempts fixed — not configurable.
```

Also convert `> **Validation Guide** — ...` blockquotes to `### Validation Guide` sections with bullet fields on separate lines.

Report what was migrated before proceeding to Step 3:

```
## Format Migration

| Item | Occurrences converted |
|------|-----------------------|
| SRS-007 | 1 review point |
| AT-005 | 1 review point (with answer) |
```

If nothing needed migration, note that and continue.

---

## Step 3: Define the expected schema

The current required sections for each item type. Scan each item file and check for these headings. Missing = that `## Heading` does not appear anywhere in the file.

| Layer | Required sections (in order) |
|-------|------------------------------|
| CuRS  | State · Tags · Why · Traces · Input · Context |
| SRS   | State · Tags · Why · Traces · Description |
| SAD   | State · Tags · Why · Traces · Static View · Dynamic View · Location · Responsibility · Dependencies · Interface · **Debug strategy** |
| SDD   | State · Tags · Why · Traces · Static View · Dynamic View · Signature · Algorithm · Variables · Error cases · Side effects · **Debug strategy** |
| AT    | State · Tags · Why · Traces · Function · Case · Input · Expected output |
| SIT   | State · Tags · Why · Traces · Diagram · Components under test · Scenario · Expected behavior |
| UT    | State · Tags · Why · Traces · Function · Case · Input · Expected output |

> **Update this table whenever a sophist-* skill template changes.** This table is the source of truth for what "up to date" means.

Skip items in `deprecated` state — they do not need to be synced.

---

## Step 4: Scan and report drift

For each item type in scope, list all item files and read them:

```bash
ls .sophist/src/sad/ | grep "^SAD-"
ls .sophist/src/sdd/ | grep "^SDD-"
# etc.
```

Check each file for missing section headings. Produce a drift report before touching anything:

```
## Schema Drift Report

### SAD items (2 of 4 need update)
| Item | Missing sections |
|------|-----------------|
| SAD-003 | ## Debug strategy |
| SAD-005 | ## Debug strategy |

### SDD items (3 of 6 need update)
| Item | Missing sections |
|------|-----------------|
| SDD-010 | ## Debug strategy |
| SDD-011 | ## Debug strategy |
| SDD-012 | ## Debug strategy |

### Everything else: up to date ✓
```

If nothing is missing, tell the human and stop — no changes needed.

Ask for confirmation before proceeding: "Ready to fill these sections. Should I go ahead?"

---

## Step 5: Infer and fill missing sections

For each item that needs updating, read the full item file, reason from its existing content, and write the missing section. Never insert a section that contains only unresolved template placeholders — derive real content or write a focused review point explaining what you couldn't infer.

### Filling `## Debug strategy` in SAD items

Read:
- `## Dynamic View` (`sequenceDiagram`) — the call sequence is the healthy trace
- `## Responsibility` — what failure looks like when this component breaks
- `## Interface` — the entry points and return values to instrument
- `## Dependencies` — which downstream components to rule out when debugging

Write the section with these fields:

```markdown
## Debug strategy
**Healthy trace**: <derive from sequenceDiagram: entry call → each outbound call → return; name the log messages in order>
**Key observables**: <parameters from Interface + intermediate state implied by Responsibility>
**Failure signatures**:
- <failure mode from Responsibility or child SDD error cases>: <what log pattern or absent output signals this>
**Diagnostic process**: <ordered steps for interpreting logs and data files — check entry log first, then each downstream call in sequenceDiagram order, then cross-reference data files against expected schema, then check error paths>
**Subprocess logs** (if this component invokes external processes): <list each subprocess by name; log path recorded in main log before launch; exit code and duration logged after completion>

**Debug data model** (written to `--debug-output-dir` when set — active even without `--debug-level`):

| File | Format | When written | Purpose | Contents |
|------|--------|-------------|---------|---------|
| `<component-slug>-state.json` | JSON | on error | <why this file exists — what question it answers> | <key fields from Interface parameters and any intermediate state> |
```

Notes on filling this:
- Each row in the Debug data model table is part of the component's data model — derive fields from `## Interface` parameters and `## Responsibility` state, not from generic templates.
- If the component invokes subprocesses, add a row for each subprocess log file: format `text`, when `on subprocess launch`, purpose `stdout/stderr capture for <subprocess name>`.
- The "Purpose" column is what gets logged as metadata in the main log alongside each write event — make it specific enough to be useful in isolation.

### Filling `## Debug strategy` in SDD items

Read:
- `## Algorithm` — numbered steps drive the happy path trace
- `## Error cases` — each entry drives an error path trace
- `## Variables` — named variables are the key observables
- `## Dynamic View` — branch structure shows where paths diverge

Write the section with these fields:

```markdown
## Debug strategy
**Happy path**: <one log message per significant Algorithm step — entry, key decisions, return>
**Error paths**:
- `<ErrorType from ## Error cases>`: <log messages and variable values that confirm this error fired>
**Key variables**: <most diagnostic variables from ## Variables — the ones that distinguish correct from incorrect execution>
**Analysis guide**: <how to interpret the data files and log sequence to diagnose a failure — e.g. "compare entry.json inputs against expected schema, then check if error.json exists; if absent, failure happened after the function returned">
**Subprocess logs** (if this function invokes external processes): <subprocess name → log file naming pattern; note that path and timing are recorded in main log>

**Debug data model** (written to `--debug-output-dir` when set — active even without `--debug-level`):

| File | Format | When written | Purpose | Contents |
|------|--------|-------------|---------|---------|
| `<function-slug>-entry.json` | JSON | on entry | <why — e.g. "capture inputs for replay"> | <input parameters from ## Signature> |
| `<function-slug>-error.json` | JSON | on error | <why — e.g. "capture state at failure point"> | <ErrorType, error message, relevant variable values at point of failure> |
```

Notes on filling this:
- Each Debug data model row defines the schema for one file — derive field names from `## Variables` and `## Signature`, not from generic templates.
- If the function invokes a subprocess, add a row with format `text`, when `on subprocess launch`, purpose `stdout/stderr capture`.
- The "Purpose" column is logged as metadata in the main log alongside the write event — make it specific.
- When multiple calls to the same function could produce the same filename (e.g. in a loop), note that the implementation appends a sequence index automatically (`-1`, `-2`, …).

### Filling other missing sections

Apply the same pattern: read existing content, derive the missing section's content from it. For optional or context-dependent sections (e.g. `## Dynamic View` in simple SDDs), use judgment — if the existing content clearly doesn't need it, note that in the section rather than fabricating a diagram.

---

## Step 6: Insert sections at the correct position

Insert each new section at the position the schema table specifies — after the section that precedes it in the required order. Preserve every existing line in the file exactly.

```
## Debug strategy  →  insert after ## Interface  in SAD items
## Debug strategy     →  insert after ## Side effects  in SDD items
```

---

## Step 7: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
```

Fix any broken markdown links before reporting.

---

## Step 8: Report

```
## Sync Complete

### Updated items
| Item  | Section added      | Source used for inference               |
|-------|--------------------|-----------------------------------------|
| SAD-003 | ## Debug strategy | Dynamic View sequenceDiagram + Interface |
| SAD-005 | ## Debug strategy | Dynamic View sequenceDiagram + Responsibility |
| SDD-010 | ## Debug strategy   | Algorithm (6 steps) + Error cases (2)  |
| SDD-011 | ## Debug strategy   | Algorithm (3 steps) + Error cases (1)  |

### Review recommended
The inferred sections are first drafts. Open each updated item and check:
- Do the log messages in the traces match what the implementation actually emits?
- Are the debug data file fields specific enough to implement without guessing?
- Do the failure signatures cover the failures you've actually encountered?

Run **sophist-codereview** to verify implementations cover the newly specified debug points.
```

---

## Commit message

```
docs(sophist): sync items to current template

Why: <which skill update caused the drift — e.g. "## Debug strategy added to SAD template in sophist-srs">
What: <N SAD items and M SDD items updated with the missing sections>
```

---

## Constraints

- **Infer, don't blank.** Every added section must contain content derived from the existing item. If you genuinely cannot infer something, write a targeted `### Review needed` section explaining exactly what you couldn't determine — not a generic template placeholder.
- **Never modify existing sections** — except for format migration (Step 2). Converting blockquote review points to `### Review needed` headers is a pure format change; the content is preserved. All other sections: only add what's missing, never rewrite or reorder reviewed content.
- **Deprecated items are skipped.** Do not sync items in `deprecated` state.
- **Update the schema table when templates change.** Step 2's table is the single source of truth for what "up to date" means. When a sophist-* skill adds or removes a section from its item template, update this table in the same commit.
- **One pass per item.** If an item is missing multiple sections, add all of them in a single pass — do not make partial updates that leave the item in an inconsistent state.
