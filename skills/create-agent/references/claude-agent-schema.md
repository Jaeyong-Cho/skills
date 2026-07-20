---
schema-version: 2.1.197
last-verified: 2026-07-10
source: https://code.claude.com/docs/en/sub-agents
---

# Claude Code Subagent Schema

**Location:** `.claude/agents/*.md`, project scope — scanned recursively (subfolders OK). Check into version control; the whole team shares it.

**Frontmatter** — only `name` and `description` are required:

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | lowercase letters + hyphens, unique across the whole `.claude/agents/` tree |
| `description` | Yes | when Claude should delegate here — include "use proactively" to encourage automatic delegation |
| `tools` | No | comma list, allowlist; omit to inherit all tools. Do **not** list `Skill` here to preload skills — use `skills:` instead |
| `disallowedTools` | No | denylist, applied before `tools` is resolved |
| `model` | No | `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit` (default) |
| `permissionMode` | No | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | No | list of skill names — full content of each is injected into the subagent's context at startup |
| `mcpServers` | No | inline or by-name MCP servers scoped to this subagent |
| `hooks` | No | lifecycle hooks scoped to this subagent |
| `memory` | No | `user`, `project`, or `local` — persistent cross-session notes directory |
| `isolation` | No | `worktree` — runs in an isolated git worktree |
| `color` | No | display color: red, blue, green, yellow, purple, orange, pink, cyan |
| `maxTurns`, `effort`, `background`, `initialPrompt` | No | turn cap, effort override, force-background, session-start prompt |

**Body:** the system prompt (Markdown). The subagent receives only this prompt plus CLAUDE.md and a git status snapshot — not the parent conversation's history.

**Name collisions:** if two files anywhere under `.claude/agents/` (including subfolders) declare the same `name`, only one loads — by filesystem read order, not a documented precedence. Check existing names before writing a new one.

**New directory caveat:** a running session doesn't detect a brand-new `.claude/agents/` directory. Restart Claude Code after creating the first agent file in a project that had none.
