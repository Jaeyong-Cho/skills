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
- **MUST FOLLOW** `/ponytail` skill to do not overengineer. Think about the cheapest way to get a verdict, not the fanciest.
- **MUST DESIGN** strategy at this agent to make answer the questions and request for sub-agents.
- **Prior stage output is first priority.** Each stage reads what the last stage wrote and treats it as sufficient; don't re-explore or re-grep to double-check it. Fall back to fresh `/explore` only for a genuine gap.

## Multi-question fan-out

Runs once, before Stages, only when root `goal.md` has more than one `## Question N` heading with no `**Answer:**` line beneath it, and the request doesn't name a single one of them. Request names one question -> skip this section, go straight to Stages for that slug as normal.

Stay resident as the orchestrator (this invocation) rather than handing the whole run off — the shared files touched at the end of Publish (`goal.md`, `README.md`, `questions/index.html`) aren't safe to write from several concurrent subagents, so this parent does that part itself, once, after the parallel work lands.

1. **MUST DISPATCH** one claude-sonnet-5 subagent (Agent tool) per open, unanswered question — all in a single message, `run_in_background: true` — each briefed to run Stages (Explore -> Core/Viewpoints) for exactly that one `## Question N` heading's slug, then Publish steps 1-3 only (report, HTML render, handoff manifest — all scoped under `questions/{slug}/`). Tell each subagent explicitly **not** to touch `README.md`, `goal.md`, or run either rebuild script — that's this parent's job, next. Have it report back the verdict line.
2. Wait for every subagent to finish.
3. For each question, in turn: append the README bullet and the `goal.md` Answer line (Publish steps 4-5).
4. Once all questions are updated, run the two rebuild scripts (Publish steps 6-7) a single time — they do a full rewrite from `goal.md`'s current state, so running them once at the end covers every question; no need to re-run per question.
5. Summarize the batch: one line per question (slug — verdict), before ending the turn.

A subagent that fails or comes back inconclusive doesn't block the others — report it in the summary and still run steps 3-4 for the ones that succeeded.

## Stages

Three gated stages, each detailed in its own reference under `references/` — **read only the one you're about to run.** Each ends in a gate: if the result already resolves the question, hand off and stop.

1. **Explore** — `references/explore-stage.md`. Locates/creates the question's directory; its gate resolves directly, skips straight to Viewpoints (evidence worth seeing, not testing), or sends you to Core.
2. **Core** — `references/core-stage.md`. Grill once, then one or more attempts (hypothesis, method, execute, analyze), each picking cheap or full tier fresh based on what that attempt's angle needs; its next-attempt gate loops back to another attempt (usually a new angle, same cheap tier), or its viewpoints gate sends you to Publish or to Viewpoints.
3. **Viewpoints** — `references/viewpoints-stage.md`. Builds the gallery, then Publish. Reachable directly from Explore (no hypothesis) or from Core (after a verdict).

## Publish

Runs once a gate stops at Explore-to-Viewpoints, Core, or later (skip entirely if Explore's gate already resolved the request in words). Every field below has a source file from an earlier stage — read it, don't re-derive. If the core stage never ran (explore -> viewpoints direct), the report has no hypothesis to state — see the template's note on that case.

**MUST DISPATCH** one claude-haiku-4-5 subagent (Agent tool) to perform steps 1-7 below directly — assembling and writing every file itself, not returning content for the orchestrator to write. Brief it with every stage's real artifacts that ran (hypothesis/result/method/raw under `experiments/`, or `.context/explore/` evidence if Explored) plus the path `references/report-template.md` — tell it to read that file itself rather than inlining the template in the brief. `run_in_background: false`. Read back only confirmation that `report.md`'s Verdict line and `goal.md`'s Answer line were written before treating the question as closed.

1. **Write the report.** Assemble `questions/{slug}/report.md` per `references/report-template.md` from real artifacts of the stages actually run. Verdict first, not buried.
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

Report template: `references/report-template.md`.
