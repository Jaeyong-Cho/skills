---
name: p4d
description: Create step-by-step implementation plans from context. Use this when the user provides a context location (file, directory, or URL) and needs a detailed breakdown of how to implement something. The skill reads the context, analyzes the codebase if relevant, and writes the plan as one file per parallel-execution group (plan/index.md plus plan/group-{n}.md) so a subagent dispatched to one group only needs to read that group's file.
---

# Plan from Context (p4d)

Use this skill to generate implementation plans by reading and analyzing context provided by the user
**MUST READ** `/ponytail` skill before planning

## When to use

- User gives you a context location (file path, directory, URL, or description)
- They want a step-by-step implementation plan
- You need to understand existing code/structure before planning

## Your approach

### 1. Gather context
Ask the user for the context location if not provided:
- Local file path
- Project directory
- URL or external resource
- Or a description of what they're building

### 2. Read and analyze
- Read the context file(s) or codebase
- Understand the existing structure, patterns, and dependencies
- Identify constraints and requirements
- Note relevant technologies or frameworks

### 2b. Verify load-bearing claims before trusting them

A claim is load-bearing if believing it wrong would change whether a plan step exists at all — most commonly "X was already removed/done/fixed," "nothing else references X," or "the only state/callers are Y." These are the highest-risk category: a plan built on a false one *omits* a step rather than getting a step wrong, and an omission doesn't show up on a read-through of the plan.

- If the context doc tags claims `[DIRECT]`/`[INFERRED]` (the `explore` skill does this), spot-check every `[INFERRED]` load-bearing claim. Treat an untagged doc's absence/removal/"only X" claims as `[INFERRED]` by default.
- Spot-check cheaply — this is not "read the codebase," it's checking the specific facts the plan's correctness depends on: one targeted `Read`/`Grep`/`Bash` call against the literal named artifact if you have codebase access, or one `haiku`-tier `explore` dispatch if you don't. A handful of targeted checks costs orders of magnitude less than re-deriving the whole doc from a full read, for the same correctness.
- If a spot-check contradicts the doc, say so explicitly in the plan (a short "Correction to context doc" callout referencing what was claimed vs. what the check found) — don't just silently fix the plan and leave the doc wrong for the next person who reads it.

### 3. Group steps before writing anything

Determine parallel execution groups now, before the plan is written down — not as an afterthought over a finished flat list. Group steps that can run concurrently (no shared file, no data dependency between them); a group that needs another group's output declares that dependency rather than being merged into it.

### 4. Write the plan as one file per group

A subagent later dispatched to execute one group must be able to work from that group's file alone — never require it to read a sibling group's file to know what to do. Write:

- `plan/index.md` — the plan's own attributes, key-value (per `../references/document-style.md`'s `key_value_format`): `objective:`, `prerequisites:` (list), `testing_approach:`, `edge_cases:` (list), plus a **Corrections to context doc** section if step 2b found any (what the doc claimed vs. what the spot-check found, and which steps exist because of it). Then a group table: `Group N | steps | depends_on | file`.
- `plan/group-{n}.md` per group — that group's steps only, each with a clear action, file(s) to modify/create, and expected outcome. If a step depends on a prior group's output, state the concrete artifact to expect (a file path, an exported symbol, a schema) — a fact the dispatched agent can check for itself — not "see group N," which would send it back to a file it isn't given.

### 4b. Every step's `Verify:` is a command, not a description

Per `../references/good-harness.md`: classify each step's constraint (structural/behavioral x objective/judgment) and write `Verify:` as the actual command that produces a pass/fail — never a prose claim the executor would have to eyeball ("Middleware rejects invalid tokens"). If a step's outcome genuinely can't be reduced to a command (rare — usually means the step is too coarse), split it until each piece can.

- Objective + structural: a `grep`/`test`/field check (`grep -q "^export function verifyToken" src/middleware/auth.ts`)
- Objective + behavioral: the actual test/repro command and its expected exit code or output (`npm test -- auth.test.ts`, `curl -s localhost:3000/api/x | grep -q '"ok":true'`)
- Judgment-based: still name a concrete command that produces the artifact to judge (e.g. a diff or log) — the plan can't automate the judgment call, but it must automate getting to the evidence
- If no command produces a failing case you can picture, the step isn't harnessed yet — don't write "Verify: looks correct"

### 5. Present clearly

Report `plan/index.md`'s group table so the orchestrating skill (e.g. `/work`) can see dispatch order and dependencies at a glance without opening every group file.

## Example output structure

`plan/index.md`:
```text
objective: Add user authentication to the API
prerequisites:
  - Node.js 16+
  - PostgreSQL running locally
  - Environment variables configured
testing_approach: ...
edge_cases:
  - ...

Group | Steps | Depends on | File
1     | 1-3   | none       | group-1.md
2     | 4-5   | none       | group-2.md
3     | 6-8   | 1, 2       | group-3.md
```

`plan/group-1.md`:
```text
Step 1: Create auth schema
  File: db/migrations/001_auth_schema.sql
  Action: Create users, sessions tables
  Verify: psql -c "\dt" | grep -qE "users|sessions"

Step 2: Add auth middleware
  File: src/middleware/auth.ts
  Action: Implement JWT validation
  Verify: npm test -- auth.test.ts (expects "rejects invalid token" case to pass)

[... step 3 ...]
```

`plan/group-3.md` (depends on groups 1 and 2) states what to expect from them inline, e.g. "Expects `src/middleware/auth.ts` to export `verifyToken()` (group 1) and `src/db/models/session.ts` (group 2)" — not a pointer back to those files.

## Notes

- Plans should be detailed enough to execute without ambiguity
- **MUST NOT** write code directly and plan document. Just write a instruct as a plan.
- Call out file paths, function names, and concrete artifacts
- Every step's verification is a command (see 4b) — no eyeball-only checklists
- If the context is large, summarize and focus on the relevant parts
- Ask clarifying questions if requirements are unclear
- Don't let step 2b's spot-checks turn into a full codebase read by default — only widen beyond the targeted claims if a spot-check actually turns up a contradiction serious enough to doubt the rest of the doc
