---
name: system-grill-me
description: Run a @skills/grill-me interview to design an unattended agent system — Leader + sub-agent(s), skills, CLI tools — that iterates a specific goal cycle by cycle without human-in-the-loop mid-cycle. Covers goal, success metric, cycle/workflow shape, team topology, target platform (claude/copilot/pi) mechanics, autonomy boundary, stop condition, review cadence.
disable-model-invocation: true
---

# System Grill Me

**MUST RUN** `@skills/grill-me` covering every point below to design the system. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms:

- Goal — the concrete, single target this system iterates toward (not a general-purpose capability)
- Metric — the deterministic pass/fail signal(s) that tell the Leader a cycle reached the goal vs. needs another cycle, per `../references/deterministic-evaluation.md`
- Harness — for each agent/skill/CLI tool this system builds, classify it per `../references/good-harness.md`'s axes (structural vs. behavioral, objective vs. judgment) and name the resulting local, executable check — so "the Leader/sub-agent does its job" is proven, not just shaped right
- Cycle — what one vertical slice of this loop produces that's independently observable (mirrors the user's normal explore → grill → plan → do → boy-scout → test+commit → merge loop)
- Workflow — phase-by-phase mapping of the cycle onto the existing skills (`@skills/to-context`/`@skills/experiment`, `@skills/dev-grill-me`/`@skills/story-grill-me`, `@skills/to-plan`, `@skills/do-plan`, `@skills/boy-scout`), and any goal-specific deviation from that default order
- Agent team topology — Leader vs. sub-agent(s): who owns which phase, how many sub-agents, and the dispatch/report contract between them
- Target platform(s) — claude / copilot / pi, and this goal's chosen sub-agent mechanic per platform: Claude's Task tool, Copilot's `--agent`, or pi's `pi-subagents` plugin per `../references/pi-custom-subagent.md` — anything not covered by that reference (Claude, Copilot, or a pi-subagents field the reference doesn't mention) is found by dispatching a sub-agent to check the real installed tool (`--help`, its docs), never assumed from memory
- Autonomy boundary — which HITL gates in the normal workflow (branch-merge, release, commit confirmation) stay human-gated vs. get delegated to the Leader for this system, and what "stuck, escalate to the human" looks like when the loop can't proceed
- Stop condition — what tells the Leader one cycle is done vs. blocked, same bar as `@skills/do-plan`'s completion criterion
- Review cadence — what AI and human discuss once a cycle ends, and that this discussion is the input to re-running `system-grill-me` to update the system
- CLI tooling — any local script/wrapper the Leader needs beyond the existing skills to dispatch sub-agents unattended
- Build target — where locally the agent team, skills, and CLI tools get written (repo path), confirmed before `@skills/to-plan` drafts action items
- Dogfood test — run one real cycle end-to-end before trusting the system unattended

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in the checklist above: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one above appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a `--help`/command output, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST** surface assertions aggressively wherever there is any uncertainty — for each, name the agent/skill/file it belongs to and whether it's a precondition, invariant, or postcondition, so `@skills/to-plan` can carry it into the plan's Assertions section as a real runtime check the Leader makes before proceeding, not a comment.
**MUST NOT** start building the agent team, skills, or CLI tools before the frontier is empty.

Once complete, next step is `@skills/to-plan` by human to turn the recorded answers into a plan whose action items write the Leader/sub-agent definitions, skills, CLI tools, and the Harness point's checks; `@skills/do-plan` then builds and dogfoods them. After the first unattended cycle runs, its end-of-cycle review (per the Review cadence point above) is the input to the next `system-grill-me` pass that updates the system.
