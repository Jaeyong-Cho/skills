---
name: pf-review
description: |
  Review a VAO ADR implementation — walk through each user story scenario step by step, grill the user with targeted questions referencing actual source files and line numbers, and confirm the implementation matches the design intent.
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

For each hop — stop, ask, wait for answer, then proceed:

1. **Announce** — `"Now at: file:line — <what this hop does>"`
2. **Show** — display the relevant code snippet inline with `file:line` header
3. **Ask** — one specific question about this code via `AskUserQuestion` (discrete) or plain text: what does this do, which branch is taken, what is the input/output, why is this here?
4. **Confirm** — after user answers: confirm if correct and explain why, or correct and explain the actual behavior. Then move to next hop.

Do not advance until user has answered. User can say **"wrap up"** to skip remaining hops. Walk every hop. Never skip.

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

## Step 6: Done

Ask via `AskUserQuestion`: "Issues fixed. What next?" — options: "Re-review the fixes" / "Done".

Mark ADR status as `Accepted`. Show files created/updated. Suggest commit message using `../pf/references/commit.md`.
