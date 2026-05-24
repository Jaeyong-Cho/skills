---
name: pf-review
description: |
  Review a VAO ADR implementation — walk through each user story scenario step by step, grill the user with targeted questions referencing actual source files and line numbers, and confirm the implementation matches the design intent. Then update the documentation.
  Use after pf-impl is done. Triggers: "pf-review", "review the implementation", "review the code", "code review", "let's review", after implementation is complete.
---

Read `../pf/references/caveman.md` and apply caveman style throughout — including all output documents.
Check journal: `[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null` — use to orient review to today's focus.

# VAO Code Review

Review implementation against ADR — user story by user story. Use `AskUserQuestion` throughout. Cite `file:line` in every question.

## Step 1: Load the ADR

User names an ADR → find it: `ls .pf/src/adr/ | grep <id>`. Otherwise list and ask which to review.

Read ADR. Focus on: User Stories, Decision section (Value/Aspect/Object layers), Step-by-Step Plan.

## Step 2: Find implementation files

From ADR Step-by-Step Plan, collect all listed files + their layer (`[value]`, `[aspect]`, `[object]`). Read each in full.

Find test files: `grep -rl "<ComponentName>" tests/ 2>/dev/null`

Build mental map: which file owns which behavior, at which line numbers.

## Step 3: Trace execution — entry to end

**Map first** — before asking anything, read all files and map the full execution path (see [REFERENCE.md](REFERENCE.md#execution-trace-map)). Print map so user sees the full journey.

For each hop in order:
1. **Announce** — `"Now at: file:line — <what this hop does>"`
2. **Quote** exact relevant lines
3. **Grill** — one question at a time via `AskUserQuestion` (discrete) or plain text (open). Types: explain it, why here, inputs/outputs, edge cases, layer check, what would you change? Cite `file:line` in every question.

Correct code still gets questions — use to cement understanding. User can say **"wrap up"** to skip to next hop. Walk every hop. Never skip.

## Step 4: Simulate scenarios

Derive scenarios from ADR User Stories + edge cases found during trace. See [REFERENCE.md](REFERENCE.md#scenario-list-format) for list format.

Ask via `AskUserQuestion`: "Add any missing scenarios?" — user can add or say "looks good".

For each scenario: trace code path (`file:line` per hop), state expected vs actual, mark: Pass / Fail / Partial / Untestable. Collect failures/partials as issues.

Generate HTML report — see [REFERENCE.md](REFERENCE.md#scenario-html-report) for spec.
Save: `.pf/review/YYYY-MM-DD-<adr-slug>.html`

```
Scenario report: .pf/review/YYYY-MM-DD-<adr-slug>.html
```

## Step 5: Fix issues

Collect every issue from Step 3 — wrong behavior, wrong layer, missing error handling, scattered concerns, missing tests.

For each: fix code at cited `file:line`, update ADR to reflect changes (Decision, User Stories if behavior shifted, Step-by-Step Plan if files/layers changed). Batch fixes, show summary after.

## Step 6: Confirm and decide

Ask via `AskUserQuestion`: "Issues fixed. What next?" — options: "Update documentation" (Recommended) / "Re-review the fixes" / "Done — skip docs".

## Step 7: Update documentation (if confirmed)

Read `../pf/references/docs.md` for full structure and SUMMARY.md format.

Check existing: `ls .pf/src/docs/value/ .pf/src/docs/aspect/ .pf/src/docs/object/ 2>/dev/null`

From ADR Decision section, create one file per entity per layer. See [REFERENCE.md](REFERENCE.md#doc-file-formats) for file format. Write in present tense. Add **Related files** section per entity: `grep -rl "<EntityName>" src/`

Update indexes and SUMMARY.md, then build: `cd .pf && mdbook build 2>&1` — fix all errors before reporting.

## Step 8: Done

Mark ADR status as `Accepted`. Show files created/updated. Suggest commit message using `../pf/references/commit.md`.

If review surfaced surprising findings or insights worth keeping → suggest running `/pf-research` to record them.
