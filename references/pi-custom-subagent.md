# How to Make a Pi Custom Subagent

A pi subagent is one markdown file: YAML frontmatter, then its system prompt below. Sub-agents run via [`pi-interactive-subagents`](https://github.com/hazat/pi-interactive-subagents) — install with `pi install git:github.com/HazAT/pi-interactive-subagents`. Unlike a blocking call, a spawn returns immediately and the sub-agent runs in its own multiplexer pane, so pi must be started inside a supported multiplexer (`cmux`, `tmux`, `zellij`, or WezTerm) for spawning to work at all.

## Where to put it

| Scope | Path | Use for |
|---|---|---|
| Project | `.pi/agents/**/*.md` | agents specific to this repo/goal — the usual choice for a `system-grill-me`-designed team |
| User | `~/.pi/agent/agents/**/*.md` | agents you want in every project |

Discovery priority: project > user (global) > package-bundled (`planner`, `scout`, `worker`, `reviewer`, `visual-tester`). There's no separate "disable builtins" setting — name a project or user agent the same as a bundled one and yours wins the collision outright. `bin/pi-interactive-subagents-setup` does this for all five bundled names at once: it writes an inert, `disable-model-invocation`-hidden stub per name into `.pi/agents/`, idempotently, so only this repo's own custom agents (e.g. from `system-grill-me`) get suggested or spawned.

## Minimal example

```yaml
---
name: reviewer
description: Reviews a diff against the task/plan, tests, edge cases, simplicity
model: anthropic/claude-sonnet-4-6
thinking: minimal
tools: read, bash, grep, find
auto-exit: true
spawning: false
---

You are a review subagent. Check the diff against the stated task and plan...
```

Only `name` and `description` are required. `tools` is a comma list of **native pi tools only** (`read`, `bash`, `edit`, `write`, `grep`, `find`, `ls` — no extension tools); `skills` takes the same comma-list shape. `auto-exit: true` shuts the session down as soon as the agent finishes its turn instead of waiting on an explicit `subagent_done` call — set it on autonomous agents (scout, worker, reviewer) but not interactive ones (planner). `spawning: false` denies the agent every subagent-lifecycle tool (`subagent`, `subagent_interrupt`, `subagents_list`, `subagent_resume`) — set it on anything that should do the work itself, not delegate further (every bundled agent except `planner` sets this). Everything else (`session-mode`, `interactive`, `cwd`, `deny-tools`, `disable-model-invocation`, ...) is optional and defaults sanely; see the extension's own `README.md` for the full field table rather than duplicating it here — it changes with the package version.

## Calling it

Spawning is async: the call returns immediately, the sub-agent runs in its own pane (a live widget above the input tracks its state), and its result steers back into the main session as a notification once it finishes.

```typescript
subagent({ name: "Reviewer", agent: "reviewer", task: "Review this diff against the plan" });
```

`/subagent <agent> <task>` is the same call as a slash command. Call `subagent()` more than once for parallel sub-agents — they run concurrently, each steering its result back independently as it finishes.

## Overriding instead of writing a new file

Don't need a whole new agent, just a tweak to a bundled one (`planner`/`scout`/`worker`/`reviewer`/`visual-tester`)? There's no per-field override setting — write a project or user agent file with the *same `name`* instead; discovery precedence (project > user > bundled) means yours wins outright. Copy the bundled prompt as a starting point if you only need to tweak it, not replace it wholesale. Disabling all five at once instead of tweaking one is `bin/pi-interactive-subagents-setup`'s job (see above) — don't hand-write five stubs.
