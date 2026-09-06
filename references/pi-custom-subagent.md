# How to Make a Pi Custom Subagent

A pi subagent is one markdown file: YAML frontmatter, then its system prompt below. Sub-agents run via [`pi-subagents`](https://github.com/nicobailon/pi-subagents) — install with `pi install npm:pi-subagents`. A spawn may run in the foreground or background; pi-subagents manages the child session and returns its result to the parent.

## Where to put it

| Scope | Path | Use for |
|---|---|---|
| Project | `.pi/agents/**/*.md` | agents specific to this repo/goal — the usual choice for a `system-grill-me`-designed team |
| User | `~/.pi/agent/agents/**/*.md` | agents you want in every project |

Discovery priority: project > user (global) > package-bundled (`scout`, `researcher`, `worker`, `reviewer`, `oracle`, `delegate`). Name a project or user agent the same as a bundled one to override it. To disable all bundled agents for a project, set `{"subagents":{"disableBuiltins":true}}` in `.pi/settings.json`, so only this repo's own custom agents are suggested or spawned.

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

Only `name` and `description` are required. `tools` is a comma list of **native pi tools only** (`read`, `bash`, `edit`, `write`, `grep`, `find`, `ls` — no extension tools); `skills` takes the same comma-list shape. `auto-exit: true` shuts the session down as soon as the agent finishes its turn instead of waiting on an explicit completion call — set it on autonomous agents, but not interactive ones. `spawning: false` denies the agent every subagent-lifecycle tool — set it on anything that should do the work itself, not delegate further. Everything else (`session-mode`, `interactive`, `cwd`, `deny-tools`, `disable-model-invocation`, ...) is optional and defaults sanely; see the extension's own `README.md` for the full field table rather than duplicating it here — it changes with the package version.

## Calling it

Spawning may run in the foreground or background; pi-subagents manages the child session and returns its result to the main session when it finishes.

```typescript
subagent({ name: "Reviewer", agent: "reviewer", task: "Review this diff against the plan" });
```

`/subagent <agent> <task>` is the same call as a slash command. Call `subagent()` more than once for parallel sub-agents — they run concurrently, each steering its result back independently as it finishes.

## Overriding instead of writing a new file

Don't need a whole new agent, just a tweak to a bundled one (`scout`/`researcher`/`worker`/`reviewer`/`oracle`/`delegate`)?  There's no per-field override setting — write a project or user agent file with the *same `name`* instead; discovery precedence (project > user > bundled) means yours wins outright. Copy the bundled prompt as a starting point if you only need to tweak it, not replace it wholesale. Disable all bundled agents with `{"subagents":{"disableBuiltins":true}}` in the project's `.pi/settings.json`; don't hand-write stub agents.
