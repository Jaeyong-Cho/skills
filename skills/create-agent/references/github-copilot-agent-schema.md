---
schema-version: 2.0
last-verified: 2026-07-15
source: https://docs.github.com/en/copilot/reference/custom-agents-configuration
---

# GitHub Copilot Custom Agent Schema

**Location:** `.github/agents/*.agent.md` (also `.md`), repository/org/enterprise scope. Check into version control. Lowest-level config (repo > org > enterprise) wins on name conflicts. Works for GitHub.com Copilot cloud agent, Copilot CLI, and supported IDEs (VS Code, JetBrains, Eclipse, Xcode — in public preview for the latter three).

**Frontmatter** — only `description` is required:

| Field | Required | Notes |
|---|---|---|
| `name` | No | display name for the custom agent |
| `description` | Yes | description of the custom agent's purpose and capabilities |
| `target` | No | `vscode` or `github-copilot`; if unset, applies to both |
| `tools` | No | list (or comma-separated string) of tool names/aliases the agent may use. Omit or `["*"]` = all tools. `[]` = no tools. See Tools below. |
| `model` | No | model to use when this agent executes; if unset, inherits the default model. Free-form string — the host environment (Copilot CLI, VS Code, cloud agent) resolves it against its own available models, not a fixed enum. Real-world examples seen in `github/awesome-copilot/agents/*.agent.md`: `'GPT-5'`, `'GPT-4.1'`, `'Claude Sonnet 4.5'`, `'Claude Sonnet 4.6'`, `claude-sonnet-4-5-20250929`, `claude-sonnet-4-6`. Prefer whatever exact string/casing your target host's model picker shows; verify it resolves rather than assuming any of the above always works. |
| `disable-model-invocation` | No | boolean. `true` stops Copilot cloud agent from auto-picking this agent based on task context — it must be manually selected (or explicitly delegated to via the `agent` tool). Equivalent to `infer: false`; if both set, this one wins. Default `false`. |
| `user-invocable` | No | boolean. `false` means a human cannot manually select this agent — usable only programmatically/via delegation. Default `true`. Combine with `disable-model-invocation: true` for a pure subagent-only worker. |
| `infer` | No | **Retired** — use `disable-model-invocation`/`user-invocable` instead. |
| `mcp-servers` | No | object — additional MCP servers/tools for this agent. Not used in VS Code/other IDE custom agents. |
| `metadata` | No | object of string name/value pairs for annotating the agent. Not used in VS Code/other IDE custom agents. |

Body (below frontmatter) is the agent's Markdown system prompt — max 30,000 characters.

> **Not supported for Copilot cloud agent on GitHub.com** (ignored, VS Code/IDE-only): `argument-hint`, `handoffs`.

## Tools

`tools` filters which built-in/MCP tools the agent gets. No `tools` key = all tools enabled; `tools: []` = none; a specific list = only those. Unrecognized tool names are silently ignored (not an error) — so a typo'd/aspirational tool name just disappears rather than failing loudly; always double check the resulting agent actually has the capability you intended.

**Official tool aliases** (case-insensitive; use the primary alias):

| Primary alias | Compatible aliases | Purpose |
|---|---|---|
| `execute` | `shell`, `Bash`, `powershell` | Run a shell command |
| `read` | `Read`, `NotebookRead` | Read file contents |
| `edit` | `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | Edit/write files |
| `search` | `Grep`, `Glob` | Search files/text (covers what earlier drafts of this doc called `findTestFiles`/`githubSearch`/`codebase`) |
| `agent` | `custom-agent`, `Task` | Invoke another custom agent as a subagent/worker |
| `web` | `WebSearch`, `WebFetch` | Fetch URLs / web search |
| `todo` | `TodoWrite` | Structured task list (VS Code only; not supported in cloud agent) |

Out-of-the-box MCP servers usable via namespacing: `github` (read-only tools, `github/*` or `github/<tool>`), `playwright` (`playwright/*`, localhost-only).

There is **no documented `agents:` allowlist property** — delegation is controlled purely by including `agent` in `tools` (which lets the agent invoke other custom agent files by name from its prompt) plus the target agent's own `disable-model-invocation`/`user-invocable` settings. (An earlier version of this note claimed an `agents:` field existed based on third-party examples; the official reference above does not document it — don't rely on it without re-verifying against a specific host's behavior.)

## Example

```yaml
---
name: implementation-planner
description: Creates detailed implementation plans and technical specifications in markdown format
tools: ["read", "search", "edit"]
model: GPT-5
---

You are a technical planning specialist...
```

> **Note:** This schema is manually maintained against `docs.github.com/en/copilot/reference/custom-agents-configuration` (fetched 2026-07-15). Re-verify before relying on it, especially exact `model` string matching and any behavior GitHub hasn't formally documented.
