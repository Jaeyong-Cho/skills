---
name: create-agent
description: Design and write a project-specific subagent — Claude Code (.claude/agents/{name}.md) or GitHub Copilot (.github/agents/{name}.agent.md), or both. Use when invoked as /create-agent.
disable-model-invocation: true
---

# Create Agent

Read `.context/wiki/` for context.

## 1. Focus gate

A subagent earns its own file only when the work has a **focused**, repeatable shape: one job, a distinct tool/model/context scope, delegable without step-by-step supervision. If what's described is a one-shot judgment call, or purely deterministic (a script would do), say so and point at the better fit — a skill (`skill-creator`), or a plain script — instead of building an agent nobody should have. Stop here if it doesn't pass.

## 2. Format selection

Ask the user which format(s) to produce:

- **Claude Code** — `.claude/agents/{name}.md`
- **GitHub Copilot** — `.github/agents/{name}.agent.md`
- **Both**

The answer drives which steps below apply. Note it — referred to as the **target format** throughout.

## 3. Grill the work pattern

Run a `/grilling` skill to resolve every branch:

1. **Job** — the one task this agent excels at. If it takes "and" to describe, it's two agents.
2. **Delegation trigger** — the `description` Claude uses to decide when to hand off to it. Encourage proactive delegation ("use proactively after X") where that fits.
3. **Tools & model** — which tools it needs (allowlist beats inherit-everything for a focused agent), which model fits the job's cost/quality tradeoff.
4. **Isolation** — does it need its own git worktree, persistent memory across sessions, or plain shared-checkout access?
5. **Self-update** — does this agent's operating knowledge (project conventions, schemas, module layout) go stale as the project changes? If yes, name what it must track and how often it's likely to drift.
6. **Completion criterion** — what is the done state? When does the agent stop and declare success? (Equivalent to `exit 0` in a script: the observable condition it checks before reporting done.)

## 4. Survey project skills _(Claude Code only)_

Skip this step if target format is GitHub Copilot only.

List skill frontmatter (`name` + `description`) from every `SKILL.md` under the project's `.claude/skills/` (if present) and the user's `~/.claude/skills/`. Ask which of these the new agent should be wired to — the skills it's expected to actually use while doing its job, not every skill that exists.

## 5. Check for name collisions

```bash
grep -rl "^name: {name}$" .claude/agents/ 2>/dev/null   # if Claude Code target
grep -rl "^name: {name}$" .github/agents/ 2>/dev/null   # if GitHub Copilot target
```

Any match → pick a different name or confirm the overwrite with the user.

## 6. Write the file(s)

**Prompt body — structure it like an automation script in natural language.** An agent is a CI/CD or debugging script where the non-deterministic parts are expressed in prose instead of code. Structure the body accordingly: setup → sequence → done check. Wherever a step is deterministic (a check, extraction, or fixed operation with one right way to run it), write the actual command(s) in a code block. Reserve prose for the parts that genuinely need judgment. The body must end with an explicit **completion criterion** (from grill item 6) — the observable condition the agent checks before reporting done. A prompt body without a done condition is a script without `exit`.

Write the file(s) for the selected target format:

### Claude Code

Read `references/claude-agent-schema.md`. Follow it exactly — required fields only where required, optional fields only where the grill surfaced a need for them. If the schema no longer matches what Claude Code accepts, tell the user and ask them to update the reference file.

Wire the surveyed skills via the `skills:` frontmatter field (not `tools: Skill`) so their full content preloads at startup.

If grill item 5 flagged self-update: set `memory: project`. In the prompt body, instruct it: consult memory before starting work, and after finishing write down what changed in the project since last time.

```bash
mkdir -p .claude/agents
```

Write `.claude/agents/{name}.md`.

### GitHub Copilot

Read `references/github-copilot-agent-schema.md`. Translate the same job and prompt body to that schema's frontmatter fields and tool names.

```bash
mkdir -p .github/agents
```

Write `.github/agents/{name}.agent.md`.

## 7. Validate deterministically

Run for each file written:

**Claude Code:**
```bash
awk '/^---$/{c++} END{print c}' .claude/agents/{name}.md          # must print 2
grep -c "^name:" .claude/agents/{name}.md                          # must print 1
grep -c "^description:" .claude/agents/{name}.md                   # must print 1
grep -E "^(tools|model|permissionMode|isolation|memory|skills):" .claude/agents/{name}.md
```
For each optional field printed, confirm its value is in the valid-values column of `references/claude-agent-schema.md`.

**GitHub Copilot:**
```bash
awk '/^---$/{c++} END{print c}' .github/agents/{name}.agent.md          # must print 2
grep -c "^name:" .github/agents/{name}.agent.md                          # must print 1
grep -c "^description:" .github/agents/{name}.agent.md                   # must print 1
```

Any failed check → fix the file and re-run the full sequence before reporting done.

Completion criterion: every selected file exists and passes its validation sequence; no name collision; Claude Code file has `skills:` wired and a completion criterion in the prompt body; if grill item 5 flagged self-update, `memory` field and consult/update instructions are present.

Tell the user each path written. If this was the first agent file in a previously-empty `.claude/agents/`, remind them to restart Claude Code so the directory is picked up.
