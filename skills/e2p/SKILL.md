---
name: e2p
description: Bridge experiments to production — transform ad-hoc research into integrated product code. Takes an experiment location, a product target, and an integration goal; orchestrates grilling (intent capture), exploration (codebase reconnaissance), planning (design strategy), implementation (automated coding), and review (multi-angle validation). Outputs ship-ready code plus decision records in a timestamped session context.
---

# Experiment to Product (E2P)

Transform experiments into production-quality code. Requires experiment source, product target, and a clear goal; orchestrates the full chain: intent capture → reconnaissance → architecture planning → implementation → review.

## 1. Gather inputs

From the user, collect three pieces of information:

| Input | Purpose | Example |
|---|---|---|
| Experiment location | Where the research/prototype lives | `../my-experiment/` or a GitHub URL |
| Product target | Where code goes in the product repo | `apps/web/` or `services/api/` |
| Integration goal | What to accomplish and success criteria | "Add A/B testing widget to checkout, wire into analytics" |

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

**Check for prior artifacts first.** If the experiment location contains `report.md` and/or a `gallery/` from the `experiment` skill, treat those as ground truth — do not re-derive findings they already cover. Read them directly instead of dispatching a subagent for anything they already answer.

Delegate to `explore` only for what the prior artifacts leave open, on up to two fronts in parallel:

### Experiments branch
Skip entirely if `report.md` already covers implementation patterns, data structures, assumptions, and lessons learned. Otherwise research the experiment source for whatever `report.md` doesn't answer.

### Product branch
Research the product codebase for existing patterns, dependencies, architecture expectations, and integration points where the experiment fits. (No prior artifact covers this — always run.)

**Outputs:** `experiments/{question-slug}.md` (only if dispatched) and `product/{question-slug}.md` in the session context.

## 4. Grill for intent (Sonnet-5, foreground)

**Check for a prior grilling output first.** If the experiment location has `.context/grilling/` from the `experiment` skill, pass that file into this step as prior intent — the real question and why it mattered are already answered. Scope this grill to what that file doesn't cover: product-specific unknowns (deployment target, non-negotiables specific to this codebase, integration constraints).

**MUST DISPATCH** sub-agent (Agent tool) with claude-sonnet-5 model `/grilling` using the exploration findings (and prior grilling output, if found) to ground the conversation. Stress-test and capture the goal with facts in hand. Outputs a signed-off intent document pinning down:

- What success looks like (measurable, grounded in what's actually possible)
- Non-negotiables vs. nice-to-haves (informed by codebase reality)
- Known constraints (timeline, dependencies, team, technical debt)
- Risk surface (what could break this, based on existing patterns)

**Output:** `intent.md` in the session context directory.

## 5. Plan implementation (Sonnet-5, foreground)

**MUST DISPATCH** sub-agent (Agent tool) with claude-sonnet-5 model `/p4d` to plan to implement the intent in the product codebase.

- Where code lands (file structure, module boundaries)
- What refactors or scaffolding are needed
- Dependency and integration points
- Step-by-step change list with risk annotations

**Output:** `plan.md` in the session context directory.

## 6. Implement (Haiku-4.5, foreground)

**MUST DISPATCH** sub-agent (Agent tool) with claude-haiku-4-5 model `/work` to execute the implementation plan:

- Apply code changes to the product codebase
- Run existing tests to catch regressions
- Create or update tests for new code paths

**Output:** Code changes committed (or staged) in the product repo; logs in `implementation/` in the session context.

## 7. Review (Sonnet-5, foreground)

**Scale to integration size.** For a small, low-risk integration (single file or module, no new architecture), skip the subagent entirely — read the diff yourself against `plan.md`, fix anything minor inline, and move on. Reserve the dispatch below for integrations that touch multiple modules, introduce new architecture, or carry real production risk.

**MUST DISPATCH** (large/risky integrations only) sub-agent (Agent tool) with claude-sonnet-5 model `/viewpoints` to build a multi-angle analysis of the result:

- Implementation completeness vs. plan
- Code quality and test coverage
- Integration risk (breaking changes, dependency conflicts, performance)
- Production readiness and rollout strategy

**Output:** `review/gallary/` in the session context (large/risky path only; small integrations note the inline check in `plan.md` and proceed).

## 8. Handoff

Session complete when:

- ✓ Intent pinned down and signed off
- ✓ Exploration evidence collected and reviewed
- ✓ Plan written and risk-annotated
- ✓ Implementation committed
- ✓ Review complete (no critical blockers)

Leave the `.context/{timestamp}-{goal}/` directory intact for audit trail and future reference.
