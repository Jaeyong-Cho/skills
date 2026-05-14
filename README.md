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
| Claude Code | `~/.claude/CLAUDE.md` symlink + `PFJ_PATH` in `settings.json` |
| GitHub Copilot CLI | `~/.copilot/AGENTS.md` symlink + `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` + `PFJ_PATH` in shell rc |
| VS Code + Copilot | `CLAUDE.md` reference in VS Code settings |
| Cursor | `~/.cursor/rules/global.md` symlink |
| Windsurf | `~/.codeium/windsurf/global_rules.md` symlink |

`PFJ_PATH` is exported in `.zshrc`/`.bashrc` and points to your journal directory (default: `~/pofe`).

---

## Global Instructions

`CLAUDE.md` (Claude Code) and `AGENTS.md` (Copilot CLI) define global behaviors active in every session:

- **Session logging** — after any skill session, append a timestamped summary + lessons to `$PFJ_PATH/today.md`
- **Skill feedback** — ask for feedback on the skill after logging, to surface improvement ideas

Format in today.md:
```markdown
## HH:MM:SS (skill-name)

**Summary**: what was done — outcomes, files changed, decisions made
**Lessons**: what to carry forward
**Feedback**: (if given)
```

---

## PF — Architecture Workflow

PF applies the VAO (Value–Aspect–Object) three-layer design philosophy: **Value** (why — user goals), **Aspect** (how — composable algorithms), **Object** (what — stable domain objects).

All pf-* skills follow caveman style — terse, no filler, including in output documents.

### Workflow

```
[uncertain about design?]
        ↓
   pf-proto  ──→  PoC document
                        ↓
[clear on what to build]
        ↓
      pf    ──→  ADR (written + confirmed)
                        ↓
                   pf-impl  ──→  TDD implementation
                                        ↓
                              code review confirmed
                                        ↓
                               pf-docs  ──→  documentation updated
```

### Skills

| Skill | When to use |
|-------|-------------|
| `pf-init` | First time — initialize the `.pf/` book in the project |
| `pf-proto` | Design question unresolved — throwaway prototype + PoC document |
| `pf` | Design clear — grill-me session, write and confirm an ADR |
| `pf-impl` | ADR confirmed — TDD implementation, RED → GREEN → REFACTOR |
| `pf-docs` | Implementation reviewed — write or update project documentation |
| `pf-docs-migrate` | One-time — migrate old feature-centric docs to layer-centric format |

### Artifacts

```
.pf/
├── src/
│   ├── adr/    # Architectural Decision Records (0001-slug.md)
│   ├── poc/    # Proof of Concept documents (0001-slug.md)
│   └── docs/   # Project documentation
│       ├── value/    # Why — user goals per component
│       ├── aspect/   # How — workflows per component
│       └── object/   # What — domain objects per component
└── serve.sh    # Start the book server
```

---

## PFJ — Daily Journal Workflow

PFJ is a personal productivity system: daily journaling, goal management, achievement tracking, wiki, and work pattern analysis, rendered via mdbook.

### Workflow

```
[start of day]
      ↓
  pfj-init  ──→  knowledge base ready  (run once)
                        ↓
               write in today.md freely
                        ↓
        [concern, plan, or decision to work through?]
                        ↓
             pfj-grill  ──→  conclusion recorded in today.md
                        ↓
            [priorities shift mid-day?]
                        ↓
             pfj-adjust  ──→  today's goal updated
                        ↓
              [end of day]
                        ↓
             pfj-review  ──→  daily report written
                               goal progress marked
                               tomorrow seeded
```

### Skills

| Skill | When to use |
|-------|-------------|
| `pfj-init` | First time — initialize the knowledge base repo |
| `pfj-grill` | Any time — think through a concern, plan, or decision; records conclusion in today.md |
| `pfj-adjust` | Mid-day — priorities changed, task blocked, new urgent work |
| `pfj-review` | End of day — close the day, propagate goal progress, seed tomorrow |

### Journal structure

```
~/pofe/
├── today.md              # daily goals + journal
├── goals/
│   ├── goal.md           # lifetime goals
│   └── YYYY/
│       ├── goal.md       # yearly
│       ├── goal-MM.md    # monthly
│       └── goal-MM-WNN.md # weekly
├── wiki/                 # persistent knowledge
├── Journal/              # archived daily entries
├── stats/                # work pattern data
└── archive/              # completed goals
```

---

## Other Skills

| Skill | What it does |
|-------|-------------|
| `grill-me` | Interview relentlessly about any plan or design until shared understanding is reached |
| `caveman` | Ultra-compressed output mode — ~75% fewer tokens, no filler |
| `write-a-skill` | Create new agent skills with proper structure and review checklist |

---

## Deprecated

Skills in `deprecated/` are no longer actively used. The `sophist-*` documentation skills have been superseded by the PF workflow.
