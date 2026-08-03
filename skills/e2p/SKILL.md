---
name: e2p
description: Bridge experiments to production — turn research/prototypes into integrated product code via grilling, exploration, planning, implementation, and review, or via a fast track (single haiku dispatch implements and commits directly) when the integration is small and the experiment's report already fully specifies it. Use when the user names an experiment (or a goal-directory question) and a product target to integrate it into.
---

# Experiment to Product (E2P)

Turn an experiment into production code: intent capture -> reconnaissance -> plan -> implement -> review. **DO NOT READ** the codebase directly — use `/explore`.

**Experiment results are first priority.** Before exploring, grilling, or planning, read each experiment location's `report.md` (via `handoff/manifest.md`) — the authoritative source for that experiment's findings. Later steps only fill what it leaves open, never re-derive what it already states.

## 1. Gather inputs and set up the session

Collect from the user:
- experiment location(s) — a path, a URL, or a `## Question N` in a `goal.md` (see `../experiment/references/pipeline.md`): resolve by content match to its existing `questions/{slug}/` directory (don't re-slugify); if several questions match, ask via `AskUserQuestion` rather than guessing
- product target — where the code lands (e.g. `apps/web/`)
- integration goal — what to accomplish and success criteria

Multiple experiment locations are fine when several prototypes feed one integration — treat each independently through step 4, then reconcile into one plan in step 5 (note in `plan/index.md` which piece each experiment is responsible for). Judge integration size now too (single file/module vs. multi-module/new architecture) — it shapes how much the plan in step 4 needs to break down.

Create `{product_repo_root}/.context/{YYYYMMDD-HHMM}-{goal-slug}/` for this session's artifacts: `intent.md`, `experiments/`, `product/`, `plan/`, `implementation/`, `review/`.

## Fast track — skip straight to implementation?

Judge this before step 2, every time. Fast-track when **all** hold:
- single experiment location, single small product target (one file/module, not multi-module/new architecture)
- that experiment's `report.md` already fully specifies what to build — a clear `Verdict`, concrete Method/Results, nothing architecturally ambiguous left for grilling or planning to resolve
- the user asked to move fast, or the integration is obviously this small on its face (a config value, a small function, wiring one already-proven snippet into one call site)

If any of those doesn't hold, skip this section — continue to step 2 as normal.

**MUST DISPATCH** one claude-haiku-4-5 subagent (Agent tool), briefed with the experiment's `report.md` directly, the product target, and the integration goal, to: read `report.md` (via `handoff/manifest.md` if present), implement the change directly in the product target, run the test(s) that prove it (existing + new), then commit. `run_in_background: false`. Have it save its actual test output (pass/fail, not a summary) to `{product_repo_root}/.context/{YYYYMMDD-HHMM}-{goal-slug}/implementation/fast-track.md`, alongside a one-line note of which report.md it worked from.

**Output:** code changes committed (or staged) in the product repo; `implementation/fast-track.md`. Session complete — skip steps 2 through 6 and go straight to step 7's handoff (grill/plan/review artifacts will be absent; that's expected on this path, not a gap).

## 2. Explore experiment and product (subagents via `/explore`)

**Check for prior artifacts first.** For each experiment location, look for `handoff/manifest.md` — it links that question's `report.md`, `.context/explore/`, and (if the core stage ran) `.context/grilling/` as machine-readable evidence, plus `gallery/index.html` as human-only reference (skip reading it — already summarized in `report.md`). Treat the machine-readable links as ground truth. No `.context/grilling/` link is expected on the explore-to-viewpoints path (`**Verdict:** Explored`), not a missing artifact — fall back to the report's Motivation section there. No manifest at all (pre-dates this convention, or wasn't built with `/experiment`): fall back to `report.md` directly.

Delegate to `explore` only for what the prior artifacts leave open, on up to two fronts in parallel:
- **Experiments branch** — skip per experiment if its manifest already covers implementation patterns, data structures, assumptions, lessons learned; otherwise research what it doesn't answer.
- **Product branch** — always runs once: existing patterns, dependencies, architecture, integration points in the product codebase.

**Output:** `experiments/{exp-slug}/{question-slug}.md` (as needed) and `product/{question-slug}.md`.

## 3. Grill for intent

**Check for prior grilling first.** Pass any experiment's `.context/grilling/` in as prior intent. A location on the explore-to-viewpoints path has none to reuse — grill it from scratch, same as a location with no manifest. Also pass in the product repo's `goal.md` if it exists. Scope this grill to what those files don't cover: product-specific unknowns (deployment target, non-negotiables, constraints) and, with multiple experiments, how their findings reconcile.

Run `/grilling` with the exploration findings (and any prior grilling output) as background. Output pins down: what success looks like, non-negotiables vs. nice-to-haves, known constraints, risk surface.

**Output:** `intent.md`.

## 4. Plan implementation (Sonnet-5, foreground)

Brief the subagent with each experiment's `report.md` (Method, Results, Analysis) directly, not just `intent.md` — the plan builds on what was already tried, not a re-derivation from product code alone.

**MUST DISPATCH sub-agent** (Agent tool) with claude-sonnet-5 model, run to `/p4d`, to plan: where code lands, what refactors/scaffolding are needed, dependency/integration points, a step-by-step change list structured as **implement -> test -> commit** per change — with risk annotations, grouped into parallel-execution groups. Per `/p4d`'s own convention, this writes `plan/index.md` (group table: steps, depends_on, file) plus one `plan/group-{n}.md` per group — not a single flat file.

**Output:** `plan/index.md`, `plan/group-{n}.md` per group.

## 5. Implement (Haiku-4.5, foreground)

Read `plan/index.md`'s group table. For each dependency wave (groups with no unmet `depends_on`, dispatched together; wait for a wave to finish before the next), **MUST DISPATCH** one claude-haiku-4-5 subagent per group, each given only that group's `plan/group-{n}.md` — via `/work`, to execute its implement -> test -> commit entries: apply the change, run the test(s) that prove it (existing + new), then commit. Each subagent saves its actual test output (pass/fail, not a summary) to `implementation/test-results/group-{n}.md` — namespaced per group so concurrent dispatches never write over each other; step 6 reads the whole directory rather than re-running anything.

**Output:** code changes committed (or staged) in the product repo; `implementation/test-results/group-{n}.md` and other logs in `implementation/`.

## 6. Review against the goal (Sonnet-5, foreground)

**MUST DISPATCH sub-agent** (Agent tool) with claude-sonnet-5 model — briefed with `intent.md`, `plan/index.md` (plus its group files), and everything under `implementation/test-results/`, to review the implementation against the integration goal: completeness vs. plan, whether the saved test results actually validate the goal (not just that tests passed), integration risk, production readiness. Sonnet, not haiku, since judging "does this satisfy the goal" is the reasoning-heavy call this step exists for.

**Output:** `review/report.md`.

## 7. Handoff

Full pipeline: session complete when intent signed off, exploration evidence collected, plan risk-annotated, implementation committed, review has no critical blockers. Fast track: session complete when `implementation/fast-track.md` shows a passing commit — no intent/plan/review artifacts to check, by design. Leave `.context/{timestamp}-{goal}/` intact for audit trail either way.
