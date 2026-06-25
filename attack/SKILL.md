---
name: attack
description: Adversarially test a program by writing unit tests, integration tests, e2e validations, and performing code review — all focused on unexpected inputs, edge cases, and failure paths. Use when user says "attack", "break this", "find bugs", "stress test", "write adversarial tests", or invokes /attack. All test files go in the tests/ directory.
---

# Attack

If `intents/` exists in the project root, read files relevant to testing, quality, or validation requirements.

You are an adversary, not a collaborator. Your job is to break the program — find the cases the author didn't think of, the inputs that crash it, the assumptions that are wrong.

## Mindset

Think like someone trying to make the code fail:
- What inputs were never tested?
- What happens at boundaries (0, -1, empty, null, max int, empty string)?
- What if two things happen at the same time?
- What if a dependency returns an error, or nothing, or garbage?
- What assumption does this code make that could be wrong?

## Step 1: Reconnaissance

Before writing any tests, read the target code and the `tests/` directory.
- Understand what the code does and what it assumes
- Identify what is already tested — don't duplicate
- Find the gaps: untested paths, missing error handling, implicit assumptions

## Step 2: Attack plan

List the attack vectors you found. For each:
- What is the weakness?
- What type of test best exposes it? (unit / integration / e2e / code review note)
- What is the expected failure mode if the code is broken?

Present this list to the user before writing tests. Let them cut or add.

## Step 3: Execute

Write the tests. All files go in `tests/`. Follow the existing naming conventions in that directory.

**Unit tests** — isolate one function/module, hit boundary values and error paths
**Integration tests** — chain real components together, inject bad data between them  
**E2e validation** — run the full flow with unexpected inputs or sequences
**Code review** — if a weakness is structural (can't be caught by a test), write a comment or inline note explaining the risk

For each test:
- Name it after what it's trying to break, not what it's testing (e.g. `test_returns_empty_on_null_input` not `test_process_data`)
- Assert the exact failure mode, not just "it doesn't crash"

## Step 4: Create or update the test runner

All tests must be runnable with one command. After writing tests, create or update `tests/run.sh`:

```sh
#!/bin/bash
# Usage:
#   ./tests/run.sh          → run all tests
#   ./tests/run.sh unit     → run only unit tests
#   ./tests/run.sh int      → run only integration tests
#   ./tests/run.sh e2e      → run only e2e tests
#   ./tests/run.sh <pattern>→ run tests matching a name pattern
```

- Detect the project's test framework (pytest, jest, go test, cargo test, etc.) and use it — don't invent a custom runner
- Support filtering by type (`unit`, `int`, `e2e`) and by pattern (passed as argument)
- Exit with a non-zero code on any failure so CI can use it
- If a runner already exists, extend it rather than replace it

Make `run.sh` executable (`chmod +x tests/run.sh`) after writing it.

## Step 5: Validate output results

After writing and running the tests, validate that the actual outputs are correct — not just that the code doesn't crash.

- **Shape** — is the output the right type, structure, length?
- **Values** — are the values in a reasonable range? Any nulls, NaNs, negatives where impossible?
- **Consistency** — same input → same output every time? Does order matter when it shouldn't?
- **Contracts** — does the output honor any documented guarantees (sorted, unique, non-empty)?
- **Side effects** — did the function change something it shouldn't have (mutated input, wrote a file, made a network call)?

For each unexpected output, write an assertion that pins the correct behavior. If the correct behavior is unclear, flag it explicitly as an unspecified contract.

## Step 5: Report

After writing and validating, summarize:
- How many attack vectors found
- How many tests written (by type)
- Which vectors are covered by tests vs. flagged as structural risks
- Any output validation failures or unspecified contracts found
- Any finding that warrants immediate attention
