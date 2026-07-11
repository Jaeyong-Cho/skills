---
schema-version: 1.0
last-verified: 2026-07-11
source: https://docs.github.com/en/copilot/customizing-copilot/building-a-copilot-coding-agent
---

# GitHub Copilot Coding Agent Schema

**Location:** `.github/agents/*.md`, repository scope. Check into version control.

**Frontmatter** — only `name` and `description` are required:

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | display name for the agent |
| `description` | Yes | one-line summary of what the agent does |
| `tools` | No | list of tools the agent may use (omit to allow all) |

**Available tools:**

| Tool | What it does |
|---|---|
| `codebase` | search and read files in the repository |
| `terminal` | run terminal/shell commands |
| `web` | web search and browsing |
| `githubRepo` | GitHub repository operations (issues, PRs, code) |
| `findTestFiles` | locate test files in the repo |
| `githubSearch` | search across GitHub |

**Body:** the agent's system prompt (Markdown). Describes the agent's job, constraints, and behavior.

**Differences from Claude Code agents:**
- No `model`, `permissionMode`, `memory`, `isolation`, `skills`, or `hooks` fields.
- Tool names differ from Claude Code tool names — do not reuse the Claude `tools:` list verbatim.
- Runs in GitHub Copilot's execution context, not Claude Code's.

> **Note:** This schema is manually maintained. Verify against current GitHub docs before relying on it.
