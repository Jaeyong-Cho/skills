# System Checklist

Every point a `@skills/grill-me` interview must cover to design an unattended agent system. If the Build target already has an agent team from an earlier run, this is an update pass, not a fresh design: the end-of-cycle review (Review cadence point below) is the round's input — carry every earlier point's answer forward as its `Decision:` line, and only turn a point back into a `❓` question where the review calls it into question. Phrase every question in plain, ELI5 language — no jargon, no unexplained terms.

- Goal — the concrete, single target this system iterates toward (not a general-purpose capability)
- Metric — the deterministic pass/fail signal(s) that tell the Leader a cycle reached the goal vs. needs another cycle, per `deterministic-evaluation.md`
- Harness — for each agent/skill/CLI tool this system builds, classify it per `good-harness.md`'s axes (structural vs. behavioral, objective vs. judgment) and name the resulting local, executable check — so "the Leader/sub-agent does its job" is proven, not just shaped right
- Cycle — what one vertical slice of this loop produces that's independently observable (mirrors the user's normal explore → grill → plan → do → boy-scout → test+commit → merge loop)
- Workflow — phase-by-phase mapping of the cycle onto the existing skills (`@skills/to-context`/`@skills/experiment`, `dev-checklist.md`/`req-checklist.md`, `@skills/to-plan`, `@skills/do-plan`, `@skills/boy-scout`), and any goal-specific deviation from that default order
- Agent team topology — Leader vs. sub-agent(s): who owns which phase, how many sub-agents, and the dispatch/report contract between them
- Target platform(s) — claude / copilot / pi, and this goal's chosen sub-agent mechanic per platform: Claude's Task tool, Copilot's `--agent`, or pi's `pi-interactive-subagents` plugin per `pi-custom-subagent.md` — anything not covered by that reference (Claude, Copilot, or a pi-interactive-subagents field the reference doesn't mention) is found by dispatching a sub-agent to check the real installed tool (`--help`, its docs), never assumed from memory
- Autonomy boundary — which HITL gates in the normal workflow (branch-merge, release, commit confirmation) stay human-gated vs. get delegated to the Leader for this system, and what "stuck, escalate to the human" looks like when the loop can't proceed
- Stop condition — what tells the Leader one cycle is done vs. blocked, same bar as `@skills/do-plan`'s completion criterion. **MUST NOT** block caused minor issue. (cli option error, just quoting error, ... )
- Review cadence — what AI and human discuss once a cycle ends, and that this discussion is the input to re-running `system-grill-me` to update the system
- CLI tooling — any local script/wrapper the Leader needs beyond the existing skills to dispatch sub-agents unattended
- Build target — where locally the agent team, skills, and CLI tools get written — any path, not necessarily inside a repo — confirmed before this skill writes them there
- Human in the loop — when human must review and confirm in the cycle.
