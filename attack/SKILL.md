---
name: attack
description: Adversarially analyze a program — find weaknesses across runtime behavior, source structure, hardcoded smells, and architecture. Produces an attack report only, no test writing. Use when user says "attack", "break this", "find weaknesses", "what can go wrong", "review structure", or invokes /attack. Pair with /to-ut, /to-it, /to-e2et to write tests from the findings.
---

# Attack

Run `sot search-cmd "testing quality validation" --k 5` for relevant context.
Read `../references/tdd.md` and `../references/tdd-tests.md` and `../references/deep-modules.md` and `../references/meta-pattern.md` before engaging.

You are an adversary, not a collaborator. Your job is to find what breaks — not fix it.

## Mindset

You are an adversary across every dimension — runtime, structure, and design. Attack on all fronts:

**Runtime behavior**
- What inputs were never considered?
- What happens at boundaries (0, -1, empty, null, max int, empty string)?
- What if two things happen at the same time?
- What if a dependency returns an error, nothing, or garbage?
- What assumption does this code make that could be wrong?

**Source structure**
- Are modules too shallow — exposing complexity that should be hidden? (`deep-modules.md`)
- Is the file/folder structure coherent with the actual domain boundaries?
- Are concerns mixed in the same file or function?

**Code smells**
- Long functions, large classes, deep nesting
- Duplicated logic across multiple places
- Dead code, unused parameters, obsolete comments
- Inconsistent naming, misleading abstractions
- Feature envy, inappropriate intimacy between modules

**Hardcoded smells**
- Magic numbers, hardcoded strings, inline config values
- Hardcoded paths, URLs, credentials, timeouts
- Logic that should be data-driven but isn't

**Architecture**
- Does the decomposition match the scale and subdomain? (`meta-pattern.md`)
- Are the wrong things coupled together (cohesers vs. decouplers)?
- Is abstraction at the wrong level — too high or too low?

## Step 1: Reconnaissance

Read the target code and the `tests/` directory.
- Understand what the code does and what it assumes
- Identify what is already tested — skip those
- Find gaps across all four attack dimensions

## Step 2: Attack

For each finding, report:
- **What** — the specific weakness
- **Dimension** — runtime / structure / code-smell / hardcode / architecture
- **How to trigger or observe** — the input, condition, or code location
- **Expected impact** — what breaks, degrades, or misleads
- **Test type** — if testable: unit / integration / e2e; if structural: code review note

If the user provides a specific unexpected example, analyze it immediately:
- Which feature/component does it touch?
- What is the failure mode?
- Which test type best exposes it?

## Step 3: Report

Output a numbered attack list. Each item is a self-contained finding the user can hand to `/to-ut`, `/to-it`, or `/to-e2et` to write tests for.

Do not write any test code.
