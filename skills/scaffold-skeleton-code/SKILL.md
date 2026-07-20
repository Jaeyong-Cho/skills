---
name: scaffold-skeleton-code
description: Generate skeleton code with TODOs and tests for implementation
disable-model-invocation: true
compatibility: none
---

# Scaffold Skeleton Code

You describe what you want to build. This skill generates the skeleton — function signatures, test file, and brief TODO hints — so you implement the actual logic.

## How it works

1. **You provide:** feature description, language, any specific structure preferences
2. **Skill generates:**
   - Skeleton code file (all function signatures + TODO comments with brief hints)
   - Test file (comprehensive tests covering the skeleton)
   - Implementation guide (list of what each function should do)
3. **You implement:** fill in the function bodies with actual logic

## What the skill produces

### Skeleton Code
- All function/method signatures (with type hints if the language supports them)
- Detailed TODO comments on each function with implementation hints, edge cases, and constraints
- Module/class structure set up
- Imports stubbed out where needed

Example TODO hint:
```python
def calculate_total(items):
    # TODO: Sum the price of all items. Handle edge case: empty list returns 0.
    pass
```

### Test File
- One test per skeleton function (or logical group)
- Tests use realistic inputs and edge cases
- Tests are ready to run immediately (they will fail until you implement)
- Tests are written in the language's standard testing framework

## Process

1. **Describe the feature** — what you're building, in a few sentences
2. **Specify language** — Python, TypeScript, Go, etc.
3. **Optional: add constraints** — "no external dependencies", "must be async", etc.
4. Skill generates skeleton code and tests
5. **You implement** — write the function bodies using TODO hints as your guide

That's it. Ask for help if you get stuck on a specific function, but the scaffolding is done.

## Tips

- Tests come first (in the output) so you can see what success looks like before implementing
- If a TODO hint is unclear, ask for clarification before implementing
- Run tests as you go — they'll guide you toward working code
- Skeleton code is language-idiomatic: Python gets dataclasses, TypeScript gets interfaces, etc.
