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
| Claude Code | `~/.claude/CLAUDE.md` symlink, `rtk init -g` hooks, Understand-Anything plugin |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` symlink, `rtk init -g --copilot` hooks, Understand-Anything plugin |

---

## Workflow

```
/brainstorm  →  /directing  →  /planning  →  /auto-action
                    ↑                             |
                    └────── .context/wiki/ ───────┘
```

All workflow skills are user-invoked. Artifacts land in `.context/`. All skills work on new development and fixing existing code.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/brainstorm` | ideas | Read the codebase, grill to surface gaps, pain, and opportunities |
| `/directing` | `.context/direction/` | Grill to find the goal, explore decision space, commit to a direction |
| `/planning` | `.context/adr/` | Grill to design architecture, test-loop, and action sequence, then write an ADR |
| `/auto-action` | code changes | Execute the ADR's action sequence straight through, no confirmation between steps |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grilling` | — | Interview relentlessly about a plan, one question at a time, until every branch resolves. Called directly or from within other skills |
| `/create-agent` | `.claude/agents/*.md` or `.github/agents/*.agent.md` | Grill to design a project-specific subagent wired to existing skills, then write it |
| `/to-todo` | `.context/TODO.md` | Manage a global checklist — add, check off, remove tasks |
| `/to-changelog` | `.context/changelog/{year}/{month-day}.md` | Append a dated entry summarizing what changed |
| `/to-wiki` | `.context/wiki/` | Harvest tacit knowledge — one file per topic |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |

## References

Referenced by workflow skills — loaded at the point they're needed. Also auto-discovered by `/grilling` so any branch of an interview can pull the matching file in.

| Reference | What it covers |
|-----------|---------------|
| `archi.md` | Architecture layers: what question each layer answers, DDD equivalents |
| `meta-pattern.md` | Architecture decomposition: Abstractness, Subdomain, Sharding axes |
| `deep-modules.md` | Hide complexity, widen interfaces |
| `tdd.md` | Test-driven development principles |
| `tdd-tests.md` | How to write good tests |
| `tdd-mocking.md` | When and how to mock |
| `tdd-refactoring.md` | Refactoring checklist — only after all tests pass |
| `test-loop.md` | Build a tight harness that mirrors real system: real result, debug output, logs |
| `model-selection.md` | Pick opus/sonnet/haiku by task ambiguity, mistake cost, and verifiability |

## Templates

Auto-discovered by `/grilling`; filled in and written to `.context/` by the workflow skill that needs them.

| Template | Used by |
|----------|---------|
| `adr.md` | `/planning` — written to `.context/adr/{timestamp}-{slug}.md` |
| `requirements.md` | Spec/requirements gathering during `/grilling` |
