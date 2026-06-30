---
name: evaluate
description: Evaluate skill. Runs the test plan from an ADR and writes a verdict report. Use when invoked as /evaluate.
disable-model-invocation: true
---

# Evaluate

List all files in `source-of-truth/adr/`. If multiple exist, ask the user which ADR to evaluate. If one exists, use it.

Use this after new implementation or after a fix — re-evaluate any time to verify the result still holds.

Read the selected ADR's **Test-Loop Design** and **Evaluation Criteria**. Read `../references/test-loop.md`.

Run the test-loop — this is the primary evaluation signal. Unit test results are not the main scope.
1. Apply clean state — reset and initialize exactly what the design specifies.
2. Apply environment setup.
3. Run each named behavior scenario.
4. For each scenario: compare actual output against expected. Flag every unexpected result.
5. For every unexpected result: trace the root cause through debug output and logs — do not just report it, explain why it happened.
6. Group all unexpected results — what pattern do they share? Name the pattern (e.g. "all failures on empty input", "fails only on large payloads"). Identify the likely single root cause of the pattern.

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a slug from the ADR being evaluated.

Write the report to `source-of-truth/evaluate/{timestamp}-{slug}.md`. Keep the format simple — no strict structure required. The report must clearly communicate:

- **Good** — what is working as expected
- **Unexpected / Ambiguous / Needs check** — anything surprising, unclear, or worth revisiting, each with a root cause traced from debug output and logs
- **Patterns** — unexpected results grouped by shared pattern, each named with a single root cause
- **Next steps** — if anything needs fixing: "Run /attack on [X]"

`mkdir -p source-of-truth/evaluate` if needed. Tell the user the file path.

If failures exist, flag each as a target: "Run /attack on [X]." Those findings feed back into /directing.

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `source-of-truth/wiki/` at any time.

**DO NOT START IMPLEMENT**
