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

## Step 3: Walk each user story

For each User Story in the ADR, do the following in order:

1. **State the story** — re-read it: "Story N: As a `<actor>`, I want `<feature>`, so that `<benefit>`."
2. **Trace the code** — find the entry point, aspect logic, and objects involved. Note exact file paths and line numbers.
3. **Ask questions** using `AskUserQuestion` — one at a time, no maximum. Frame each question around the story, cite `file:line`, and offer concrete options. Put your assessment first (Recommended). Keep asking until the story is fully confirmed or all issues are surfaced.

For each story, ask about both basic functionality (does the happy path work?) and edge cases (what happens when inputs are invalid, missing, or boundary conditions are hit?). Draw questions from what you actually see in the code — cite `file:line` in every question.

The user can say "wrap up" at any time to skip remaining questions and move to the next story. Walk every user story. Do not skip any.

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
