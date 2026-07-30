---
name: experiment
description: Run an experiment on a user's request — frame a hypothesis, design a method, execute it, analyze the results, build a visualization gallery via /viewpoints in a subagent, and write up an experiment report. Use when invoked as /experiment.
disable-model-invocation: true
---

# Experiment

Turn a user's request into a small scientific-method run: hypothesis, method, execution, analysis, then a report a reader can trust without re-running it. The **verdict** — supported, refuted, or inconclusive — is the spine everything else hangs from.

## Steps

1. **Frame the hypothesis.** Restate the user's request as one falsifiable hypothesis (a claim that could turn out false), plus the observations that would confirm it and the ones that would refute it. Ask the user only if the request is too vague to convert into a testable claim. Slugify the hypothesis into `{slug}` (kebab-case, e.g. `cache-ttl-vs-latency`) and create `experiments/{slug}/`. Done when the hypothesis reads as a claim (not a question) and both confirming and refuting observations are named.

2. **Design the method before touching anything.** Decide what varies (the treatment), what stays fixed (the control/baseline, if the hypothesis is comparative), what gets measured, and how — run code, benchmark, query data/logs, read source, targeted research, whatever the request actually calls for. Write this down before executing it: a method decided after seeing results is not a method. Done when the variable(s), control, and measurement are all named.

3. **Execute the method and collect raw results.** Run it for real — actual commands, actual output — never fabricate or estimate a result to save time. Save raw output (command output, data files, logs) under `experiments/{slug}/raw/` so the report and gallery can both point back to it. Done when every measurement the method called for has a real, saved result.

4. **Analyze against the hypothesis.** Compare the raw results to the confirming/refuting observations from step 1 and reach a verdict: supported, refuted, or inconclusive (state why, if inconclusive — usually insufficient signal or an uncontrolled variable). Done when the verdict is one of the three states and each is backed by a specific result, not a general impression.

5. **Build the gallery in a subagent.** Dispatch a subagent (Agent tool) pointed at the raw results in `experiments/{slug}/raw/`, with the instruction: "with /viewpoints, build a gallery over <describe the results/data>, output to `experiments/{slug}/gallery/`." Wait for it to finish before continuing — the report in step 6 links the gallery, so it must exist first. Isolating this in a subagent keeps viewpoints' own multi-step legwork (profiling, shortlisting, rendering) out of the main run, so the report step waiting behind it doesn't rush it. Done when `experiments/{slug}/gallery/index.html` exists.

6. **Write the experiment report.** Assemble `experiments/{slug}/report.md` using the template below. Done when every section is filled from real artifacts of steps 1-5 (not restated boilerplate) and the report opens with the verdict, not buried at the end.

## Report template (`experiments/{slug}/report.md`)

```
# Experiment: <hypothesis, stated as a claim>

**Verdict:** Supported | Refuted | Inconclusive

## Hypothesis
<the claim, and what would confirm/refute it>

## Method
- Variable(s): <what varied>
- Control/baseline: <what stayed fixed, or "none — non-comparative">
- Measurement: <what was measured and how>

## Results
<the raw findings, with reference to experiments/{slug}/raw/>

## Analysis
<why the verdict follows from the results — the reasoning, not just the number>

## Visualizations
See [gallery](gallery/index.html) — <one line on what the gallery's views add to the analysis>
```
