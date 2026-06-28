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

## Skills

| Skill | What it does |
|-------|-------------|
| `/attack` | Adversarially find weaknesses across runtime, structure, architecture, and usability — produces a numbered finding list |
