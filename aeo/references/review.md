# Code Review Mode

Output file: `.aeo/src/reviews/<slug>.md`

## Process

For each piece of code, identify which layer it belongs to and flag violations:

- Axiology mixed into Epistemology (e.g., scoring logic tangled with execution logic)
- Ontology shaped by a specific Epistemology (entity changes shape for one caller)
- Missing Axiology (selection/evaluation done implicitly, not explicitly)
- Monolithic code where all three layers are entangled

Structure each finding as: **[Layer] Issue → Why it matters → Suggested fix**

If layers are cleanly separated, say so — don't invent problems.

## Output structure

```markdown
# Code Review: <title>

## Layer Classification
<table or bullets mapping code sections to their AEO layer>

## Findings

### [Layer] <Issue title>
**Why it matters**: ...
**Suggested fix**: ...

## Summary
<overall assessment — what's working, what needs attention>
```

Add the file as a nested entry in `.aeo/src/SUMMARY.md` under `Code Reviews`.
