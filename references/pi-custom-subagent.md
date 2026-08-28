# How to Make a Pi Custom Subagent

A pi subagent is one markdown file: YAML frontmatter, then its system prompt below. `bin/pi-subagents-setup` installs the extension and turns off its builtins (`scout`/`researcher`/`worker`/`reviewer`/`oracle`/`delegate`) — this is how you replace them with your own.

## Where to put it

| Scope | Path | Use for |
|---|---|---|
| Project | `.pi/agents/**/*.md` | agents specific to this repo/goal — the usual choice for a `system-grill-me`-designed team |
| User | `~/.pi/agent/agents/**/*.md` | agents you want in every project |

Nested subdirectories are discovered recursively. Project agents win a name collision over user agents, which win over builtins.

## Minimal example

```yaml
---
name: reviewer
description: Reviews a diff against the task/plan, tests, edge cases, simplicity
tools: read, grep, find, ls
thinking: low
---

You are a review subagent. Check the diff against the stated task and plan...
```

## Calling it

No slash command or registration step needed once the file exists — ask in plain language ("Use reviewer to review this diff") and Pi resolves the name. `subagent({ agent: "reviewer", task: "..." })` is the same call made explicitly.
