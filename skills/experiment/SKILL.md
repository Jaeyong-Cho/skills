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

4. **Write it up with `@skills/to-paper`.** **MUST KEEP** any script/query/asset used in step 2 as a real file under `experiments/{nn}-{slug}.raw/`, sibling to the write-up below — copy it there if it started elsewhere (e.g. a scratch dir) — plus one `regenerate.sh` (or equivalent) in that same folder that reproduces the whole Act step end-to-end with a single command, so a human re-runs the experiment themselves instead of reading the script. The plan, raw output, and verdict become that skill's manifest sections — reuse this session's Plan/Act/Analyze, don't run a fresh grill-me round:
   - Introduction — the question, and why it needed an experiment instead of just exploring.
   - Background — context the reader needs to follow the method (skip filling with restated Introduction text if there's genuinely nothing more).
   - Methodology — step 1's method and stated pass/fail expectation.
   - Results — step 2's real output; reference `regenerate.sh` and the `.raw/` files by their exact path.
   - Conclusion — step 3's comparison and verdict (supported/refuted/inconclusive).
   Skip `to-paper`'s own directory-confirmation step — the location is already fixed here: if this session already wrote `experiments/{nn}-{slug}/` for the same question, update its `manifest.json` in place and re-run `to-paper`'s lint+build with the new run instead of starting another one. Otherwise, read `../references/research-topic-directory.md` first — confirm `{NN}-{slug}` with the user (new directory vs. an existing one from today) before writing, skipping re-asking if already confirmed earlier this session — then write to `{NN}-{slug}/experiments/{nn}-{slug}/` under `~/wiki/today/research/` (`{nn}` the next zero-padded sequence number inside `experiments/`, counting existing `{nn}-{slug}.raw/` dirs; starts at `01`), following `@skills/to-paper`'s own steps 2 onward (manifest → diagram type → diagrams → lint → build) from there.

Completion criterion: the question has a stated verdict backed by real, recorded output, and `to-paper`'s lint is clean.
