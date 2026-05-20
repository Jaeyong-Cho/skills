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

## Step 3: Trace the execution flow — entry point to end

Follow the actual runtime path of the code, not the ADR's writing order. Start at the entry point (the first thing that runs when a user triggers the feature) and trace every hop until the response or side effect is complete.

**Never skip a point in the trace — even if the code is exactly correct.** The purpose is both to catch issues and to build the human's understanding of their own code.

### 3a. Map the trace first

Before asking anything, read all implementation files and map the full execution path:

```
Entry point (file:line)
  → Aspect 1 (file:line)
  → Aspect 2 (file:line)
  → Object method (file:line)
  → ...
  → Response / side effect (file:line)
```

Print this map so the human can see the full journey before you begin.

### 3b. Walk each hop

For each hop in the trace, in execution order:

1. **Announce the hop** — `"Now at: file:line — <what this hop does>"`
2. **Read the exact lines** — quote the relevant code snippet
3. **Ask questions** — one at a time, no maximum. Use `AskUserQuestion` for discrete options, plain text for open-ended. Cite `file:line` in every question.

**Question types to draw from at each hop** (use what fits):
- *Explain it* — ask the human to describe what this code does in their own words, before you confirm or correct
- *Why here?* — why does this logic live at this hop, in this layer?
- *What comes in / what goes out?* — inputs, outputs, side effects at this exact point
- *What happens when...?* — edge cases, invalid input, null, empty, concurrent access
- *Layer check* — is this Value, Aspect, or Object code? Does it belong here?
- *Anything you'd change?* — open reflection after seeing it in context

Correct code still gets questions. If a hop is flawless, use it to cement understanding — ask the human to explain it rather than just confirm it.

The user can say **"wrap up"** to compress remaining questions for the current hop and move to the next. Walk every hop. Do not skip any.

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
