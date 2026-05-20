---
name: pf-review
description: |
  Review a VAO ADR implementation — walk through each user story scenario step by step, grill the user with targeted questions referencing actual source files and line numbers, and confirm the implementation matches the design intent. Then update the documentation.
  Use after pf-impl is done. Triggers: "pf-review", "review the implementation", "review the code", "code review", "let's review", after implementation is complete.
---

Read `../pf/references/caveman.md` and apply caveman style throughout — including in all output documents.

Check for today's journal context:

```bash
[ -n "$PFJ_PATH" ] && cat "$PFJ_PATH/today.md" 2>/dev/null
```

If today.md is found, use it to orient the review to today's focus and goals.

# VAO Code Review

Review the implementation against the ADR — user story by user story. Use `AskUserQuestion` throughout. Reference source files and line numbers in every question.

---

## Step 1: Load the ADR

If the user names an ADR (e.g. "adr-001", "0001", "auth-flow"), find it:

```bash
ls .pf/src/adr/ | grep 0001
```

If no ADR is specified, list available ADRs and ask which one to review.

Read the ADR. Focus on: User Stories, the Decision section (Value/Aspect/Object layers), and the Step-by-Step Plan.

---

## Step 2: Find the implementation files

From the ADR's Step-by-Step Plan, collect all listed files and their assigned layer (`[value]`, `[aspect]`, `[object]`). Read each file in full.

Also find test files:

```bash
grep -rl "<ComponentName>" tests/ 2>/dev/null
```

Build a mental map: which file owns which behavior, and at which line numbers.

---

## Step 3: Walk each implementation step

Walk through every step in the ADR's Step-by-Step Plan in order. **Never skip a step — even if the code is exactly correct.** The purpose is both to catch issues and to ensure the human understands every line that was written.

For each step:

1. **Announce the step** — state the step number, its goal, and the files it touches: `"Step N: <goal> — <file>"`
2. **Read the code** — read the relevant file and locate the exact lines for this step
3. **Ask questions** — one at a time, no maximum, using `AskUserQuestion` for discrete options or plain text for open-ended questions. Cite `file:line` in every question.

**Question types to cycle through for every step** (adapt to what the code actually shows):
- *What does this do?* — ask the human to explain the logic in their own words before you confirm or correct
- *Why this approach?* — probe the design choice: why this structure, this name, this boundary?
- *What happens when...?* — edge cases, invalid input, boundary conditions
- *Which layer does this belong to?* — confirm Value / Aspect / Object placement
- *Is there anything you'd change now that you see it?* — open reflection

Correct code still gets questions. Understanding is the goal, not just finding bugs. If a step is flawless, use it to cement the human's mental model — ask them to explain it, not just confirm it.

The user can say **"wrap up"** to compress remaining questions for the current step and move on. Walk every step. Do not skip any.

---

## Step 4: Fix issues from the review

Collect every issue surfaced during Step 3 — incorrect behavior, wrong layer placement, missing error handling, thin objects, scattered concerns, missing tests, etc.

For each issue:
1. Fix the code at the cited `file:line`
2. Update the ADR to reflect what actually changed — correct the Decision section (Value/Aspect/Object), User Stories if the behavior shifted, and the Step-by-Step Plan if files or layers changed

Apply all fixes before moving on. Do not ask the user to confirm each fix individually — batch them and show a summary after.

---

## Step 5: Confirm and decide

Use `AskUserQuestion`:

- Question: "Issues fixed. What next?"
- Options: "Update documentation" (Recommended) / "Re-review the fixes" / "Done — skip docs"

---

## Step 6: Update documentation (if confirmed)

Read `../pf/references/docs.md` for the full structure, file templates, and SUMMARY.md format.

Check what already exists:

```bash
ls .pf/src/docs/value/ .pf/src/docs/aspect/ .pf/src/docs/object/ 2>/dev/null
```

From the ADR's Decision section, identify every individual entity in each layer:
- **Value** — each entry point, command, or use case
- **Aspect** — each concern handler (auth, billing, logging, etc.)
- **Object** — each domain entity/aggregate

Create one file per entity within its layer directory. Write in present tense — describe what **is**, not what was decided.

**`value/<N>-<entry-point>.md`** — the user need this entry point serves: what it does, what success looks like, what must never happen.

**`aspect/<N>-<concern>.md`** — how this concern is handled: the algorithm or workflow, which objects it uses and from what angle. Mermaid diagrams for flows.

**`object/<N>-<entity>.md`** — this entity's full identity: properties, actions, behaviors, relationships, invariants. Mermaid diagrams for relationships.

At the bottom of each file, add a **Related files** section with the source and test files for that entity:

```bash
grep -rl "<EntityName>" src/ --include="*.ts" --include="*.py" --include="*.go"
```

Update indexes and SUMMARY.md, then build:

```bash
cd .pf && mdbook build 2>&1
```

Fix all errors before reporting to the user.

---

## Step 7: Done

Mark the ADR status as `Accepted`. Show the user which files were created or updated. Suggest a commit message using `../pf/references/commit.md`.
