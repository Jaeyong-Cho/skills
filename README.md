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

## Workflow

```
/attack  →  /directing  →  /planning  →  /action  →  /evaluate
                ↑                                          |
                └──────────── failures feed back ─────────┘
```

All workflow skills are user-invoked. Artifacts land in `source-of-truth/`.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/attack` | `source-of-truth/attack/` | Find weaknesses — each finding is a goal for /directing |
| `/directing` | `source-of-truth/wiki/` | Grill to find the goal, explore decision space, commit to a direction |
| `/planning` | `source-of-truth/adr/` | Grill to design architecture, test plan, and action sequence |
| `/action` | code changes | Execute the ADR one confirmed step at a time |
| `/evaluate` | `source-of-truth/evaluate/` | Run the test plan, deliver a verdict, flag failures for /attack |
