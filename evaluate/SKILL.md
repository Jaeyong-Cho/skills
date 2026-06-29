---
name: evaluate
description: Evaluate skill. Runs the test plan from an ADR and writes a verdict report. Use when invoked as /evaluate.
disable-model-invocation: true
---

# Evaluate

List all files in `source-of-truth/adr/`. If multiple exist, ask the user which ADR to evaluate. If one exists, use it.

Use this after new implementation or after a fix — re-evaluate any time to verify the result still holds.

Read the selected ADR's **Test Plan** and **Evaluation Criteria**.

Run each test in the Test Plan. For each:
- State what it tests
- Run it
- Record pass or fail

Deliver a verdict against the Evaluation Criteria:
- **Pass** — all criteria met
- **Partial** — state what passes and what doesn't
- **Fail** — state what broke and why

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a slug from the ADR being evaluated.

Write the report to `source-of-truth/evaluate/{timestamp}-{slug}.md`:

```markdown
# Evaluate: {ADR Title}

**Date:** {YYYY-MM-DD}
**ADR:** {path to ADR}
**Verdict:** Pass / Partial / Fail

## Results

| Test | Result |
|------|--------|
| {test} | Pass / Fail |

## Verdict Detail
{What passed, what failed, why}

## Next Steps
{If failures: "Run /attack on [X] to find the root cause." If pass: "Evaluation complete."}
```

`mkdir -p source-of-truth/evaluate` if needed. Tell the user the file path.

If failures exist, flag each as a target: "Run /attack on [X]." Those findings feed back into /directing.

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `source-of-truth/wiki/` at any time.

**DO NOT START IMPLEMENT**
