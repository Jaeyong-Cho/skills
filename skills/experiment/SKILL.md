---
name: experiment
description: Run an experiment on a user's request — explore codebase/domain context first, grill for real intent and question, frame a hypothesis, design and execute a method, analyze results, build a gallery via /viewpoints in a subagent, and write up a report. Use when invoked as /experiment.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, Skill, AskUserQuestion
---

# Experiment

Turn a user's request into a small scientific-method run: hypothesis, method, execution, analysis, then a report a reader can trust without re-running it. The **verdict** — supported, refuted, or inconclusive — is the spine everything else hangs from.

Default to full latitude for running the method — install packages, run scripts, hit local services, whatever the hypothesis needs. MUST NOT remove, edit, or create anything outside `experiments/{slug}/`, except appending the summary bullet to the project root `README.md` in step 9 and regenerating `experiments/index.html` in step 10 — treat everything else as read-only. If the method needs to touch code or data elsewhere, copy it into `experiments/{slug}/raw/` first and work on the copy.

- The context of this session is in the `experiments/{slug}/.context/` directory.
- The context of this goal's context is in the `.context/` directory.
- Defaultly **DO NOT READ** codebase directly at the parent agent. **MUST USE** the existing context information `/explore` skill to research and explore for getting informations.

## Steps

1. **Explore for context.** Before interviewing the user, **MUST RUN** `../explore/SKILL.md` for each purposes, posing a single open-ended question grounded in the user's raw request: "What codebase/domain context is relevant to <the user's request>, and what would ground an interview about it?" This is open-ended reconnaissance, not a narrow lookup, so it's explore's `sonnet` tier. Save the evidence file under `experiments/{slug}/.context/explore-context/` — the `{slug}` directory itself is only created in step 3, once the hypothesis exists; treat this as the same forward reference step 2's grilling output uses. Done when the evidence file exists and is ready to hand to step 2 as interview background.

2. **Grill the user.** Run the `grilling` skill on the user's request, giving it step 1's evidence file as background — and the project root `goal.md`, if it exists (written by `/goal-init`), since it states the project's declared goal and grounds why this experiment matters to it. Focus on three things: the real intent, the real question being tested (may not match the literal wording), and why it matters enough to spend an experiment on. Pass `run_in_background: false` so the interview completes before proceeding. And make sure the subagent's output is saved to `experiments/{slug}/.context/grilling/` so it can be referenced in step 3.

3. **Frame the hypothesis.** Restate the real question from step 2's evidence file as one falsifiable hypothesis (a claim that could turn out false), plus the observations that would confirm it and the ones that would refute it. Slugify the hypothesis into `{slug}` (kebab-case, e.g. `cache-ttl-vs-latency`) and create `experiments/{slug}/`. Write hypothesis.md. Done when the hypothesis reads as a claim (not a question) and both confirming and refuting observations are named.

4. **Design the method before touching anything.** **MUST DISPATCH** a subagent (Agent tool) with claude-sonnet-5 model, decide what varies (the treatment), what stays fixed (the control/baseline, if comparative), what gets measured, and how — run code, benchmark, query data/logs, read source, whatever the request calls for with `/p4d` skill. Write this down to the method.md before executing: a method decided after seeing results isn't a method. Done when variable(s), control, and measurement are all named.

5. **Execute the method and collect raw results.** **MUST DISPATCH** a subagent (Agent tool) with claude-haiku-4.5 model, briefed with step 4's method exactly as decided, to run it for real with `/work` skill parallelly according to groups and depends — actual commands, actual output, never fabricate or estimate — and save every raw result (command output, data, logs) under `experiments/{slug}/raw/` so the report and gallery can point back to it. Pass `run_in_background: false` so execution completes before proceeding. Done when every measurement has a real, saved result.

6. **Analyze against the hypothesis.** Compare the raw results to the confirming/refuting observations from step 3 and reach a verdict: supported, refuted, or inconclusive (state why, if inconclusive — usually insufficient signal or an uncontrolled variable). Done when the verdict is one of the three states and each is backed by a specific result, not a general impression.

7. **Build the gallery in a subagent.** **MUST DISPATCH** a subagent (Agent tool) with claude-sonnet-5 model pointed at the raw results in `experiments/{slug}/raw/`, with the instruction: "with /viewpoints skill, build a gallery over <describe the results/data>, output to `experiments/{slug}/gallery/`." Haiku is enough here — the gallery is human-only reference (see step 9), not something a decision hangs on. Pass `run_in_background: false` — steps 8-10 read the gallery's output and rebuild the dashboard from it, so the call must block until the subagent actually finishes, not just until it's dispatched. Isolating this in a subagent keeps viewpoints' own multi-step legwork (profiling, shortlisting, rendering) out of the main run. Done when `experiments/{slug}/gallery/index.html` exists on disk — confirm with a file check before moving on, don't infer completion from the agent's summary alone.

8. **Write the experiment report.** Assemble `experiments/{slug}/report.md` using the template below. Done when every section is filled from real artifacts of steps 1-7 (not restated boilerplate) and the report opens with the verdict, not buried at the end.

9. **Package the handoff.** Create `experiments/{slug}/handoff/manifest.md` with relative links to `../report.md`, `../.context/grilling/`, and `../.context/explore-context/` — mark these as machine-readable, for downstream tooling (e.g. `/e2p`) to read as evidence. Also link `../gallery/index.html`, labeled explicitly as human-only reference (rendered HTML, not something an agent should parse for findings) — the report's prose already carries anything the gallery shows. This is the single path downstream tooling should read — it should never need to know this skill's internal layout. Done when `manifest.md` exists and every link in it resolves.

10. **Summarize in the project README.** Append a short bullet to the `## Experiments` section of the project root `README.md` (create the section, or the file, if missing) — one bullet per experiment, verdict-first, linking to the full report. Never restate the report's contents beyond that one line. Done when the bullet is added and its link resolves.

    ```
    ## Experiments
    - **Supported/Refuted/Inconclusive** — <hypothesis in a few words>: <one-line takeaway>. [Report](experiments/{slug}/report.md)
    ```

11. **Refresh the experiments dashboard.** Run `python ../goal-init/scripts/build_dashboard.py experiments experiments/index.html` (path relative to this skill's own directory) so this experiment's verdict, hypothesis, and gallery thumbnail appear alongside every prior one. This is the same script `/goal-init` uses to build the dashboard from scratch — don't reimplement it here. Done when `experiments/index.html` exists and includes this experiment's slug.

## Report template (`experiments/{slug}/report.md`)

```
# Experiment: <hypothesis, stated as a claim>

**Verdict:** Supported | Refuted | Inconclusive

## Motivation
- Intent: <why the user wanted this, from step 2's evidence file>
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
