# Skills

A collection of agent skills for software engineering and personal productivity.

---

## Installation

Clone this repo to `~/.claude/skills`, then run the install script:

```bash
git clone git@github.com:Jaeyong-Cho/skills.git ~/.claude/skills
~/.claude/skills/install.sh
```

The script detects which AI agents are installed and sets up each one:

| Agent | What gets configured |
|-------|----------------------|
| Claude Code | `~/.claude/CLAUDE.md` symlink |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` symlink |

---

## Workflows

Skills are designed to chain. Here are the common pipelines:

### Find weaknesses → Write tests
```
/attack  →  /to-ut   (unit test for an isolated function)
         →  /to-it   (integration test across components)
         →  /to-e2et (end-to-end test for a full flow)
```
Run `/attack` on any code. Each numbered finding in the report can be handed directly to one of the test-writing skills. Just invoke the next skill — it reads the current conversation and picks up the finding.

### Plan a feature → Implement it
```
/to-sot  →  /small-impl
```
`/to-sot` persists the plan to `source-of-truth/` so every subsequent skill reads it as context. `/small-impl` executes one atomic change at a time.

---

## All Skills

| Skill | What it does |
|-------|-------------|
| `/attack` | Adversarially find weaknesses across runtime, structure, architecture, and usability — produces a numbered finding list |
| `/to-ut` | Write a unit test targeting one specific function or edge case |
| `/to-it` | Write an integration test chaining real components together |
| `/to-e2et` | Write an end-to-end test driving the full application flow |
| `/feeling` | Emotional check-in — share what's good/bad/concerning/wanted, get grilled on the root cause, land on a concrete decision |
| `/grill-me` | Relentless interviewing about any plan or design until shared understanding is reached |
| `/small-impl` | Implement one atomic change; blocks and decomposes if the plan is too large |
| `/to-todo` | Add or remove tasks in `TODO.md` directly |
| `/to-sot` | Save the current conversation's intent to `source-of-truth/` so future skills read it as context |
| `/caveman` | Ultra-compressed output mode — ~75% fewer tokens, no filler |
| `/write-a-skill` | Create a new skill with proper structure and description |

---

## `source-of-truth/`

Many skills say "if `source-of-truth/` exists, read it." This directory holds your project's goals, constraints, and decisions so every skill session starts with context.

Create and update it with `/to-sot` — it reads the current conversation and writes the relevant intent as a markdown file into `source-of-truth/`.
