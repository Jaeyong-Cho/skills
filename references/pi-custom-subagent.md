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

Only `name` and `description` are required. `tools` is the strict child tool allowlist (omit it to inherit Pi's normal tools) — accepts a comma list or a `- item` block list, same for `defaultReads`/`skills`/`fallbackModels`/`extensions`. Everything else (`model`, `systemPromptMode`, `output`, `timeoutMs`, `acceptance`, per-agent `memory`, ...) is optional and defaults sanely; see the full field table in the installed package's `docs/agents.md` (`~/.pi/agent/git/github.com/nicobailon/pi-subagents/docs/agents.md`) rather than duplicating it here — it changes with the package version.

## Calling it

No slash command or registration step needed once the file exists — ask in plain language ("Use reviewer to review this diff") and Pi resolves the name. `subagent({ agent: "reviewer", task: "..." })` is the same call made explicitly.

## Overriding instead of writing a new file

Don't need a whole new agent, just a tweak to a builtin? Set `subagents.agentOverrides.<name>` in `.pi/settings.json` instead (`model`, `tools`, `disabled`, `systemPromptMode`, ...) — cheaper than a full custom file. `subagent({ action: "eject", agent: "<name>" })` copies a builtin into `.pi/agents/` as an editable starting point when the override surface isn't enough.
