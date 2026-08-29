---
name: system-grill-me
description: Run a @skills/grill-me interview to design an unattended agent system — Leader + sub-agent(s), skills, CLI tools — that iterates a specific goal cycle by cycle without human-in-the-loop mid-cycle, or re-run it after a cycle ends to update that same system from the cycle's review. Covers goal, success metric, cycle/workflow shape, team topology, target platform (claude/copilot/pi) mechanics, autonomy boundary, stop condition, review cadence.
disable-model-invocation: true
---

# System Grill Me

**MUST RUN** `@skills/grill-me` covering every point below to design the system. If the Build target already has an agent team from an earlier run, this is an update pass, not a fresh design: the end-of-cycle review (Review cadence point below) is the round's input — carry every earlier point's answer forward as its `Decision:` line, and only turn a point back into a `❓` question where the review calls it into question. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms:

- Goal — the concrete, single target this system iterates toward (not a general-purpose capability)
- Metric — the deterministic pass/fail signal(s) that tell the Leader a cycle reached the goal vs. needs another cycle, per `../references/deterministic-evaluation.md`
- Harness — for each agent/skill/CLI tool this system builds, classify it per `../references/good-harness.md`'s axes (structural vs. behavioral, objective vs. judgment) and name the resulting local, executable check — so "the Leader/sub-agent does its job" is proven, not just shaped right
- Cycle — what one vertical slice of this loop produces that's independently observable (mirrors the user's normal explore → grill → plan → do → boy-scout → test+commit → merge loop)
- Workflow — phase-by-phase mapping of the cycle onto the existing skills (`@skills/to-context`/`@skills/experiment`, `@skills/dev-grill-me`/`@skills/req-grill-me`, `@skills/to-plan`, `@skills/do-plan`, `@skills/boy-scout`), and any goal-specific deviation from that default order
- Agent team topology — Leader vs. sub-agent(s): who owns which phase, how many sub-agents, and the dispatch/report contract between them
- Target platform(s) — claude / copilot / pi, and this goal's chosen sub-agent mechanic per platform: Claude's Task tool, Copilot's `--agent`, or pi's `pi-interactive-subagents` plugin per `../references/pi-custom-subagent.md` — anything not covered by that reference (Claude, Copilot, or a pi-interactive-subagents field the reference doesn't mention) is found by dispatching a sub-agent to check the real installed tool (`--help`, its docs), never assumed from memory
- Autonomy boundary — which HITL gates in the normal workflow (branch-merge, release, commit confirmation) stay human-gated vs. get delegated to the Leader for this system, and what "stuck, escalate to the human" looks like when the loop can't proceed
- Stop condition — what tells the Leader one cycle is done vs. blocked, same bar as `@skills/do-plan`'s completion criterion. **MUST NOT** block caused minor issue. (cli option error, just quoting error, ... )
- Review cadence — what AI and human discuss once a cycle ends, and that this discussion is the input to re-running `system-grill-me` to update the system
- CLI tooling — any local script/wrapper the Leader needs beyond the existing skills to dispatch sub-agents unattended
- Build target — where locally the agent team, skills, and CLI tools get written — any path, not necessarily inside a repo — confirmed before this skill writes them there
- Human in the loop — when human must review and confirm in the cycle.

## Subagent vs. skill

Read `../references/subagents-vs-skills.md` before the Agent team topology point — it decides whether a phase becomes a sub-agent or stays a skill the Leader calls directly.

## Impact Level and Uncertainty
Read `../references/grill-impact.md` first — ask its Mode question before round 1, then its Impact Level, Uncertainty, and Action rules govern which questions get asked outright versus skipped-with-an-assertion-mark for the rest of this session.

For every point in the checklist above: classify impact level and uncertainty first. Low impact level → **do not ask** a `❓` question — state the auto-decided answer as a plain line (`Decision:` + impact/uncertainty tag, assertion mark if uncertainty is High) and move on. Only High impact points become `❓` questions in the round. **MUST NOT** silently drop any checklist point — every one above appears in the transcript, either as a `❓` question or a `Decision:` line; "skip" means skip the question, never skip discussing it.

**MUST show evidence, not just a conclusion.** Every `Decision:` line and every `➡️` recommended answer cites what it's based on — a file:line, a `--help`/command output, or an existing pattern found in the repo — found by a sub-agent per `@skills/grill-me`'s "Finding facts is your job" rule, not asserted from memory. No evidence found → say so and mark uncertainty High instead of guessing.

**MUST NOT** assert the agent team itself too much. Make runnable. The harness and assert is for a the environment not agent team system.
**MUST NOT** start building the agent team, skills, or CLI tools before the frontier is empty.

Once the frontier is empty, show the human a summary of the agent team the recorded answers add up to (goal, cycle, topology, target platform, autonomy boundary, build target — one line each), then **MUST ASK** confirmation to build it, per `../references/question-format.md`'s ❓/➡️ format (`➡️ Yes, build it` as the recommended answer). Once confirmed, build it for real — the goal of this skill is the agent team itself: write the Leader/sub-agent definitions, the skills and CLI tools named by the Workflow and CLI tooling points, and the Harness point's checks, with every Assertions-worthy uncertainty point wired in as a real runtime assert, at the Build target path. Create these fresh if the Build target is empty, or edit the existing files in place if this is a review-cadence update pass. After the first unattended cycle runs, its end-of-cycle review (per the Review cadence point above) is the input to the next `system-grill-me` pass that updates that same agent team.
