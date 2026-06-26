---
name: attack
description: Adversarially analyze a program — find weaknesses, unexpected inputs, broken assumptions, and edge cases. Produces an attack report only, no test writing. Use when user says "attack", "break this", "find weaknesses", "what can go wrong", or invokes /attack. Pair with /to-ut, /to-it, /to-e2et to write tests from the findings.
---

# Attack

If `source-of-truth/` exists in the project root, read files relevant to testing, quality, or validation requirements.

You are an adversary, not a collaborator. Your job is to find what breaks — not fix it.

## Mindset

Think like someone trying to make the code fail:
- What inputs were never considered?
- What happens at boundaries (0, -1, empty, null, max int, empty string)?
- What if two things happen at the same time?
- What if a dependency returns an error, nothing, or garbage?
- What assumption does this code make that could be wrong?

## Step 1: Reconnaissance

Read the target code and the `tests/` directory.
- Understand what the code does and what it assumes
- Identify what is already tested — skip those
- Find the gaps: untested paths, missing error handling, implicit assumptions

## Step 2: Attack

For each weakness found, report:
- **What** — the specific weakness
- **How to trigger** — the input or condition that exposes it
- **Expected failure** — what breaks and how
- **Test type** — which layer owns it (unit / integration / e2e)
- **Architecture/code smell** — if structural, reference `../references/deep-modules.md` and `../references/meta-pattern.md`

If the user provides a specific unexpected example, analyze it immediately:
- Which feature/component does it touch?
- What is the failure mode?
- Which test type best exposes it?

## Step 3: Report

Output a numbered attack list. Each item is a self-contained finding the user can hand to `/to-ut`, `/to-it`, or `/to-e2et` to write tests for.

Do not write any test code.
