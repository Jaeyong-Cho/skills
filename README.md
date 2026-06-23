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
| Claude Code | `~/.claude/CLAUDE.md` symlink + `PFJ_PATH` in `settings.json` and shell rc |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` symlink + `PFJ_PATH` in shell rc |

`PFJ_PATH` is exported in `.zshrc`/`.bashrc` and points to your journal directory (default: `~/pofe`).

---

## Global Instructions

`CLAUDE.md` defines global behaviors active in every session:

- **Caveman style** — terse, no filler, fragments ok, technical terms exact
- **Session logging** — after any skill session, append a timestamped summary + lessons to `$PFJ_PATH/today.md`

---

---

## Prototype → Design Workflow

A bottom-up pipeline: explore first, design from evidence.

```
/expected  →  /proto  →  /observe  →  /to-tdgoal
```

| Step | Skill | What happens |
|------|-------|-------------|
| 1 | `/expected` | Grill user to produce unambiguous input/output pairs; written to `expected/<slug>.md` |
| 2 | `/proto` | Build a throwaway prototype in `proto/<slug>/`; optionally reads an expected file to shape output |
| 3 | `/observe` | Run the prototype, collect output, write an analytical report to `proto/<slug>/observe/<timestamp>-<slug>.md` |
| 4 | `/to-tdgoal` | Read source + observe reports; grill; write an ADR grounded in what the prototype actually proved |

### When to use each path

- **Start with `/expected`** when you know what behavior you want but not how to get there
- **Start with `/proto`** when you want to explore and don't know what you'll find
- **Use `/tdgoal`** instead of `/to-tdgoal` when starting from a hypothesis, not a prototype

---

## Other Skills

| Skill | What it does |
|-------|-------------|
| `tdgoal` | Top-down decomposition of a goal into sub-goals grounded in architecture layers; writes ADR |
| `if-write` | Design an interface through grilling; writes structured IF doc |
| `if-impl` | Implement an existing IF spec faithfully using TDD |
| `docs-init` | Initialize an mdBook docs project with themes and mermaid |
| `docs-write` | Write program documentation through grilling; writes to docs/src/ |
| `grill-me` | Interview relentlessly about any plan or design until shared understanding is reached |
| `caveman` | Ultra-compressed output mode — ~75% fewer tokens, no filler |
| `write-a-skill` | Create or review agent skills with proper structure and checklist |
