---
name: p4d
description: Create step-by-step implementation plans from context. Use this when the user provides a context location (file, directory, or URL) and needs a detailed breakdown of how to implement something. The skill reads the context, analyzes the codebase if relevant, and produces a structured plan that can be executed sequentially.
---

# Plan from Context (p4d)

Use this skill to generate implementation plans by reading and analyzing context provided by the user.

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

### 3. Create the plan
Structure your plan with:
- **Objective**: What will be implemented
- **Prerequisites**: What needs to be in place first
- **Steps**: Numbered, sequential steps with:
  - Clear action
  - What file(s) to modify or create
  - Why this step matters
  - Expected outcome
- **Testing approach**: How to verify each step works
- **Edge cases**: Known challenges or gotchas

### 4. Present clearly
Use a structured format (ASCII diagram or numbered list) that's easy to follow. Each step should be actionable by someone following the plan directly.

## Example output structure

```text
Objective: Add user authentication to the API

Prerequisites:
- Node.js 16+
- PostgreSQL running locally
- Environment variables configured

Step 1: Create auth schema
  File: db/migrations/001_auth_schema.sql
  Action: Create users, sessions tables
  Why: Foundation for auth system
  Verify: psql shows new tables

Step 2: Add auth middleware
  File: src/middleware/auth.ts
  Action: Implement JWT validation
  Why: Protect routes
  Verify: Middleware rejects invalid tokens

[... more steps ...]
```

## Notes

- Plans should be detailed enough to execute without ambiguity
- Call out file paths, function names, and concrete artifacts
- Include verification steps for each major phase
- If the context is large, summarize and focus on the relevant parts
- Ask clarifying questions if requirements are unclear
