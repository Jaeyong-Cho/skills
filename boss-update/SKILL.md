---
name: boss-update
description: |
  Use this skill when the user provides new or changed customer requirements (CuRS) and wants the BOSS documents updated. Triggers: "update the docs with this requirement", "I have a new requirement", "add this to the spec", "the customer wants X", "update vdoc", or any time the user describes what the software should do. This is the core workflow skill. AI drafts CuRS → SRS → SAD → SDD → test items, marks them DRAFT, and provides review points. No source code is written.
---

# boss-update: Update BOSS from Customer Input

**Goal**: Translate customer intent (CuRS) into a cascade of draft items across SRS → SAD → SDD → AT/SIT/UT. Mark all new/changed items `draft`. Provide consolidated review points. Write no source code.

Read before starting:
- `references/items.md` — item format, ID system, states, tags, traceability links
- `references/structure.md` — per-document conventions, SAD/SDD specificity requirements
- `references/review-points.md` — how to write review points

---

## Step 1: Orient — read state and find relevant existing items

### 1a. Next available IDs

```bash
ls book/src/curs/ | grep "^CuRS-[0-9]" | sort -t- -k2 -n | tail -1
ls book/src/srs/  | grep "^SRS-[0-9]"  | sort -t- -k2 -n | tail -1
ls book/src/sad/  | grep "^SAD-[0-9]"  | sort -t- -k2 -n | tail -1
ls book/src/sdd/  | grep "^SDD-[0-9]"  | sort -t- -k2 -n | tail -1
ls book/src/at/   | grep "^AT-[0-9]"   | sort -t- -k2 -n | tail -1
ls book/src/sit/  | grep "^SIT-[0-9]"  | sort -t- -k2 -n | tail -1
ls book/src/ut/   | grep "^UT-[0-9]"   | sort -t- -k2 -n | tail -1
```

### 1b. Find relevant existing items (before writing anything new)

Check for existing coverage to avoid duplicates and to find items to link:

```bash
# Does any SRS item already cover this topic? (keyword search)
grep -ril "<keyword>" book/src/srs/

# Does any SAD item already own this component?
grep -ril "<component-name>" book/src/sad/

# Does any SDD item already design this function?
grep -ril "<function-name>" book/src/sdd/

# Which items share relevant tags?
grep -rl "#<tag>" book/src/
```

Read the full content of any item that looks relevant:

```bash
cat book/src/srs/SRS-007.md    # read a specific item
head -20 book/src/sad/SAD-003.md  # read just header fields quickly
grep -A10 "^\*\*Traces\*\*" book/src/sad/SAD-003.md  # read only traces
```

### 1c. Read tag registry

```bash
cat book/src/tags.md
```

Determine which existing tags apply to the new items, and which new tags are needed.

---

## Step 2: Write CuRS item(s)

Create a new file `book/src/curs/CuRS-{NNN}.md`. Record the customer's input as-is — do not interpret or reformulate yet.

```markdown
# CuRS-{NNN}: <short title>

**State**: `draft`
**Tags**: `#tag1` `#tag2`
**Traces**:
- → [SRS-{NNN}](../srs/SRS-{NNN}.md): <explain which aspect of this customer input is being formalized into a requirement and why it requires its own SRS item>

**Input** (verbatim or near-verbatim):
> "<customer's words>"

**Context**: <when this was stated and any relevant background>

> **Review needed** — confirm this captures the customer's intent accurately; note any assumptions made in transcription
```

Then add the item to `SUMMARY.md` under Customer Requirements:
```markdown
  - [CuRS-{NNN}: <title>](./curs/CuRS-{NNN}.md)
```

And add a row to `book/src/curs/index.md` traceability table.

---

## Step 3: Derive SRS items

For each CuRS item, create one or more files `book/src/srs/SRS-{NNN}.md`. Each SRS item must:
- Be testable (an AT can be written for it)
- State what the system shall do, not how
- Trace upstream to CuRS and downstream to SAD + AT

If a CuRS item is ambiguous, write the most likely interpretation and flag it.

```markdown
# SRS-{NNN}: <requirement title>

**State**: `draft`
**Tags**: `#tag1` `#tag2`
**Traces**:
- ← [CuRS-{NNN}](../curs/CuRS-{NNN}.md): <explain why this requirement is a direct derivation of that customer input, including any assumptions added beyond what the customer literally said>
- → [SAD-{NNN}](../sad/SAD-{NNN}.md): <explain why this particular component is the architectural response to this requirement>
- → [AT-{NNN}](../at/AT-{NNN}.md): <explain what aspect of this requirement the acceptance test validates>

<Requirement text. Use "shall" for mandatory, "should" for preferred.>

> **Review needed** — <specific question: scope, ambiguity, or assumption to verify>
```

Add to `SUMMARY.md` under Software Requirements, and add a row to `book/src/srs/index.md`.

---

## Step 4: Update or create SAD items

For each new SRS item, identify which architectural component handles it. Create `book/src/sad/SAD-{NNN}.md`. If an existing SAD item must change, edit it and reset its state to `draft`.

SAD items must be concrete enough for the human to create files and directories:

```markdown
# SAD-{NNN}: <component or structure title>

**State**: `draft`
**Tags**: `#tag1`
**Traces**:
- ← [SRS-{NNN}](../srs/SRS-{NNN}.md): <explain which requirement(s) this component satisfies and why this component boundary was chosen to satisfy it>
- → [SDD-{NNN}](../sdd/SDD-{NNN}.md): <explain which function or class in the detailed design implements the core responsibility of this component>
- → [SIT-{NNN}](../sit/SIT-{NNN}.md): <explain what integration scenario between components this test covers>

**Location**: `src/<path>/<FileName>.{ext}`
**Responsibility**: <single sentence — what this component does>
**Dependencies**: <other SAD components this depends on>
**Interface**:
- `<methodName>(params) → ReturnType` — <one-line description>

> **Review needed** — <question about component boundary, naming, or interface>
```

If this is the first SAD item or directory structure has changed, update `book/src/sad/SAD-001.md` to reflect the full directory tree.

Add to `SUMMARY.md` under Architectural Design, and add a row to `book/src/sad/index.md`.

---

## Step 5: Create or update SDD items

For each function or class in a SAD component, create `book/src/sdd/SDD-{NNN}.md`. SDD items must be detailed enough for the human to write the implementation without guessing:

```markdown
# SDD-{NNN}: <ClassName.methodName() or module-level function>

**State**: `draft`
**Tags**: `#tag1`
**Traces**:
- ← [SAD-{NNN}](../sad/SAD-{NNN}.md): <explain why this function is the implementation of a specific responsibility declared in the parent SAD component>
- → [UT-{NNN}](../ut/UT-{NNN}.md): <explain which behavior of this function the unit test covers>

**Signature**: `<functionName>(param: Type, ...): ReturnType`

**Algorithm**:
1. <Step 1 — specific action, not vague>
2. <Step 2>
3. ...

**Variables**:
- `<varName>: <Type>` — <purpose>

**Error cases**:
- `<ErrorType>` — <when this is raised>

**Side effects**: <what is written/read beyond the return value, or "none">

> **Review needed** — <question about algorithm detail, error handling, or edge case>
```

Add to `SUMMARY.md` under Detailed Design, and add a row to `book/src/sdd/index.md`.

---

## Step 6: Write test items

For each new SRS/SAD/SDD item, create the corresponding test file.

**AT item** — create `book/src/at/AT-{NNN}.md` (traces SRS — black-box, user perspective):
```markdown
# AT-{NNN}: <test title>

**State**: `draft`
**Tags**: `#tag1`
**Traces**:
- ← [SRS-{NNN}](../srs/SRS-{NNN}.md): <explain which "shall" statement this test verifies, and why this scenario is sufficient to confirm compliance>

**Preconditions**: <system state before test>
**Steps**:
1. <action>
2. <action>
**Expected result**: <observable outcome — specific and measurable>
**Failure criterion**: <what makes this test fail>

> **Review needed** — <question about test scope or pass criterion>
```

**SIT item** — create `book/src/sit/SIT-{NNN}.md` (traces SAD — component interaction):
```markdown
# SIT-{NNN}: <test title>

**State**: `draft`
**Tags**: `#tag1`
**Traces**:
- ← [SAD-{NNN}](../sad/SAD-{NNN}.md): <explain which interface boundary this test exercises and why testing this interaction point is necessary>

**Components under test**: <ComponentA> ↔ <ComponentB>
**Scenario**: <what interaction is being verified>
**Expected behavior**: <specific observable outcome>

> **Review needed** — <question about test boundary or mock strategy>
```

**UT item** — create `book/src/ut/UT-{NNN}.md` (traces SDD — function level):
```markdown
# UT-{NNN}: <test title>

**State**: `draft`
**Tags**: `#tag1`
**Traces**:
- ← [SDD-{NNN}](../sdd/SDD-{NNN}.md): <explain which specific algorithm step, error case, or behavior defined in SDD this test case is validating>

**Function**: `<functionName>()`
**Case**: <what specific case this tests>
**Input**: <specific input values>
**Expected output**: <specific return value or side effect>

> **Review needed** — <question about edge case coverage>
```

Add each test item to `SUMMARY.md` under its respective section, and add a row to the corresponding index file.

---

## Step 7: Update tags.md

For every new tag used, add a row to the tag registry. Update item counts for all affected tags.

```bash
# Find all tags in use across all item files
grep -rh "#[a-z]" book/src/curs/ book/src/srs/ book/src/sad/ \
  book/src/sdd/ book/src/at/ book/src/sit/ book/src/ut/ \
  | grep -o "#[a-z-]*" | sort | uniq -c | sort -rn
```

---

## Step 8: Update traceability summaries

Update the traceability table at the top of each affected document to include the new items.

---

## Step 9: Build check

```bash
cd book && mdbook build 2>&1 | tail -20
```

Fix all broken links and build errors before reporting.

---

## Step 10: Report review points

End every session with a consolidated review summary. See `references/review-points.md` for format.

```
## Items Updated

| ID | Title | State | Type |
|----|-------|-------|------|
| CuRS-003 | ... | draft | new |
| SRS-007  | ... | draft | new |
| SAD-003  | ... | draft | new |
| SAD-001  | ... | draft | updated (directory structure) |
| SDD-010  | ... | draft | new |
| AT-005   | ... | draft | new |
| SIT-003  | ... | draft | new |
| UT-010   | ... | draft | new |

## Review Points

### Must Resolve
- [ ] SRS-007: ...
- [ ] SAD-003: ...

### Should Verify
- [ ] SDD-010: ...

### For Awareness
- [ ] Tags added: #lockout
```

---

## Constraints

- **Never write source code.** Not even pseudocode in a function body — that is SDD's algorithm field.
- **Never promote state.** AI sets `draft`. Human promotes to `reviewed` or `done`.
- **SAD must name files.** If a SAD item introduces a component, it must specify the exact file path.
- **SDD must be implementable.** If you cannot describe the algorithm step-by-step, place a `> **Review needed**` blockquote asking the human for clarification instead of writing a vague description.
- **Every test item traces to exactly one upstream item.** Do not write a test that covers multiple SRS/SAD/SDD items.
