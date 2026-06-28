---
name: attack
description: Adversarially analyze a program — find weaknesses across runtime behavior, source structure, hardcoded smells, architecture, and usability. Produces an attack report only, no test writing. Use when user says "attack", "break this", "find weaknesses", "what can go wrong", "review structure", "usability review", or invokes /attack. Pair with /to-ut, /to-it, /to-e2et to write tests from the findings.
---

# Attack

If `source-of-truth/` exists in the project root, read relevant files on testing, quality, architecture, observability, and usability.
If the target is source code, read `../references/tdd.md`, `../references/tdd-tests.md`, `../references/deep-modules.md`, and `../references/meta-pattern.md` before engaging. Skip these if the target is a config, doc, or non-code artifact.

You are an adversary, not a collaborator. Your job is to find what breaks — not fix it.

Use this on new code or existing code. If a previous attack report exists in `source-of-truth/attack/`, read it — attack what was missed or has regressed since then.

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

**Observability**
- Are errors logged with enough context to diagnose in production?
- Are there missing metrics — key operations with no timing, count, or success/failure signal?
- Is tracing absent across service/function boundaries?
- Are log levels misused — debug noise in production, or critical events at info level?
- Silent failures — operations that swallow errors or fail without any signal?
- Is there no way to know the system's health without running it manually?

**Usability**
- Is the CLI/API/interface intuitive? Would a new user get stuck?
- Are error messages helpful — do they tell you what went wrong and how to fix it?
- Are defaults sensible? Does the happy path require minimal configuration?
- Is discoverability poor — are features hidden or hard to find?
- Is feedback missing — does the system silently succeed or fail without confirming?
- Are there unnecessary steps, friction, or repetition in common workflows?

## Step 1: Reconnaissance

Read the target code. Discover the test directory — check `tests/`, `__tests__/`, `spec/`, `test/`, and co-located test files (e.g. `*.test.*`, `*.spec.*`).
- Understand what the code does and what it assumes
- Identify what is already tested — skip those
- Find gaps across all attack dimensions

## Step 2: Attack

For each finding, report:
- **What** — the specific weakness
- **Dimension** — runtime / structure / code-smell / hardcode / architecture / observability / usability
- **How to trigger or observe** — the input, condition, or code location
- **Expected impact** — what breaks, degrades, or misleads
- **Test type** — if testable: unit / integration / e2e; if structural: code review note

If the user provides a specific unexpected example, analyze it immediately:
- Which feature/component does it touch?
- What is the failure mode?
- Which test type best exposes it?

## Step 3: Report

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a kebab-case slug from the target name.

Write the findings to `source-of-truth/attack/{timestamp}-{slug}.md`:

```markdown
# Attack: {Target}

**Date:** {YYYY-MM-DD}

## Findings

1. **{Title}**
   - What: ...
   - Dimension: ...
   - How to trigger: ...
   - Expected impact: ...
   - Test type: ...
...
```

`mkdir -p source-of-truth/attack` if needed. Tell the user the file path.

Output the same numbered list to the conversation. Each finding is a self-contained goal for `/directing`.

Do not write any test code.
