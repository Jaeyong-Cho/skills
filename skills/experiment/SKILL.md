---
name: experiment
description: Run an experiment through three gated stages — explore, then (if needed) one or more attempts, each a cheap one-shot check by default and each free to take a different angle on the question, stepping up to a full p4d/haiku-swarm method only for the specific angle that needs more rigor than a quick check can give. Each stage hands off and stops as soon as it resolves the question, instead of always running to the end. Use when invoked as /experiment.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, Skill, AskUserQuestion
---

# Experiment

Turn a request into a scientific-method run: hypothesis, method, execution, analysis, then a report a reader can trust without re-running it. The **verdict** — supported, refuted, or inconclusive — is the spine everything hangs from.

Full latitude for running the method (install packages, run scripts, hit local services). MUST NOT touch anything outside `questions/{slug}/`, except appending to root `README.md` and `goal.md`, and regenerating `questions/index.html`, in Publish.

- `{slug}` names a `## Question N` heading in root `goal.md`; its directory is created by `/goal-init` before this skill runs — see `references/pipeline.md`. No `goal.md` -> the explore stage stops and says so.
- **DO NOT** read the codebase directly — use `/explore`.
- **Prior stage output is first priority.** Each stage reads what the last stage wrote and treats it as sufficient; don't re-explore or re-grep to double-check it. Fall back to fresh `/explore` only for a genuine gap.

## Stages

Three gated stages, each detailed in its own reference under `references/` — **read only the one you're about to run.** Each ends in a gate: if the result already resolves the question, hand off and stop.

1. **Explore** — `references/explore-stage.md`. Locates/creates the question's directory; its gate resolves directly, skips straight to Viewpoints (evidence worth seeing, not testing), or sends you to Core.
2. **Core** — `references/core-stage.md`. Grill once, then one or more attempts (hypothesis, method, execute, analyze), each picking cheap or full tier fresh based on what that attempt's angle needs; its next-attempt gate loops back to another attempt (usually a new angle, same cheap tier), or its viewpoints gate sends you to Publish or to Viewpoints.
3. **Viewpoints** — `references/viewpoints-stage.md`. Builds the gallery, then Publish. Reachable directly from Explore (no hypothesis) or from Core (after a verdict).

## Publish

Runs once a gate stops at Explore-to-Viewpoints, Core, or later (skip entirely if Explore's gate already resolved the request in words). Every field below has a source file from an earlier stage — read it, don't re-derive. If the core stage never ran (explore -> viewpoints direct), the report has no hypothesis to state — see the template's note on that case.

**MUST DISPATCH** one claude-haiku-4-5 subagent (Agent tool) to perform steps 1-7 below directly — assembling and writing every file itself, not returning content for the orchestrator to write. Brief it with every stage's real artifacts that ran (hypothesis/result/method/raw under `experiments/`, or `.context/explore/` evidence if Explored) plus the report template. `run_in_background: false`. Read back only confirmation that `report.md`'s Verdict line and `goal.md`'s Answer line were written before treating the question as closed.

1. **Write the report.** Assemble `questions/{slug}/report.md` (template below) from real artifacts of the stages actually run. Verdict first, not buried.
2. **Render the report to HTML.** `python ../goal-init/scripts/render_report.py questions/{slug}/report.md` (path relative to this skill's directory) — writes `questions/{slug}/report.html`, a standalone rendered page (same theme as the gallery/dashboard) so a reader opens it straight in a browser instead of downloading the raw `.md`. Same script every run, don't reimplement it; re-run whenever `report.md` changes.
3. **Package the handoff.** `questions/{slug}/handoff/manifest.md` with relative links to `../report.html` (rendered; link `../report.md` alongside it as the source), `../.context/explore/`, `../.context/grilling/` (omit if the core stage never ran), and — if Viewpoints ran — `../gallery/index.html` (labeled human-only reference). This is the single path downstream tooling (e.g. `/e2p`) should read.
4. **Update the README.** Append one bullet to `## Experiments` in root `README.md` (create if missing), verdict-first, nothing beyond one line:
   ```
   ## Experiments
   - **Supported/Refuted/Inconclusive** — <hypothesis in a few words>: <takeaway>. [Report](questions/{slug}/report.html)
   ```
5. **Answer the question in `goal.md`.** Directly under the `## Question N` heading this `{slug}` came from, add one line:
   ```
   **Answer:** <verdict> — <takeaway, same one used above>
   ```
   Replace it in place on a later re-run (same question, new experiment) rather than stacking multiple `**Answer:**` lines under one heading.
6. **Rebuild Acceptance Criteria.** `python ../goal-init/scripts/build_acceptance_criteria.py goal.md` (path relative to this skill's directory) — same script `/goal-init` uses, don't reimplement it. Rewrites the `## Acceptance Criteria` checklist from every `**Answer:** Supported|Refuted` line in `goal.md`; Inconclusive answers don't produce a criterion. Preserves any box already checked off.
7. **Refresh the dashboard.** `python ../goal-init/scripts/build_dashboard.py questions questions/index.html` (path relative to this skill's directory) — same script `/goal-init` uses, don't reimplement it. Picks up `report.html` automatically (step 2) and links the dashboard's Report card to it instead of `report.md`.

## Report template (`questions/{slug}/report.md`)

Motivation/Hypothesis/Method are key-value (single-subject attributes, per `../../references/document-style.md`); Results/Analysis are bullets (list-shaped). `**Verdict:**` stays bolded prose, not key-value — `build_dashboard.py` parses it with `\*\*Verdict:\*\*\s*(\w+)` and would break on a renamed field.

**If the core stage never ran** (explore -> viewpoints direct, no hypothesis was framed): use `**Verdict:** Explored`, title the heading from the question itself rather than a claim, and write `Hypothesis`, `Method`, `Analysis` as `not applicable — evidence explored and visualized, no claim tested`; `Motivation` still comes from the explore evidence's Answer section (there's no grilling output on this path).

**If the core stage ran more than one attempt** (a different angle each time, and/or a step up in tier for one of them): Hypothesis/Method/Results/Analysis describe only the resolving (or final) `experiments/{n}-*/`, not every attempt — that attempt is the claim actually being reported. Add a `## Prior attempts` section (bullets) listing each earlier `experiments/{n}-*/`: its angle, tier, verdict, and why it didn't close the question — so the report doesn't read as if the resolving attempt were the only one tried, and so a future reader doesn't re-run an already-ruled-out angle.

```
# Experiment: <hypothesis, stated as a claim — or the question itself, if Explored>

**Verdict:** Supported | Refuted | Inconclusive | Explored

## Motivation
intent: <why the user wanted this, from grilling, or from the explore evidence if Explored>
real_question: <the question being tested, may differ from the literal request>
why_it_matters: <why worth an experiment>

## Hypothesis
claim: <the falsifiable claim, or "not applicable — evidence explored and visualized, no claim tested">
confirms_if: <observation that would confirm it, or "n/a">
refutes_if: <observation that would refute it, or "n/a">

## Method
variables: <what varied, or "not applicable">
control_baseline: <what stayed fixed, or "none — non-comparative", or "not applicable">
measurement: <what was measured and how, or "not applicable">

## Results
- <one bullet per finding, referencing questions/{slug}/experiments/{n}-{angle-slug}/raw/... — or, if Explored, referencing questions/{slug}/.context/explore/...>

## Analysis
- <one bullet per reasoning point tying a result to the verdict, or "not applicable — no claim tested">

## Prior attempts
<omit this section entirely if only one attempt ran, or if the core stage never ran>
- **{n}-{angle-slug}** (tier: cheap|full) — <verdict>: <why it didn't close the question, e.g. "right angle, underpowered" or "missed the cold-start case">

## Visualizations
See [gallery](gallery/index.html) — <what it adds>, or "Not built — not needed to resolve the question." if Viewpoints was skipped
```
