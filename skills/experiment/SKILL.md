---
name: experiment
description: Run a lightweight plan -> act -> analyze experiment to answer a question the cheapest way that still gives a trustworthy verdict. Use when a question can't be resolved by exploring alone and needs something actually run (script, query, test) to get evidence, or when invoked as /experiment.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Skill, AskUserQuestion
---

# Experiment

Turn a question into a minimal scientific-method run instead of guessing at an answer.

1. **Plan.** Run `/ponytail` (Skill tool) to find the cheapest method that would resolve the question, and state what result would count as supported/refuted. Completion criterion: a stated method and a stated pass/fail expectation.
2. **Act.** Execute the method for real — script, query, test, read — not a simulated or imagined result. Completion criterion: real output captured, not inferred.
3. **Analyze.** Compare the real result against the plan's expectation and state a verdict: supported, refuted, or inconclusive.

Write the plan, raw output, and verdict under `.context/experiment/{slug}/` (kebab-case slug of the question), in `../references/document-style.md` style.

Completion criterion: the question has a stated verdict backed by real, recorded output.
