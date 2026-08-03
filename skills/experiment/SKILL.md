---
name: experiment
description: Run an experiment through three gated stages — explore, then (if needed) hypothesize/method/execute/analyze, then (if needed) build a /viewpoints gallery. Each stage hands off and stops as soon as it resolves the question, instead of always running to the end. Use when invoked as /experiment.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, Skill, AskUserQuestion
---

# Experiment

Turn a request into a scientific-method run: hypothesis, method, execution, analysis, then a report a reader can trust without re-running it. The **verdict** — supported, refuted, or inconclusive — is the spine everything hangs from.

Full latitude for running the method (install packages, run scripts, hit local services). MUST NOT touch anything outside `questions/{slug}/`, except appending to root `README.md` and regenerating `questions/index.html` in Publish.

- `{slug}` names a `## Question N` heading in root `goal.md`; its directory is created by `/goal-init` before this skill runs — see `references/pipeline.md`. No `goal.md` -> the explore stage stops and says so.
- **DO NOT** read the codebase directly — use `/explore`.
- **Prior stage output is first priority.** Each stage reads what the last stage wrote and treats it as sufficient; don't re-explore or re-grep to double-check it. Fall back to fresh `/explore` only for a genuine gap.

## Stages

Three gated stages, each detailed in its own reference under `references/` — **read only the one you're about to run.** Each ends in a gate: if the result already resolves the question, hand off and stop.

1. **Explore** — `references/explore-stage.md`. Locates/creates the question's directory; its gate resolves directly, skips straight to Viewpoints (evidence worth seeing, not testing), or sends you to Core.
2. **Core** — `references/core-stage.md`. Grill, hypothesis, method, execute, analyze; its gate sends you to Publish or to Viewpoints.
3. **Viewpoints** — `references/viewpoints-stage.md`. Builds the gallery, then Publish. Reachable directly from Explore (no hypothesis) or from Core (after a verdict).

## Publish

Runs once a gate stops at Explore-to-Viewpoints, Core, or later (skip entirely if Explore's gate already resolved the request in words). Every field below has a source file from an earlier stage — read it, don't re-derive. If the core stage never ran (explore -> viewpoints direct), the report has no hypothesis to state — see the template's note on that case.

1. **Write the report.** Assemble `questions/{slug}/report.md` (template below) from real artifacts of the stages actually run. Verdict first, not buried.
2. **Package the handoff.** `questions/{slug}/handoff/manifest.md` with relative links to `../report.md`, `../.context/explore/`, `../.context/grilling/` (omit if the core stage never ran), and — if Viewpoints ran — `../gallery/index.html` (labeled human-only reference). This is the single path downstream tooling (e.g. `/e2p`) should read.
3. **Update the README.** Append one bullet to `## Experiments` in root `README.md` (create if missing), verdict-first, nothing beyond one line:
   ```
   ## Experiments
   - **Supported/Refuted/Inconclusive** — <hypothesis in a few words>: <takeaway>. [Report](questions/{slug}/report.md)
   ```
4. **Refresh the dashboard.** `python ../goal-init/scripts/build_dashboard.py questions questions/index.html` (path relative to this skill's directory) — same script `/goal-init` uses, don't reimplement it.

## Report template (`questions/{slug}/report.md`)

Motivation/Hypothesis/Method are key-value (single-subject attributes, per `../../references/document-style.md`); Results/Analysis are bullets (list-shaped). `**Verdict:**` stays bolded prose, not key-value — `build_dashboard.py` parses it with `\*\*Verdict:\*\*\s*(\w+)` and would break on a renamed field.

**If the core stage never ran** (explore -> viewpoints direct, no hypothesis was framed): use `**Verdict:** Explored`, title the heading from the question itself rather than a claim, and write `Hypothesis`, `Method`, `Analysis` as `not applicable — evidence explored and visualized, no claim tested`; `Motivation` still comes from the explore evidence's Answer section (there's no grilling output on this path).

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
- <one bullet per finding, referencing questions/{slug}/raw/... — or, if Explored, referencing questions/{slug}/.context/explore/...>

## Analysis
- <one bullet per reasoning point tying a result to the verdict, or "not applicable — no claim tested">

## Visualizations
See [gallery](gallery/index.html) — <what it adds>, or "Not built — not needed to resolve the question." if Viewpoints was skipped
```
