---
name: create-agent
description: Design and write a project-specific Claude Code subagent — a .claude/agents/*.md file wired to the project's existing skills. Use when invoked as /create-agent.
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

**Prompt body — deterministic parts get literal command sequences, not prose.** Wherever the job (from grill item 1) involves a check, extraction, or fixed operation with one right way to run it, write the actual command(s) the agent should run, in a code block — the same way this file specifies its own CLI steps. Reserve natural-language instruction for the parts of the job that genuinely need judgment (what the grill couldn't reduce to a fixed sequence).

If grill item 5 flagged self-update: set `memory: project` so the agent gets a persistent `.claude/agent-memory/{name}/` notes directory, checked into version control. In the prompt body, instruct it explicitly: consult memory before starting work, and after finishing, write down what changed in the project since last time (new conventions, moved files, updated schemas).

`mkdir -p .claude/agents` if needed. Write `.claude/agents/{name}.md`.

## 6. Validate deterministically

Don't eyeball it — run this sequence and require the stated result at each line:

```bash
awk '/^---$/{c++} END{print c}' .claude/agents/{name}.md          # must print 2
grep -c "^name:" .claude/agents/{name}.md                          # must print 1
grep -c "^description:" .claude/agents/{name}.md                   # must print 1
grep -E "^(tools|model|permissionMode|isolation|memory|skills):" .claude/agents/{name}.md   # extract every optional field present
```
For each field the last command prints, look it up in `references/claude-agent-schema.md` and confirm the value used is in that field's valid-values column. Any failed line above → fix the file and re-run the whole sequence before reporting done.

Completion criterion: the file exists at `.claude/agents/{name}.md`, passes the step 6 checks, carries no name collision, any project skills chosen in step 3 are wired in via `skills:`, and — if grill item 5 flagged self-update — the `memory` field and consult/update instructions are present.

Tell the user the path written. If this was the first agent file in a previously-empty `.claude/agents/`, remind them to restart Claude Code so the directory is picked up.

Any useful truth discovered during this session — a constraint, a domain fact, a key decision — can also be written to `.context/wiki/` at any time.
