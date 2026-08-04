# Report template (`questions/{slug}/report.md`)

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
