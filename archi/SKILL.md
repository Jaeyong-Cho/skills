---
name: archi
description: Architecture skill. Grills to resolve architecture, design, observability, test-loop design, and verification criteria against archi.md's layers and dependency rule, then writes an ADR. Use when invoked as /archi.
disable-model-invocation: true
---

# Archi

Read `.context/req/rdr/` for the draft RDR to design against — a draft is named `{timestamp}-{slug}.md` (a merged one has `.merged.md` and is no longer live). If `.context/req/{slug}.md` also exists, read it too for prior committed context.

Check `.context/adr/{slug}.md` — if a committed architecture doc covers the same topic, read it for context. Check `.context/adr/` for a draft ADR — named `{timestamp}-{slug}.md` (a merged one has been renamed to `{timestamp}-{slug}.merged.md`). If a draft (no `.merged.md` suffix) for the same slug already exists, it's unfinished work from a run that never reached `/merge-archi`; read it and revise that record in place rather than starting a new one. Otherwise this round produces a fresh ADR.

Use this for new designs or to redesign after a fix reveals new architecture needs.
Read `../references/archi.md`, `../references/meta-pattern.md`, `../references/deep-modules.md`, `../references/test-loop.md`.

Check `.claude/agents/` and `.github/agents/` for existing project subagents. If one's description matches part of this design (e.g. a domain expert for architecture research, or a specialized reviewer for the design), delegate that part to it rather than reasoning through it inline yourself.

Run a `/grilling` skill to resolve every branch of the design:

1. **Architecture** — how to structure the implementation? Apply archi.md's layers (Objects/Logics/Usecase/External) and dependency rule, meta-pattern (Abstractness/Subdomain/Sharding axes), and deep-module principles (hide complexity, widen interfaces). Every class lands in exactly one layer; a dependency pointing outward is a design error — stop and redesign.
2. **Design** — what are the key modules, contracts, and data flows? Place each inside the layer archi.md assigns it; check against archi.md's Design Smells table.
3. **Observability** — which debugging information is needed for handling issues? How to verify the logic is working? Which information is needed to judge the design is working? How to detect known-unknown and ambiguous concern points? (e.g. "use assert to detect concern point" or "write debugging data to the json in data directory") Include runtime checkpoints: what internal state, logs, or intermediate data to observe mid-execution, not just the final output.
4. **Test-loop design** — E2E only. Check if an existing test-loop scenario covers the needed behaviors; extend it rather than creating a new scenario. Apply `test-loop.md`: what does `run` reset and initialize before executing? what does `run` write (results, metadata: version, input data, config)? what does `verify` check per scenario? For each scenario, classify the observation method: binary pass/fail | numeric metric range (with expected range) | qualitative rubric (with explicit criteria). Reference the requirements spec's User Scenario and Acceptance Criteria for each scenario's expected outcome.
5. **Verification criteria** — how do we know the result is good? Make it checkable. How does a human know if the changes are working at the real working system with real data? What to see for verification? How to observe it? How to judge the design is working well? (e.g. "the user can do X in Y seconds", "see the data and check all of them has property P", "the system can handle N requests per second", "If log A -> log B and data X -> Y -> Z is shown, then it is working well" or "All of the unmatched is zero, then it is working well"). Map each criterion to the requirements spec's Acceptance Criteria categories (Normal / Exception / Boundary). Make it checkable.

Grill until every branch is resolved and the user confirms. Completion criterion: architecture, design, observability, test-loop, and verification are each stated concretely with no ambiguous branch, layer placement is clean end to end, user confirmed.

Derive a kebab-case slug from the topic. If revising an existing draft ADR, reuse its slug and timestamp — edit that file in place. Otherwise get a fresh timestamp: run `date +%Y%m%d-%H%M%S`.

Fill in `../template/adr.md` with the resolved context, decision (before/after), observability, test-loop design, and verification criteria, and write it to `.context/adr/{timestamp}-{slug}.md`.

`mkdir -p .context/adr` if needed. Tell the user the file path, and that it's a draft ADR that `/merge-archi` will fold into `.context/adr/{slug}.md` once implementation completes. Next step: `/planning`.

**DO NOT START IMPLEMENT**
