---
name: e2p
description: Bridge experiments to production — transform ad-hoc research into integrated product code. Takes an experiment location, a product target, and an integration goal; orchestrates grilling (intent capture), exploration (codebase reconnaissance), planning (design strategy), implementation (automated coding), and review (multi-angle validation). Outputs ship-ready code plus decision records in a timestamped session context.
---

# Experiment to Product (E2P)

Transform experiments into production-quality code. Requires experiment source, product target, and a clear goal; orchestrates the full chain: intent capture → reconnaissance → architecture planning → implementation → review.
Defaultly **DO NOT READ** codebase directly at the parent agent. **MUST USE** `/explore` skill to research and explore for getting informations.

## 1. Gather inputs

From the user, collect three pieces of information:

| Input | Purpose | Example |
|---|---|---|
| Experiment location(s) | Where the research/prototype(s) live — one or more | `../my-experiment/` or a GitHub URL |
| Product target | Where code goes in the product repo | `apps/web/` or `services/api/` |
| Integration goal | What to accomplish and success criteria | "Add A/B testing widget to checkout, wire into analytics" |

Multiple experiment locations are allowed when several prototypes feed one integration (e.g. one experiment validated the algorithm, another validated the UI pattern). Treat each independently in steps 3-4, then reconcile them into one plan in step 5 — note in `plan.md` which piece of the design each experiment is responsible for.

Also judge integration size now (single file/module vs. multi-module or new architecture) — steps 3, 4, and 7 scale their dispatch depth to this judgment.

## 2. Set up session context

Create a timestamped directory for this session's artifacts and decision records:

```text
{product_repo_root}/.context/{YYYYMMDD-HHMM}-{goal-slug}/
    ├─ intent.md (grilling output)
    ├─ experiments/ (exploration findings)
    ├─ product/ (reconnaissance findings)
    ├─ plan.md (architecture + implementation strategy)
    ├─ implementation/ (code changes during auto-action)
    └─ review/ (viewpoints analysis of the result)
```

## 3. Explore experiment and product (subagents via `/explore`)

**Check for prior artifacts first.** For each experiment location, look for `handoff/manifest.md` from the `experiment` skill — it's the one path to read, linking to that experiment's `report.md`, `.context/grilling/`, and `.context/explore-context/` (machine-readable evidence) plus `gallery/index.html` (human-only reference — skip reading it, its content is already summarized in `report.md`). Treat the machine-readable links as ground truth; do not re-derive findings they already cover. If a location has no `handoff/manifest.md` (pre-dates this convention, or wasn't built with `/experiment`), fall back to checking for `report.md` directly.

Delegate to `explore` only for what the prior artifacts leave open, on up to two fronts in parallel:

### Experiments branch
Skip entirely, per experiment, if its manifest already covers implementation patterns, data structures, assumptions, and lessons learned. Otherwise research that experiment source for whatever its manifest doesn't answer. With multiple experiment locations, run this check independently per location.

### Product branch
Research the product codebase for existing patterns, dependencies, architecture expectations, and integration points where the experiment(s) fit. (No prior artifact covers this — always run, once, regardless of how many experiment locations there are.)

**Outputs:** `experiments/{exp-slug}/{question-slug}.md` (only for locations needing it; nest under the experiment's own slug when there are multiple) and `product/{question-slug}.md` in the session context.

## 4. Grill for intent (Sonnet-5, foreground)

**Check for prior grilling output first.** For each experiment location, its `handoff/manifest.md` links to that experiment's `.context/grilling/` — pass all of them into this step as prior intent, the real question(s) and why they mattered are already answered. Also check the product repo root for `goal.md` (from `/goal-init`) and pass it in too — it states the project's declared goal, useful for judging whether this integration actually serves it. Scope this grill to what those files don't cover: product-specific unknowns (deployment target, non-negotiables specific to this codebase, integration constraints) and, when there are multiple experiments, how their findings reconcile — do they agree, does one supersede another, do they cover disjoint parts of the goal?

**MUST DISPATCH sub-agent** (Agent tool) with claude-sonnet-5 model run to `/grilling` skill using the exploration findings (and prior grilling output(s), if found) to ground the conversation. Stress-test and capture the goal with facts in hand. Outputs a signed-off intent document pinning down:

- What success looks like (measurable, grounded in what's actually possible)
- Non-negotiables vs. nice-to-haves (informed by codebase reality)
- Known constraints (timeline, dependencies, team, technical debt)
- Risk surface (what could break this, based on existing patterns)

**Output:** `intent.md` in the session context directory.

## 5. Plan implementation (Sonnet-5, foreground)

**MUST DISPATCH sub-agent** (Agent tool) with claude-sonnet-5 model run to `/p4d` skill to plan to implement the intent in the product codebase.

- Where code lands (file structure, module boundaries)
- What refactors or scaffolding are needed
- Dependency and integration points
- Step-by-step change list with risk annotations

**Output:** `plan.md` in the session context directory.

## 6. Implement (Haiku-4.5, foreground)

**MUST DISPATCH sub-agent** (Agent tool) with claude-haiku-4-5 model run to `/work` skill to execute the implementation plan:

- Apply code changes to the product codebase
- Run existing tests to catch regressions
- Create or update tests for new code paths

**Output:** Code changes committed (or staged) in the product repo; logs in `implementation/` in the session context.

## 7. Review (Sonnet-5, foreground)

**Scale to integration size.** For a small, low-risk integration (single file or module, no new architecture), skip the subagent entirely — read the diff yourself against `plan.md`, fix anything minor inline, and move on. Reserve the dispatch below for integrations that touch multiple modules, introduce new architecture, or carry real production risk.

**MUST DISPATCH (large/risky integrations only) sub-agent** (Agent tool) with claude-haiku-4.5 model run to `/viewpoints` skill to build a multi-angle analysis of the result — haiku is enough here, since `/viewpoints` renders views for a human reviewer, it doesn't make the go/no-go call itself:

- Implementation completeness vs. plan
- Code quality and test coverage
- Integration risk (breaking changes, dependency conflicts, performance)
- Production readiness and rollout strategy

**Output:** `review/gallery/` in the session context (large/risky path only; small integrations note the inline check in `plan.md` and proceed).

## 8. Handoff

Session complete when:

- ✓ Intent pinned down and signed off
- ✓ Exploration evidence collected and reviewed
- ✓ Plan written and risk-annotated
- ✓ Implementation committed
- ✓ Review complete (no critical blockers)

Leave the `.context/{timestamp}-{goal}/` directory intact for audit trail and future reference.
