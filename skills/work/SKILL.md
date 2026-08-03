---
name: work
description: Execute implementation plans step-by-step. Use this when you have a structured plan (from p4d or similar) and need to follow it systematically. The skill reads the plan, executes each step in order, verifies outcomes, and tracks progress through the implementation.
---

# Execute Plan (work)

Use this skill to systematically execute a structured implementation plan.

## When to use

- You have a step-by-step plan (from p4d or provided by user)
- You need to implement each step in sequence
- You want verification after each step
- You're tracking progress through a multi-step task

## Your approach

### 1. Receive and parse the plan
- Accept the plan (text, file, or output from p4d)
- Extract objectives, prerequisites, and steps
- Verify prerequisites are met before starting
- Ask clarifying questions if steps are ambiguous

### 2. Execute step-by-step
For each step:
- **Understand**: Read the step objective and context
- **Act**: Perform the required action (write code, create files, run commands, etc.)
- **Verify**: Check the expected outcome
- **Report**: Show what was done and result
- **Move forward**: Only proceed to next step if verification passes

### 3. Handle issues
- If a step fails: diagnose the issue, don't skip it
- If verification doesn't match expectations: debug or ask for clarification
- If the plan needs adjustment: discuss with user before proceeding
- Document blockers and decisions made

### 4. Track progress
- Show which step you're on
- Summarize completed steps
- Call out remaining steps
- End with a completion summary

## Example workflow

Per `../../references/document-style.md`'s `key_value_format`: the plan header, each step's own facts, and the closing summary are all attributes of a single subject (the plan, the step, the run) — key-value, not narrated bullets. The step sequence itself stays a numbered progression.

```text
plan: "Add user authentication to API"
prerequisites:
  - Node.js 16+ installed
  - PostgreSQL running
  - Environment variables set

Step 1/5: Create auth schema
  file: db/migrations/001_auth_schema.sql
  result: users table created, sessions table created
  status: ready for step 2

Step 2/5: Add auth middleware
  file: src/middleware/auth.ts
  action: implement JWT validation logic
  test: middleware correctly rejects invalid tokens
  status: complete

[... continuing through steps ...]

summary:
  completed: 5/5 steps
  tests: passing
  status: ready for review
```

## Notes

- Execute plans as written unless you identify a blocker
- Each step builds on previous ones — order matters
- If a step is unclear, ask the user before proceeding
- Document file paths and changes for reference
- Use tools (Read, Edit, Write, Bash) to implement actual changes
- Provide clear before/after view of modifications

## Integration with p4d

This skill works seamlessly with `/p4d` plans:
1. Run p4d to get a structured plan
2. Run work to execute it step-by-step
3. work tracks progress and handles verification at each stage
