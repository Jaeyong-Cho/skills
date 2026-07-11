---
name: create-agent
description: Design and write a project-specific Claude Code subagent — a .claude/agents/*.agent.md file wired to the project's existing skills. Use when invoked as /create-agent.
disable-model-invocation: true
---

# Create Agent

Read `.context/wiki/` for context.

## 1. Focus gate

A subagent earns its own file only when the work has a **focused**, repeatable shape: one job, a distinct tool/model/context scope, delegable without step-by-step supervision. If what's described is a one-shot judgment call, or purely deterministic (a script would do), say so and point at the better fit — a skill (`skill-creator`), or a plain script — instead of building an agent nobody should have. Stop here if it doesn't pass.

## 2. Grill the work pattern

Run a `/grilling` skill to resolve every branch:

1. **Job** — the one task this agent excels at. If it takes "and" to describe, it's two agents.
2. **Delegation trigger** — the `description` Claude uses to decide when to hand off to it. Encourage proactive delegation ("use proactively after X") where that fits.
3. **Tools & model** — which tools it needs (allowlist beats inherit-everything for a focused agent), which model fits the job's cost/quality tradeoff.
4. **Isolation** — does it need its own git worktree, persistent memory across sessions, or plain shared-checkout access?
5. **Self-update** — does this agent's operating knowledge (project conventions, schemas, module layout) go stale as the project changes? If yes, name what it must track and how often it's likely to drift.
6. **Completion criterion** — what is the done state? When does the agent stop and declare success? (Equivalent to `exit 0` in a script: the observable condition it checks before reporting done.)

## 3. Survey project skills

List skill frontmatter (`name` + `description`) from every `SKILL.md` under the project's `.claude/skills/` (if present) and the user's `~/.claude/skills/`. Ask which of these the new agent should be wired to — the skills it's expected to actually use while doing its job, not every skill that exists.

## 4. Check for name collisions

```bash
grep -rl "^name: {name}$" .claude/agents/ 2>/dev/null
```
Any match → pick a different name or confirm the overwrite with the user.

## 5. Write the file

Read `references/claude-agent-schema.md`. Follow it exactly — required fields only where required, optional fields only where the grill surfaced a need for them. If you find the schema no longer matches what Claude Code actually accepts, tell the user and ask them to update the reference file — `create-agent` doesn't refresh it on its own.

Wire the surveyed skills via the `skills:` frontmatter field (not `tools: Skill`) so their full content preloads at startup.

**Prompt body — structure it like an automation script in natural language.** An agent is a CI/CD or debugging script where the non-deterministic parts are expressed in prose instead of code. Structure the body accordingly: setup → sequence → done check. Wherever a step is deterministic (a check, extraction, or fixed operation with one right way to run it), write the actual command(s) in a code block. Reserve prose for the parts that genuinely need judgment. The body must end with an explicit **completion criterion** (from grill item 6) — the observable condition the agent checks before reporting done. A prompt body without a done condition is a script without `exit`.

If grill item 5 flagged self-update: set `memory: project` so the agent gets a persistent `.claude/agent-memory/{name}/` notes directory, checked into version control. In the prompt body, instruct it explicitly: consult memory before starting work, and after finishing, write down what changed in the project since last time (new conventions, moved files, updated schemas).

`mkdir -p .claude/agents` if needed. Write `.claude/agents/{name}.agent.md`.

## 6. Validate deterministically

Don't eyeball it — run this sequence and require the stated result at each line:

```bash
awk '/^---$/{c++} END{print c}' .claude/agents/{name}.agent.md          # must print 2
grep -c "^name:" .claude/agents/{name}.agent.md                          # must print 1
grep -c "^description:" .claude/agents/{name}.agent.md                   # must print 1
grep -E "^(tools|model|permissionMode|isolation|memory|skills):" .claude/agents/{name}.agent.md   # extract every optional field present
```
For each field the last command prints, look it up in `references/claude-agent-schema.md` and confirm the value used is in that field's valid-values column. Any failed line above → fix the file and re-run the whole sequence before reporting done.

Completion criterion: the file exists at `.claude/agents/{name}.agent.md`, passes the step 6 checks, carries no name collision, any project skills chosen in step 3 are wired in via `skills:`, the prompt body includes an explicit completion criterion, and — if grill item 5 flagged self-update — the `memory` field and consult/update instructions are present.

Tell the user the path written. If this was the first agent file in a previously-empty `.claude/agents/`, remind them to restart Claude Code so the directory is picked up.

## 7. GitHub Copilot format (optional)

Ask the user if they also want a GitHub Copilot agent file. Skip this step if they don't.

If yes: read `references/github-copilot-agent-schema.md`. Write the same job and prompt body, translated to that schema's frontmatter fields and tool names.

```bash
mkdir -p .github/agents
```

Write `.github/agents/{name}.agent.md`. Validate:

```bash
awk '/^---$/{c++} END{print c}' .github/agents/{name}.agent.md   # must print 2
grep -c "^name:" .github/agents/{name}.agent.md                   # must print 1
grep -c "^description:" .github/agents/{name}.agent.md            # must print 1
```

Tell the user the path written.
