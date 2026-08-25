---
name: experiment
description: Run a lightweight plan -> act -> analyze experiment to answer a question the cheapest way that still gives a trustworthy verdict. Use when a question can't be resolved by exploring alone and needs something actually run (script, query, test) to get evidence, or when invoked as /experiment.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Skill, AskUserQuestion
---

# Experiment

Turn a question into a minimal scientific-method run instead of guessing at an answer.

1. **Plan.** Run `/ponytail` (Skill tool) to find the cheapest method that would resolve the question, and state what result would count as supported/refuted. If the question is "does this state model / logic feel right?" or "what should this look like?", the cheapest method is usually a throwaway prototype — see `../references/prototype.md`. Completion criterion: a stated method and a stated pass/fail expectation.
2. **Act.** Execute the method for real — script, query, test, read — not a simulated or imagined result. **MUST NOT** write to or edit an external tool/dependency in place (an installed package, a vendored library, a system binary, anything outside the target project this experiment is about) — read it, or `cp` it to a scratch location first if the experiment needs a modified copy to run against. Keep whatever file did the running (script, query, scratch project) — don't let it live only in a shell history or a `/tmp` dir that evaporates. Completion criterion: real output captured, not inferred, and the file that produced it saved.
3. **Analyze.** Compare the real result against the plan's expectation and state a verdict: supported, refuted, or inconclusive.

4. **Write it up as a markdown report**, same Title/Abstract/Introduction/Background/Methodology/Results/Conclusion shape as `@skills/to-paper` but plain markdown, no figures required:
   ```markdown
   # {Title}

   ## Abstract
   {one paragraph: question + verdict}

   ## 1. Introduction
   {the question, and why it needed an experiment instead of just exploring}

   ## 2. Background
   {context the reader needs to follow the method}

   ## 3. Methodology
   {step 1's method and stated pass/fail expectation}

   ## 4. Results
   {step 2's real output; reference `regenerate.sh` and the `.raw/` files by their exact path}

   ## 5. Conclusion
   {step 3's comparison and verdict: supported/refuted/inconclusive}
   ```
   **MUST KEEP** any script/query/asset used in step 2 as a real file under `experiments/{nn}-{slug}.raw/`, sibling to this report — copy it there if it started elsewhere (e.g. a scratch dir) — plus one `regenerate.sh` (or equivalent) in that same folder that reproduces the whole Act step end-to-end with a single command, so a human re-runs the experiment themselves instead of reading the script.
5. **Write it.** If this session already wrote an `experiments/{nn}-{slug}.md` file for the same question, update that file (and its `.raw/` dir) in place with the new run instead of creating another one. Otherwise, read `../references/research-topic-directory.md` first — confirm `{NN}-{slug}` with the user (new directory vs. an existing one from today) before writing, skipping re-asking if already confirmed earlier this session — then write to `{NN}-{slug}/experiments/{nn}-{slug}.md` under `~/wiki/today/research/`, `{nn}` the next zero-padded sequence number inside `experiments/` (count existing files there; starts at `01`).
6. **Lint the report.** Run `python3 scripts/lint_report.py {NN}-{slug}/experiments/{nn}-{slug}.md` (relative to this skill's directory) — same title-length/paragraph-count/sentence-count/word-count rules as `to-paper`, reused from its `lint_paper.py`, minus any diagram requirement. Fix every reported violation in the file and re-run until clean.

Completion criterion: the question has a stated verdict backed by real, recorded output, and step 6's lint is clean.
