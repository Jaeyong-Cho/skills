---
name: experiment
description: Run an experiment on a user's request — grill the user for real intent and question (folded into /explore as one haiku-tier question, alongside any research the method needs), frame a hypothesis, design a method, execute it, analyze the results, build a visualization gallery via /viewpoints in a subagent, and write up an experiment report. Use when invoked as /experiment.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, Skill, AskUserQuestion
---

# Experiment

Turn a user's request into a small scientific-method run: hypothesis, method, execution, analysis, then a report a reader can trust without re-running it. The **verdict** — supported, refuted, or inconclusive — is the spine everything else hangs from.

Default to full latitude for running the method — install packages, run scripts, hit local services, whatever the hypothesis needs. MUST NOT remove, edit, or create anything outside `experiments/{slug}/`, except appending the summary bullet to the project root `README.md` in step 7 and regenerating `experiments/index.html` in step 8 — treat everything else as read-only. If the method needs to touch code or data elsewhere, copy it into `experiments/{slug}/raw/` first and work on the copy.

## Steps

1. **Grill the user.** Invoke the `grilling` skill (Skill tool) with the user's request as the target, focused on three things: the real intent behind the request, the real question being tested (which may not match the literal wording), and why that question matters enough to spend an experiment on. Let grilling interview the user through `AskUserQuestion` until each of the three is settled — don't shortcut to one question and move on. Skip the interview only if the user's request already states intent, question, and why unprompted, or the user explicitly asks to skip it — the grilling skill itself is invoked unmodified either way.

   Once the interview concludes — or, if skipped, once intent/question/why are confirmed directly from the request — run `../explore/SKILL.md` with a single question: "What is the user's real intent, the real question being tested, and why it matters, given this interview?" — supply the full interview (every question asked and what it resolved to, or the request itself if skipped) as that question's own context. This is a write-up of an already-decided outcome, not a new judgment call, so it lands in explore's `haiku` tier. Treat the resulting evidence file, not the raw transcript, as step 2's source.

   Done when intent, the real question, and its importance are each stated in that evidence file's Answer section, ready to carry into the hypothesis in step 2.

2. **Frame the hypothesis.** Restate the real question from step 1's evidence file as one falsifiable hypothesis (a claim that could turn out false), plus the observations that would confirm it and the ones that would refute it. Slugify the hypothesis into `{slug}` (kebab-case, e.g. `cache-ttl-vs-latency`) and create `experiments/{slug}/`. Done when the hypothesis reads as a claim (not a question) and both confirming and refuting observations are named.

3. **Design the method before touching anything.** Decide what varies (the treatment), what stays fixed (the control/baseline, if the hypothesis is comparative), what gets measured, and how — run code, benchmark, query data/logs, read source, targeted research, whatever the request actually calls for. If measurement means reading source or checking facts rather than running/benchmarking something, that's the `read source, targeted research` case — plan to answer it via `../explore/SKILL.md` in step 4 rather than reading files directly in the main thread. Write this down before executing it: a method decided after seeing results is not a method. Done when the variable(s), control, and measurement are all named.

4. **Execute the method and collect raw results.** Run it for real — actual commands, actual output — never fabricate or estimate a result to save time. For a research-shaped measurement, "running it" means invoking `../explore/SKILL.md` with the question(s) step 3 named; its evidence file(s) are the raw result, not a further summary of one — copy or write them directly under `experiments/{slug}/raw/`, don't re-derive their content in your own words. For an execution-shaped measurement, save raw output (command output, data files, logs) under `experiments/{slug}/raw/` so the report and gallery can both point back to it. Done when every measurement the method called for has a real, saved result.

5. **Analyze against the hypothesis.** Compare the raw results to the confirming/refuting observations from step 2 and reach a verdict: supported, refuted, or inconclusive (state why, if inconclusive — usually insufficient signal or an uncontrolled variable). Done when the verdict is one of the three states and each is backed by a specific result, not a general impression.

6. **Build the gallery in a subagent.** Dispatch a subagent (Agent tool) with claude-sonnet-5 model pointed at the raw results in `experiments/{slug}/raw/`, with the instruction: "with /viewpoints, build a gallery over <describe the results/data>, output to `experiments/{slug}/gallery/`." Pass `run_in_background: false` — steps 7-9 read the gallery's output and rebuild the dashboard from it, so the call must block until the subagent actually finishes, not just until it's dispatched. Isolating this in a subagent keeps viewpoints' own multi-step legwork (profiling, shortlisting, rendering) out of the main run. Done when `experiments/{slug}/gallery/index.html` exists on disk — confirm with a file check before moving on, don't infer completion from the agent's summary alone.

7. **Write the experiment report.** Assemble `experiments/{slug}/report.md` using the template below. Done when every section is filled from real artifacts of steps 1-6 (not restated boilerplate) and the report opens with the verdict, not buried at the end.

8. **Summarize in the project README.** Append a short bullet to the `## Experiments` section of the project root `README.md` (create the section, or the file, if missing) — one bullet per experiment, verdict-first, linking to the full report. Never restate the report's contents beyond that one line. Done when the bullet is added and its link resolves.

   ```
   ## Experiments
   - **Supported/Refuted/Inconclusive** — <hypothesis in a few words>: <one-line takeaway>. [Report](experiments/{slug}/report.md)
   ```

9. **Refresh the experiments dashboard.** Run `python ../goal-init/scripts/build_dashboard.py experiments experiments/index.html` (path relative to this skill's own directory) so this experiment's verdict, hypothesis, and gallery thumbnail appear alongside every prior one. This is the same script `/goal-init` uses to build the dashboard from scratch — don't reimplement it here. Done when `experiments/index.html` exists and includes this experiment's slug.

## Report template (`experiments/{slug}/report.md`)

```
# Experiment: <hypothesis, stated as a claim>

**Verdict:** Supported | Refuted | Inconclusive

## Motivation
- Intent: <why the user wanted this, from step 1's evidence file>
- Real question: <the question being tested, which may not match the literal request>
- Why it matters: <why it was worth an experiment>

## Hypothesis
- Claim: <the falsifiable claim>
- Confirms if: <the observation that would confirm it>
- Refutes if: <the observation that would refute it>

## Method
- Variable(s): <what varied>
- Control/baseline: <what stayed fixed, or "none — non-comparative">
- Measurement: <what was measured and how>

## Results
- <one bullet per finding, each referencing experiments/{slug}/raw/...>

## Analysis
- <one bullet per reasoning point tying a specific result to the verdict — not a general impression>

## Visualizations
See [gallery](gallery/index.html) — <one line on what the gallery's views add to the analysis>
```
