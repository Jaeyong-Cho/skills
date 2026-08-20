---
name: experiment
description: Run a lightweight plan -> act -> analyze experiment to answer a question the cheapest way that still gives a trustworthy verdict. Use when a question can't be resolved by exploring alone and needs something actually run (script, query, test) to get evidence, or when invoked as /experiment.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Skill, AskUserQuestion
---

# Experiment

Turn a question into a minimal scientific-method run instead of guessing at an answer.

1. **Plan.** Run `/ponytail` (Skill tool) to find the cheapest method that would resolve the question, and state what result would count as supported/refuted. If the question is "does this state model / logic feel right?" or "what should this look like?", the cheapest method is usually a throwaway prototype — see `../references/prototype.md`. Completion criterion: a stated method and a stated pass/fail expectation.
2. **Act.** Execute the method for real — script, query, test, read — not a simulated or imagined result. Completion criterion: real output captured, not inferred.
3. **Analyze.** Compare the real result against the plan's expectation and state a verdict: supported, refuted, or inconclusive.

**MUST Write** the plan, raw output, and verdict (as sections in one file). If this session already wrote an `experiments/{nn}-{slug}.md` file for the same question, update that file in place with the new run instead of creating another one. Otherwise write to `~/wiki/today/research/{NN}-{slug}/experiments/{nn}-{slug}.md`, in `../references/document-style.md` style — `{slug}` a kebab-case slug of the question, `{NN}` the zero-padded sequence number for today, starting at `00` (count existing `NN-*` directories under `~/wiki/today/research/`), `{nn}` the next zero-padded sequence number inside `experiments/` (count existing files there; starts at `01`). `@skills/end-of-day` archives `today/research/` into the dated `~/wiki/journal/YYYY/MM/YYYY-MM-DD/research/` path at day's end.

Completion criterion: the question has a stated verdict backed by real, recorded output.
