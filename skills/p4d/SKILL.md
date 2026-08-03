---
name: p4d
description: Create step-by-step implementation plans from context. Use this when the user provides a context location (file, directory, or URL) and needs a detailed breakdown of how to implement something. The skill reads the context, analyzes the codebase if relevant, and produces a structured plan that can be executed sequentially.
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

### 3. Create the plan
Structure your plan with:
- A key-value header (per `../references/document-style.md`'s `key_value_format` — these are attributes of the plan itself, not a sequence): `objective:`, `prerequisites:` (list value), `testing_approach:`, `edge_cases:` (list value)
- **Corrections to context doc** (if step 2b found any): what the doc claimed vs. what the spot-check found, and which plan steps exist because of it
- **Steps**: Numbered, sequential steps with:
  - Clear action
  - What file(s) to modify or create
  - Expected outcome


### 4. Present clearly
Use a structured format (ASCII diagram or numbered list) that's easy to follow. Each step should be actionable by someone following the plan directly.

### 5. Parallel Execution Orchestration
- Group parallel execution paths.
- Determine sub-agent dispatch order.

## Example output structure

```text
objective: Add user authentication to the API
prerequisites:
  - Node.js 16+
  - PostgreSQL running locally
  - Environment variables configured

Step 1: Create auth schema
  File: db/migrations/001_auth_schema.sql
  Action: Create users, sessions tables
  Verify: psql shows new tables

Step 2: Add auth middleware
  File: src/middleware/auth.ts
  Action: Implement JWT validation
  Verify: Middleware rejects invalid tokens

[... more steps ...]

Group 1
- 1, 2, 3
Group 2 
- 4, 5
Group 3 (Depends by group 1, group 2)
- 6, 7, 8
```

## Notes

- Plans should be detailed enough to execute without ambiguity
- **MUST NOT** write code directly and plan document. Just write a instruct as a plan.
- Call out file paths, function names, and concrete artifacts
- Include verification steps for each major phase
- If the context is large, summarize and focus on the relevant parts
- Ask clarifying questions if requirements are unclear
- Don't let step 2b's spot-checks turn into a full codebase read by default — only widen beyond the targeted claims if a spot-check actually turns up a contradiction serious enough to doubt the rest of the doc
