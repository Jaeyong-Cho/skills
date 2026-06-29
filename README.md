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
/attack  →  /directing  →  /planning  →  /action      →  /evaluate
                ↑                         /auto-action        |
                └──────────── failures feed back ─────────────┘
```

All workflow skills are user-invoked. Artifacts land in `source-of-truth/`. All skills work on new development and fixing existing code.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/attack` | `source-of-truth/attack/` | Find weaknesses — each finding is a goal for /directing |
| `/directing` | `source-of-truth/wiki/` | Grill to find the goal, explore decision space, commit to a direction |
| `/planning` | `source-of-truth/adr/` | Grill to design architecture, test plan, and action sequence |
| `/action` | code changes | Execute the ADR one confirmed step at a time |
| `/auto-action` | code changes | Execute the ADR straight through without confirmation |
| `/evaluate` | `source-of-truth/evaluate/` | Run the test plan, deliver a verdict, flag failures for /attack |

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
