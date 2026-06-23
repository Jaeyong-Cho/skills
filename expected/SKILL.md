---
name: expected
description: Clarify a feature or function's expected behavior through grilling, then write unambiguous expected input/output pairs. Reads the codebase for context if in a project. Use when user wants to define expected results, specify behavior, nail down inputs and outputs, or says "expected", "write expected result", "define expected behavior", "what should this return".
---

# Expected

Produce unambiguous expected input/output pairs for a feature or function. No implementation — just what goes in and what must come out.

## Workflow

1. **Read codebase** — if in a project, read relevant source files to understand existing types, constraints, and conventions; skip if not a project
2. **Grill** — interview the user to eliminate ambiguity; one question at a time, highest-impact first; use `AskUserQuestion` for discrete options (recommended first); keep going until every edge case and boundary is resolved; user can say "wrap up" to move on
3. **Write** — produce the expected result document (see format below)

## Grill focus areas

- What are the valid inputs? What are invalid ones?
- What happens at boundaries (empty, null, zero, max)?
- Are there side effects, or is this pure input → output?
- What does failure look like — error, empty, exception?
- Are there multiple callers with different expectations?

## Output format

Write to `expected/<slug>.md` in the current directory.

```md
# Expected: {feature or function name}

## Context
{1-2 sentences: what this is for, from the codebase or user}

## Cases

### {case name}
- **Input**: {concrete value or structure}
- **Output**: {concrete value, output format (JSON/CSV/...), log lines, behavior, side effect, or error}

### {case name}
- **Input**: {concrete value or structure}
- **Output**: {concrete value, output format (JSON/CSV/...), log lines, behavior, side effect, or error}

## Rules
- {invariant that holds across all cases}
- {constraint derived from grilling}
```

## Rules

- Every input and output must be concrete — no "etc.", no "something like"
- If a case is still ambiguous after grilling, mark it `// open` and move on
- Do not specify implementation — only what goes in and what must come out
