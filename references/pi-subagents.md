# Pi Subagents for the Problem-Solving Workflow

[`pi-subagents`](https://github.com/nicobailon/pi-subagents) is the sub-agent
extension backing this project's intent-to-cycle chain
(`@skills/define-problem`, `@skills/find-solutions`, `@skills/evaluate-solution`)
— a different, more capable package than `pi-interactive-subagents` (see
`pi-custom-subagent.md`), used specifically for these three skills' "dispatch
a sub-agent" steps. Install: `pi install npm:pi-subagents`.

## Setup

Run `bin/pi-subagents-setup` inside a target repo (same per-project pattern
as `bin/pi-interactive-subagents-setup`) — it installs `pi-subagents` and
`pi-web-access` (the `researcher` builtin's web tools need it), writes this
project's two custom agents into `.pi/agents/`, and disables five of the
package's six builtins via `subagents.agentOverrides` in `.pi/settings.json`.
Idempotent — safe to re-run.

## This project's agents

| Agent | Kind | Use it for |
|---|---|---|
| `fact-finder` | custom | Read-only local investigation — Current state, Gap, and reuse-check steps in `define-problem`/`find-solutions`/`evaluate-solution`. Never edits, never runs an experiment itself. |
| `experimenter` | custom | Runs `@skills/experiment` for real, for any claim `fact-finder` can't settle by reading alone. |
| `researcher` | builtin, kept enabled | Web/docs research with sources — `find-solutions` dispatches it for reference examples (a famous open-source architecture, structure, or framework that solves a comparable Gap), cited, not invented. |

`scout`, `worker`, `reviewer`, `oracle`, and `delegate` are disabled
(`agentOverrides.<name>.disabled: true`) — this workflow's own three agents
above cover everything those would otherwise be reached for.

## Never dispatch bare

Every "dispatch a sub-agent" instruction in `define-problem`/`find-solutions`/
`evaluate-solution` means a named call —
`subagent({ agent: "fact-finder", task: "..." })`,
`subagent({ agent: "experimenter", task: "..." })`, or
`subagent({ agent: "researcher", task: "..." })` — never a bare
`subagent({ task: "..." })` that leaves Pi to pick an agent on its own.
Naming the agent is what keeps fact-finding, experiment-running, and web
research on this project's own reviewed prompts instead of whatever a
default agent would improvise.
