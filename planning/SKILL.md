---
name: planning
description: Planning skill. Grills to resolve architecture, test-loop design, evaluation criteria, and action sequence, then writes an ADR. Use when invoked as /planning.
disable-model-invocation: true
---

# Planning

Read `.context/req/rdr/` for the draft RDR to plan against — a draft is named `{timestamp}-{slug}.md` (a merged one has `.merged.md` and is no longer live). This is the spec `/req` just produced. If `.context/req/{slug}.md` also exists, read it too for prior committed context. Also read `.context/adr/` — if an existing ADR covers the same topic, read it and revise it rather than creating a new one.

Use this for new plans or to replan after a fix reveals new design needs.
Read `../references/meta-pattern.md`, `../references/deep-modules.md`, `../references/test-loop.md`.

Check `.claude/agents/` and `.github/agents/` for existing project subagents. If one's description matches part of this plan (e.g. a domain expert for architecture research, or a specialized reviewer for the design), delegate that part to it rather than reasoning through it inline yourself.

Run a `/grilling` skill to resolve every branch of the plan:

1. **Architecture** — how to structure the implementation? Apply meta-pattern (Abstractness/Subdomain/Sharding axes) and deep-module principles (hide complexity, widen interfaces).
2. **Design** — what are the key modules, contracts, and data flows?
3. **Observability** — which debugging information is needed for handling issues? How to verify the logic is working? Which information is needed to judge the plan is working? How to detect known-unknown and ambiguous concern points? (e.g. "use assert to detect concern point" or "write debugging data to the json in data directory") Include runtime checkpoints: what internal state, logs, or intermediate data to observe mid-execution, not just the final output.
4. **Test-loop design** — E2E only. Check if an existing test-loop scenario covers the needed behaviors; extend it rather than creating a new scenario. Apply `test-loop.md`: what does `run` reset and initialize before executing? what does `run` write (results, metadata: version, input data, config)? what does `verify` check per scenario? For each scenario, classify the observation method: binary pass/fail | numeric metric range (with expected range) | qualitative rubric (with explicit criteria). Reference the requirements spec's User Scenario and Acceptance Criteria for each scenario's expected outcome.
5. **Evaluation criteria** — how do we know the result is good? Make it checkable. How to a human know if the changes are working at the real working system with real data? What to see for verification? How to observe it? How to judge the plan is working well? (e.g. "the user can do X in Y seconds", "see the data and check all of them has property P", "the system can handle N requests per second", "If log A -> log B and data X -> Y -> Z is shown, then it is working well" or "All of the unmatched is zero, then it is working well"). Map each criterion to the requirements spec's Acceptance Criteria categories (Normal / Exception / Boundary). Make it checkable.
6. **Action sequence** — ordered atomic steps to implement. Each step: one concern, one logical unit, describable without "and". The template's fixed Closeout checklist (refactor, test) always follows as the last steps — no need to grill those.

Grill until every branch is resolved and the user confirms. Completion criterion: action sequence is fully ordered with no ambiguous steps, user confirmed.

Get the timestamp: run `date +%Y%m%d-%H%M%S`. Derive a kebab-case slug from the topic.

Fill in `../template/adr.md` with the resolved decision, design, action sequence, and verification, and write it to `.context/adr/{timestamp}-{slug}.md`. Leave the fixed Closeout checklist as-is.

`mkdir -p .context/adr` if needed. Tell the user the file path. Next step: `/auto-action`.

**DO NOT START IMPLEMENT**
