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
/brainstorm  ↘
/attack      →  /directing  →  /planning  →  /action      →  /evaluate
                    ↑                         /auto-action        |
                    └──────────── failures feed back ─────────────┘
```

All workflow skills are user-invoked. Artifacts land in `.sot/`. All skills work on new development and fixing existing code.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/brainstorm` | ideas | Read the codebase, grill to surface gaps, pain, and opportunities |
| `/attack` | `.sot/attack/` | Find weaknesses — each finding is a goal for /directing |
| `/directing` | `.sot/direction/` | Grill to find the goal, explore decision space, commit to a direction |
| `/planning` | `.sot/adr/` | Grill to design architecture, test-loop, and action sequence |
| `/action` | code changes | Execute the ADR one confirmed step at a time |
| `/auto-action` | code changes | Execute the ADR straight through without confirmation |
| `/evaluate` | `.sot/evaluate/` | Run the test-loop, surface unexpected results and root causes |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/to-todo` | `.sot/TODO.md` | Manage a global checklist — add, check off, remove tasks |
| `/to-changelog` | `.sot/changelog/{year}/{month-day}.md` | Append a dated entry summarizing what changed |
| `/to-wiki` | `.sot/wiki/` | Harvest tacit knowledge — one file per topic |
| `/to-html` | HTML file | Render any file as a rich Kanagawa-themed HTML document |

## References

Referenced by workflow skills — loaded at the point they're needed.

| Reference | What it covers |
|-----------|---------------|
| `meta-pattern.md` | Architecture decomposition: Abstractness, Subdomain, Sharding axes |
| `deep-modules.md` | Hide complexity, widen interfaces |
| `tdd.md` | Test-driven development principles |
| `tdd-tests.md` | How to write good tests |
| `tdd-mocking.md` | When and how to mock |
| `test-loop.md` | Build a tight harness that mirrors real system: real result, debug output, logs |
