---
name: sophist-sync
description: |
  Sync existing .sophist documents to the current skill templates. Use this when sophist-* skills have been updated (new item sections added, templates changed) and existing items are missing the new fields.
  Triggers: "sophist-sync", "sync the docs", "update existing items to new template", "my items are missing sections", "add debug strategy to existing items", "bring items up to date", "sync existing sophist items", "the template changed", "items are outdated", "apply new template to existing items".
  Use this whenever sophist-* skills have been changed and existing items no longer match the current templates.
---

# sophist-sync: Sync Existing Items to Current Templates

**Goal**: Detect gaps between existing `.sophist` items and the current skill templates, then fill them by inferring content from each item's existing content. When a sophist-* skill adds a new section (e.g. `## Debug strategy`, `## Debug trace`), this skill finds every item missing that section and writes it — not a blank template shell, but a real first draft reasoned from what the item already says.

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

## Step 2: Define the expected schema

The current required sections for each item type. Scan each item file and check for these headings. Missing = that `## Heading` does not appear anywhere in the file.

| Layer | Required sections (in order) |
|-------|------------------------------|
| CuRS  | State · Tags · Why · Traces · Input · Context |
| SRS   | State · Tags · Why · Traces · Description |
| SAD   | State · Tags · Why · Traces · Static View · Dynamic View · Location · Responsibility · Dependencies · Interface · **Debug strategy** |
| SDD   | State · Tags · Why · Traces · Static View · Dynamic View · Signature · Algorithm · Variables · Error cases · Side effects · **Debug trace** |
| AT    | State · Tags · Why · Traces · Function · Case · Input · Expected output |
| SIT   | State · Tags · Why · Traces · Diagram · Components under test · Scenario · Expected behavior |
| UT    | State · Tags · Why · Traces · Function · Case · Input · Expected output |

> **Update this table whenever a sophist-* skill template changes.** This table is the source of truth for what "up to date" means.

Skip items in `deprecated` state — they do not need to be synced.

---

## Step 3: Scan and report drift

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
| SDD-010 | ## Debug trace |
| SDD-011 | ## Debug trace |
| SDD-012 | ## Debug trace |

### Everything else: up to date ✓
```

If nothing is missing, tell the human and stop — no changes needed.

Ask for confirmation before proceeding: "Ready to fill these sections. Should I go ahead?"

---

## Step 4: Infer and fill missing sections

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
**Diagnostic process**: <ordered steps — check entry log first, then each downstream call in sequenceDiagram order, then check error paths>

**Debug data** (written to `--debug-output-dir` when enabled):

| File | Format | When written | Contents |
|------|--------|-------------|---------|
| `<component-slug>-state.json` | JSON | on error | <key fields from Interface parameters and any intermediate state> |
```

### Filling `## Debug trace` in SDD items

Read:
- `## Algorithm` — numbered steps drive the happy path trace
- `## Error cases` — each entry drives an error path trace
- `## Variables` — named variables are the key observables
- `## Dynamic View` — branch structure shows where paths diverge

Write the section with these fields:

```markdown
## Debug trace
**Happy path**: <one log message per significant Algorithm step — entry, key decisions, return>
**Error paths**:
- `<ErrorType from ## Error cases>`: <log messages and variable values that confirm this error fired>
**Key variables**: <most diagnostic variables from ## Variables — the ones that distinguish correct from incorrect execution>

**Debug data** (written to `--debug-output-dir` when enabled):

| File | Format | When written | Contents |
|------|--------|-------------|---------|
| `<function-slug>-entry.json` | JSON | on entry | <input parameters from ## Signature> |
| `<function-slug>-error.json` | JSON | on error | <ErrorType, error message, relevant variable values at point of failure> |
```

### Filling other missing sections

Apply the same pattern: read existing content, derive the missing section's content from it. For optional or context-dependent sections (e.g. `## Dynamic View` in simple SDDs), use judgment — if the existing content clearly doesn't need it, note that in the section rather than fabricating a diagram.

---

## Step 5: Insert sections at the correct position

Insert each new section at the position the schema table specifies — after the section that precedes it in the required order. Preserve every existing line in the file exactly.

```
## Debug strategy  →  insert after ## Interface  in SAD items
## Debug trace     →  insert after ## Side effects  in SDD items
```

---

## Step 6: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
```

Fix any broken markdown links before reporting.

---

## Step 7: Report

```
## Sync Complete

### Updated items
| Item  | Section added      | Source used for inference               |
|-------|--------------------|-----------------------------------------|
| SAD-003 | ## Debug strategy | Dynamic View sequenceDiagram + Interface |
| SAD-005 | ## Debug strategy | Dynamic View sequenceDiagram + Responsibility |
| SDD-010 | ## Debug trace   | Algorithm (6 steps) + Error cases (2)  |
| SDD-011 | ## Debug trace   | Algorithm (3 steps) + Error cases (1)  |

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

- **Infer, don't blank.** Every added section must contain content derived from the existing item. If you genuinely cannot infer something, write a targeted `> **Review needed**` blockquote explaining exactly what you couldn't determine — not a generic template placeholder.
- **Never modify existing sections.** Only add what's missing. Do not rewrite or reorder content the human has already written and reviewed.
- **Deprecated items are skipped.** Do not sync items in `deprecated` state.
- **Update the schema table when templates change.** Step 2's table is the single source of truth for what "up to date" means. When a sophist-* skill adds or removes a section from its item template, update this table in the same commit.
- **One pass per item.** If an item is missing multiple sections, add all of them in a single pass — do not make partial updates that leave the item in an inconsistent state.
