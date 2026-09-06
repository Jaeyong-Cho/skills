---
name: experiment
description: Run a lightweight plan -> act -> analyze experiment to answer a question the cheapest way that still gives a trustworthy verdict. Use when a question can't be resolved by exploring alone and needs something actually run (script, query, test) to get evidence, or when invoked as /experiment.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Skill, AskUserQuestion
---

# Experiment

Turn a question into a minimal scientific-method run instead of guessing at an answer.

1. **Plan.** Run `/ponytail` (Skill tool) to find the cheapest method that would resolve the question, and state what result would count as supported/refuted. If the question is "does this state model / logic feel right?" or "what should this look like?", the cheapest method is usually a throwaway prototype — see `../references/prototype.md`. Completion criterion: a stated method and a stated pass/fail expectation. Before act **MUST CONFIRM** The experiment plan and ask user with this `../references/question-format.md` ❓/➡️ format
2. **Act.** Execute the method for real — script, query, test, read — not a simulated or imagined result. **MUST NOT** write to or edit outside this experiments directory — read it, or `cp` it to a scratch location first if the experiment needs a modified copy to run against. Keep whatever file did the running (script, query, scratch project) — don't let it live only in a shell history or a `/tmp` dir that evaporates. Completion criterion: real output captured, not inferred, and the file that produced it saved.
3. **Analyze.** Compare the real result against the plan's expectation and state a verdict: supported, refuted, or inconclusive.

4. **Write it up as a markdown report** with the Title/Abstract/Introduction/Background/Methodology/Results/Discussion/Conclusion structure below. No figures are required; write the markdown directly:
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

   ## 5. Discussion
   {what the result means, how it compares with what was expected/prior context, and any limitations of the method}

   ## 6. Conclusion
   {step 3's comparison and verdict: supported/refuted/inconclusive}
   ```
   **MUST KEEP** any script/query/asset used in step 2 as a real file under `experiments/{nn}-{slug}.raw/`, sibling to this report — copy it there if it started elsewhere (e.g. a scratch dir) — plus one `regenerate.sh` (or equivalent) in that same folder that reproduces the whole Act step end-to-end with a single command, so a human re-runs the experiment themselves instead of reading the script.

   `## Results` is bound by the same paragraph/sentence/word limits as every other section (step 6 lints it) — it's for the summarized verdict-relevant numbers, not a dump of everything the run produced. If the real output has raw data/detailed statistics too voluminous for that prose (a big table of per-run numbers, log excerpts), add an unlisted `## Appendix` (or `## Appendix: Raw Data`) section after Conclusion: `lint_report.py` only checks the 7 required sections by name, so any extra `##` heading is carried through unlinted — free-form text, markdown tables, fenced code blocks, whatever the data needs. Reference it from Results in prose (e.g. "full per-run numbers in the Appendix") rather than pasting the numbers into Results itself.
5. **Write it.** If this session already wrote an `experiments/{nn}-{slug}.md` file for the same question, update that file (and its `.raw/` dir) in place with the new run instead of creating another one. Otherwise, **MUST ASK** confirmation of the directory first, per `../references/question-format.md`'s ❓/➡️ format — recommend the current directory (`./experiments/`) as the default, unless the user asks to file it under the wiki instead, in which case read `../references/research-topic-directory.md` first and confirm `{NN}-{slug}` the same way; skip re-asking if already confirmed earlier this session. Once confirmed, write to `./experiments/{nn}-{slug}.md` (creating `experiments/` if needed) or `{NN}-{slug}/experiments/{nn}-{slug}.md` under `~/wiki/today/research/`, whichever was confirmed — `{nn}` the next zero-padded sequence number inside `experiments/` (count existing files there; starts at `01`).
6. **Lint the report.** Run `python3 scripts/lint_report.py {NN}-{slug}/experiments/{nn}-{slug}.md` (relative to this skill's directory). It checks title length, paragraph counts, sentence counts, and words per sentence (per-section paragraph-count range: introduction 3-5, background 4-8, methodology 2-4, results 2-4, discussion 3-6, conclusion 1-3). Fix every reported violation in the file and re-run until clean.

Completion criterion: the question has a stated verdict backed by real, recorded output, and step 6's lint is clean.
