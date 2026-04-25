---
name: sophist-curs
description: |
  Use this skill when the user provides new or changed customer requirements (CuRS) and wants the SOPHIST documents updated. Triggers: "sophist-curs", "update the docs with this requirement", "I have a new requirement", "add this to the spec", "the customer wants X", or any time the user describes what the software should do. Also handles reviewing answered CuRS items — triggers: "review CuRS", "I answered the CuRS items", "check CuRS review points", "show CuRS pending". AI drafts CuRS → SRS → AT items, marks them draft, and provides review points. Reviewing CuRS items marks them reviewed and updates the linked SRS items. No SAD/SDD/test stubs yet — those cascade after SRS review via sophist-srs.
---

# sophist-curs: Capture Customer Input and Draft SRS

**Goal**: Two modes depending on context.

- **Capture mode** (user provides a new/changed requirement): translate customer intent into CuRS items, derive SRS requirements, create AT items. All new items are marked `draft` with review points.
- **Review mode** (user has answered review points inline): apply answers to draft CuRS items, mark them `reviewed`, update linked SRS items if content changed.

SAD and SDD are created later by sophist-srs and sophist-sad after each layer is reviewed.

Read before starting:
- `references/items.md` — item format, ID system, states, tags, traceability links
- `references/structure.md` — per-document conventions
- `references/review-points.md` — how to write review points
- `.sophist/src/goal.md` — project goal (if it exists); read to understand what the project is for and keep new items aligned with it

---

## Detect mode

Check which mode applies:

- If the user has provided a new or changed customer requirement (a description of what the software should do) → **Capture mode**: go to Step 1.
- If the user says "review CuRS", "I answered the CuRS items", "check CuRS review points", or invokes sophist-curs with no new requirement → **Review mode**: go to the Review section below.
- If there are both (new requirement AND answered items): run Review mode first, then Capture mode.

---

## REVIEW MODE

### R1: Find all draft CuRS items

```bash
grep -rl "^\`draft\`" .sophist/src/curs/
```

Read each draft CuRS item. For each, determine its status:

- **Answered**: the `### Review needed` or `### Validation Guide` section has been removed, or its content now contains an answer added by the human
- **Pending**: the section header is still present with only the original question/guide — no answer yet

Both `### Review needed` and `### Validation Guide` sections are review points — treat them the same way.

---

### R2: Show pending review points

List every pending CuRS item clearly so the human knows what still needs attention:

```
## Pending CuRS Review Points

### CuRS-003: Password reset flow
> confirm this captures the customer's intent — does "reset" mean email-based or in-app?

### CuRS-004: Audit logging requirement
> clarify whether this applies to all user actions or only privileged ones
```

If there are no pending items, note that and move to R3.

---

### R3: Apply inline answers to answered items

For each answered CuRS item:

**If the section contains an answer added by the human:**
- Read the answer
- For `### Review needed`: incorporate the answer into `## Input`, `## Why`, or `## Context` as appropriate
- For `### Validation Guide`: update the fields in place (Purpose, Intent, Hypothesis, Validation strategy, Who validates, Success criterion) with the corrected values; also update linked AT items if the success criterion changed
- Remove the entire section (header + content)

**If the section has been removed entirely:**
- Accept the current file content as the human's approved version
- No content change needed — the human has already edited it directly

After applying all answers, the item file should have no remaining `### Review needed` or `### Validation Guide` sections. If there were multiple review sections, address each separately. Rewrite clearly — don't just append.

---

### R4: Mark answered CuRS items as `reviewed`

For each item where all review points are now resolved:

Change `## State` from `` `draft` `` to `` `reviewed` ``.

---

### R5: Update linked SRS items

For each CuRS item whose content changed during R3, read its linked SRS items via the `→ [SRS-` traces. Check whether the SRS items' `## Description`, `## Why`, or upstream trace annotation still accurately reflect the updated CuRS. If they don't:

- Update the `## Why` or trace annotation to match the corrected CuRS intent
- If the SRS Description's core requirement changed (not just clarified), reset the SRS item's state to `` `draft` `` and add a review point asking the human to confirm the SRS is still correct — the downstream design depends on it

Do not create new SAD items here. That is sophist-srs's job.

---

### R6: Update traceability and tags

- Update `.sophist/src/curs/index.md` to reflect any state changes
- Update `.sophist/src/tags.md` if tags changed

---

### R7: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
```

Fix broken links before reporting.

---

### R8: Report

```
## CuRS Review Summary

### Promoted to Reviewed
| ID | Title |
|----|-------|
| CuRS-003 | Password reset flow |

### Still Pending (answer these inline, then run sophist-curs again)
| ID | Review Question |
|----|----------------|
| CuRS-004 | Applies to all user actions or only privileged ones? |

### SRS Items Updated
| ID | What changed |
|----|-------------|
| SRS-007 | Updated Why to reflect clarified password reset intent |

---

Next: Open any pending CuRS files, write your answers inline, then run sophist-curs again.
When all CuRS items are reviewed, open the SRS files, write your answers inline, then run
sophist-srs to apply answers, mark SRS items reviewed, and generate the corresponding SAD items.
```

---

## CAPTURE MODE

## Step 1: Orient — find next IDs and assess existing coverage

### 1a. Next available IDs

```bash
ls .sophist/src/curs/ | grep "^CuRS-[0-9]" | sort -t- -k2 -n | tail -1
ls .sophist/src/srs/  | grep "^SRS-[0-9]"  | sort -t- -k2 -n | tail -1
ls .sophist/src/at/   | grep "^AT-[0-9]"   | sort -t- -k2 -n | tail -1
```

### 1b. Similarity analysis

Before writing anything, understand what's already in the book. Search with several keyword angles — the user's exact words, synonyms, the feature area, and the actor/system involved:

```bash
grep -ril "<keyword1>" .sophist/src/curs/ .sophist/src/srs/
grep -ril "<keyword2>" .sophist/src/curs/ .sophist/src/srs/
```

Read the full content of every match. For each distinct concept in the user's input, classify the coverage:

| Coverage | Meaning | Action |
|----------|---------|--------|
| **Full duplicate** | An existing CuRS+SRS already captures this intent completely | **SKIP** — no new item needed; mention the existing ID |
| **Partial overlap** | An existing item covers part of it, or it extends/clarifies the existing one | **ENHANCE** — add a section or broaden the existing item's scope |
| **Changed intent** | The customer is explicitly revising a prior requirement | **UPDATE** — modify the existing item to reflect the new intent |
| **New territory** | No existing item covers this need | **NEW** — create a full CuRS → SRS → AT chain |

Present your coverage analysis to the user in a compact table before making any changes:

```
| Concept | Closest match | Coverage | Planned action |
|---------|--------------|----------|----------------|
| X       | CuRS-002     | partial  | ENHANCE CuRS-002 + SRS-004 |
| Y       | —            | none     | NEW CuRS-005 |
| Z       | CuRS-001     | full     | SKIP |
```

If any planned action is SKIP, explain briefly why the existing item already covers it. If UPDATE or ENHANCE, quote the relevant part of the existing item so the user can see the diff before you make it.

Proceed with changes only after presenting this table. If the user overrides an action (e.g., wants NEW instead of ENHANCE), follow their call.

**Refactoring signal**: If the coverage analysis shows two or more ENHANCE or UPDATE actions targeting the same functional area — meaning this area has been extended before and is being extended again — flag the Rule of Three before writing items:

> Rule of Three: this area has already been extended. Consider running **sophist-refact** to consolidate before adding more. Duplicated CuRS intent often signals a shallow design downstream.

This is a signal, not a blocker. If the human confirms they want to proceed, continue with Step 1c.

### 1c. Read tag registry

```bash
cat .sophist/src/tags.md
```

---

## Step 1d: Understand intent — record, don't block

Before making any changes, step back from the mechanics and understand what the human is actually trying to accomplish. A CuRS item that doesn't match the true intent wastes everything downstream — every wrong assumption propagates through SRS, SAD, SDD, and into code.

Analyze the input for three things and record your conclusions — you will embed them as a review point in the CuRS item during Step 2. **Do not wait for chat confirmation; proceed immediately.**

**Purpose** — What business or product goal does this serve? Ask "why does this matter to the end user or the business?" not just "what should the software do?"

**Intent** — What specific change does the human want? Is this a new feature, a constraint on existing behavior, a workflow change, or a quality improvement?

**Hypothesis** — Is this requirement based on a known, validated user need, or is the human testing an assumption? If the input reads like an experiment ("users might want X", "we think this would help", "let's try Y"), flag it.

### Infer validation strategy

Infer how success will be measured based on the requirement type:

| Requirement type | Suggested validation approach |
|-----------------|------------------------------|
| UI / UX behavior | Task-completion test with representative users; specify scenario and success threshold |
| Performance | Before/after benchmark with a specific numeric threshold |
| Data correctness | Golden-dataset comparison or property-based test |
| Integration / API | Contract test against a real dependency; specify request/response fixture |
| Security / access control | Negative test — verify the prohibited action is actually blocked |
| Configuration / operational | Runbook walkthrough; verify runtime output without rebuilding |

You will embed your analysis as a `### Validation Guide` section in the CuRS item (see Step 2 template). The human answers it inline in the file on their next review pass, then re-runs sophist-curs to apply the answer. This validation strategy directly informs the AT items written in Step 4.

---

## Step 2: Execute planned actions

Work through each concept according to the action decided in Step 1b.

### NEW — Write CuRS item(s)

Create `.sophist/src/curs/CuRS-{NNN}.md`. Record the customer's input accurately — do not over-interpret yet.

```markdown
# CuRS-{NNN}: <short title>

## State
`draft`

## Tags
`#tag1` `#tag2`

## Why
<one sentence — what business motivation or customer concern this addresses>

## Traces
- → [SRS-{NNN}](../srs/SRS-{NNN}.md): <which aspect of this customer input is being formalized>

## Input
> "<customer's words verbatim or near-verbatim>"

## Context
<when this was stated and any relevant background>

### Validation Guide
- **Purpose**: <one sentence>
- **Intent**: <one sentence>
- **Hypothesis**: stated / not yet validated
- **Validation strategy**: <how success will be measured>
- **Who validates**: end user / QA / automated test / stakeholder
- **Success criterion**: <observable, measurable outcome>

Confirm or correct this inline, then re-run sophist-curs.

### Review needed
confirm this captures the customer's intent accurately; note any assumptions made
```

Add to `SUMMARY.md` under Customer Requirements and add a row to `.sophist/src/curs/index.md`.

### UPDATE — Revise an existing CuRS item

When the customer is explicitly changing a prior requirement, edit the existing `CuRS-{NNN}.md`:

1. Change `State` to `draft` if it was `reviewed`
2. Append the new customer input to the `## Input` section (keep the original — the history matters):
   ```markdown
   > "<original input>"

   **Updated {date}:** "<new customer words>"
   ```
3. Revise `## Why` and `## Context` if the motivation or scope changed
4. Add a new review point noting what changed and what downstream items (SRS, AT) may need revisiting
5. Follow the same UPDATE path for any SRS items that trace to this CuRS

### ENHANCE — Extend an existing CuRS item

When the customer input adds scope to something already captured (not a contradiction, just more detail):

1. Keep `State` unchanged unless you're adding something structurally new
2. Add a `## Additions` section (or append to `## Context`) with the new detail
3. If the new scope warrants a new SRS item, create it and add a trace from the existing CuRS
4. If the new scope fits within an existing SRS item, update that SRS item instead

### SKIP — No changes needed

When an existing item already covers the intent, don't create anything. Just note the relevant IDs in the report so the user knows the input was heard and is already tracked.

---

## Step 3: Derive SRS items

For each CuRS item, create one or more `.sophist/src/srs/SRS-{NNN}.md` files. Each SRS item must be testable — if you can't imagine an AT for it, split or reframe it.

```markdown
# SRS-{NNN}: <requirement title>

## State
`draft`

## Tags
`#tag1` `#tag2`

## Why
<one sentence — why this requirement exists and what customer need it formalizes>

## Traces
- ← [CuRS-{NNN}](../curs/CuRS-{NNN}.md): <why this is a direct derivation of that customer input, including any added assumptions>
- → [AT-{NNN}](../at/AT-{NNN}.md): <what aspect of this requirement the acceptance test validates>

## Description

<Requirement text. Use "shall" for mandatory, "should" for preferred.>

### Review needed
<specific question: scope, ambiguity, or assumption to verify>
```

Add to `SUMMARY.md` under Software Requirements and add a row to `.sophist/src/srs/index.md`.

Note: The `→ SAD` trace is intentionally absent here. sophist-srs creates the SAD items and adds that trace after you review the SRS.

---

## Step 3b: Debugger cross-cutting concern

After deriving SRS items, check whether the project has a debugger CuRS:

```bash
grep -rl "#debugger" .sophist/src/curs/ 2>/dev/null
```

If no debugger CuRS exists and this is either the first set of requirements for the project or the new CuRS items involve multi-step behavior across components, note in the report that a debugger CuRS is missing. The debugger CuRS captures the customer's need for runtime observability — e.g. "operators shall be able to set log verbosity and output destination without rebuilding the software." Without it, the Debugger component in sophist-impl has no spec to follow and is implemented ad hoc.

Do not create the debugger CuRS automatically — let the human decide whether to add it now. If they say yes, treat it as a NEW action: write a CuRS item tagged `#debugger`, derive an SRS item that specifies:
- Debug levels: `OFF`, `INFO` = component boundary crossings, `DEBUG` = internal algorithm steps, `VERBOSE` = fine-grained traces
- Output control: `--debug-output-dir <path>` for structured data files + log file; omit for stdout-only logging
- **Data files are written automatically when `--debug-output-dir` is set, regardless of `--debug-level`**
- Subprocess logs are captured to separate files when `--debug-output-dir` is set; the main log records each subprocess log file path and timing
- File write events are logged to the main log with path, purpose, and write event metadata; filename collisions are resolved by appending a sequence index
- A data model (schema table) for each component's debug output files must be defined in the SAD `## Debug strategy` section

Write an AT item that verifies: (a) `--debug-level` and `--debug-output-dir` CLI options work at runtime, (b) data files appear in the output dir when only `--debug-output-dir` is specified without `--debug-level`, (c) file metadata is present in the main log alongside each data write.

---

## Step 4: Write AT items

For each SRS item, create `.sophist/src/at/AT-{NNN}.md`.

```markdown
# AT-{NNN}: <test title>

## State
`draft`

## Tags
`#tag1`

## Why
<one sentence — what requirement behavior this test verifies and why this scenario was chosen>

## Traces
- ← [SRS-{NNN}](../srs/SRS-{NNN}.md): <which "shall" statement this test verifies and why this scenario is sufficient>

## Preconditions
<system state before test>

## Steps
1. <action>
2. <action>

## Expected result
<observable outcome — specific and measurable>

## Failure criterion
<what makes this test fail>

### Review needed
<question about test scope or pass criterion>
```

Add to `SUMMARY.md` under Acceptance Tests and add a row to `.sophist/src/at/index.md`.

---

## Step 5: Update tags.md

For every new tag used, add a row to the tag registry and update item counts for affected tags.

```bash
grep -rh "#[a-z]" .sophist/src/curs/ .sophist/src/srs/ .sophist/src/at/ \
  | grep -o "#[a-z-]*" | sort | uniq -c | sort -rn
```

---

## Step 6: Update traceability summaries

Update the traceability tables in `.sophist/src/curs/index.md`, `.sophist/src/srs/index.md`, and `.sophist/src/at/index.md`.

---

## Step 7: Build check

```bash
cd .sophist && mdbook build 2>&1 | tail -20
```

Fix all broken links before reporting.

---

## Step 8: Report review points

```
## Changes Summary

| ID | Title | Action | Reason |
|----|-------|--------|--------|
| CuRS-003 | ... | new     | no existing coverage |
| SRS-007  | ... | new     | derived from CuRS-003 |
| CuRS-001 | ... | enhance | user input adds scope to login flow |
| SRS-002  | ... | update  | revised timeout requirement |
| CuRS-002 | ... | skip    | already fully covered (user input rephrased same need) |

## Review Points

### Must Resolve
- [ ] SRS-007: <question — blocks downstream architecture work>

### Should Verify
- [ ] CuRS-003: <assumption made in transcription>

### For Awareness
- [ ] AT-005: <coverage note>

---

Next: Open the CuRS files and write your answers under the `### Review needed` and `### Validation Guide` sections inline,
then run **sophist-curs** again to apply your answers and mark CuRS items reviewed.
Also open the SRS and AT files and write your answers there, then run **sophist-srs** to
mark SRS items reviewed and generate the corresponding SAD items.
```

---

## Debug output

If the skill was invoked with `--debug-level=VERBOSE`, write a debug session. Create the output directory from `--debug-output-dir` (default: `.sophist/debug/`):

```bash
mkdir -p <value of --debug-output-dir, or .sophist/debug>
```

Create a timestamped directory inside it (e.g. `20240115-143022-curs/`) and write:

| File | Contents |
|------|----------|
| `00-input.md` | The human's original request, verbatim |
| `01-coverage.md` | Coverage analysis table — each concept, closest match, coverage rating, planned action, and brief rationale |
| `02-intent.md` | Purpose / intent / hypothesis analysis and the full Validation Guide from Step 1d |
| `03-actions.md` | Each planned action executed (NEW/UPDATE/ENHANCE/SKIP) with item IDs and one-line reasoning |
| `04-review-points.md` | All review points generated, grouped by Must/Should/Awareness |

---

## Commit message

After all file writes are complete, propose a commit message for the changes. Run `git diff HEAD` to review what changed, then write a message in this format:

```
docs(curs): <short description under 72 chars>

Why: <what triggered this change — the new or changed customer requirement>
What: <which CuRS/SRS items were created or updated>
```

Keep `Why` and `What` to one or two sentences each — enough for someone reading `git log` to understand the change without opening the diff.

---

## Constraints

- Write no source code and no SAD/SDD items — those belong to the cascade after review.
- SAD items will be created by sophist-srs once SRS items are reviewed.
- Every SRS item must be testable. If it isn't, either split it or flag it as a question.
- Use mermaid diagrams in SRS items when a multi-step user flow is involved. Use `<br/>` for line breaks — not `\n`. Quote labels containing `[`, `]`, `(`, `)`, or `:` using `["..."]` syntax.
