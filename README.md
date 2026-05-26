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

## PF — Architecture Workflow

PF applies the VAO (Value–Aspect–Object) three-layer design philosophy: **Value** (why — user goals), **Aspect** (how — composable algorithms), **Object** (what — stable domain objects).

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
                               pf-review  ──→  code review + docs updated

[design + implement without ADR]
        ↓
  pf-grill-impl  ──→  TDD implementation (no ADR)

[validate with real data]
        ↓
  pf-e2e-val  ──→  create/edit cases + run affected
                        ↓
             pf-e2e-val-report  ──→  re-run specific or all cases

[trace a scenario through code]
        ↓
    pf-sim  ──→  execution trace + verdict

[observe runtime behavior — logs, data, state, config]
        ↓
  pf-observe  ──→  observation scripts + cause analysis
                        ↓
          pf-observe-report  ──→  run scripts + HTML findings report
```

### Skills

| Skill | When to use |
|-------|-------------|
| `pf-init` | First time — initialize the `.pf/` book in the project |
| `pf-proto` | Design question unresolved — throwaway prototype + PoC document |
| `pf` | Design clear — grill-me session, write and confirm an ADR |
| `pf-impl` | ADR confirmed — TDD implementation, RED → GREEN → REFACTOR |
| `pf-grill-impl` | Design + implement in one session — no ADR written |
| `pf-review` | Implementation done — code review, scenario simulation, docs update |
| `pf-e2e-val` | Create or edit E2E validation cases; runs affected case(s) only |
| `pf-e2e-val-report` | Re-run specific or all existing E2E cases; generates analysis report |
| `pf-sim` | Trace a scenario through source code step by step; confirm/deny hypothesis |
| `pf-observe` | Build observation scripts to surface differences, patterns, and causes in a running system |
| `pf-observe-report` | Run observe/ scripts and generate an HTML report of findings and anomalies |
| `pf-docs-migrate` | One-time — migrate old feature-centric docs to layer-centric format |
| `pf-readme` | Write or update per-directory README.md files via grill-me |

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

validate/<slug>/
└── cases/
    └── NN-<name>/   # run.py · input.json · expected.json · result.json

observe/          # observation scripts (flat — no subdirs)

.pf/reports/
├── impl/     # pf-grill-impl session reports
├── validate/ # pf-e2e-val / pf-e2e-val-report reports
└── sim/      # pf-sim scenario reports
```

---

## PFJ — Daily Journal Workflow

PFJ is a personal productivity system: daily journaling, goal management, wiki, and research notes, rendered via mdbook.

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
        [experiment or insight to capture?]
                        ↓
          pfj-research  ──→  markdown research note written
                        ↓
        [what notes are due for review today?]
                        ↓
        pfj-retention  ──→  daily spaced repetition report
                        ↓
              [end of day]
                        ↓
             pfj-review  ──→  daily report written
                               wiki entries extracted
                               tomorrow seeded
```

### Skills

| Skill | When to use |
|-------|-------------|
| `pfj-init` | First time — initialize the knowledge base repo |
| `pfj-grill` | Any time — think through a concern, plan, or decision |
| `pfj-adjust` | Mid-day — priorities changed, task blocked, new urgent work |
| `pfj-research` | Any time — capture experiment, observation, or insight as markdown note |
| `pfj-research-report` | Generate HTML report from one or more research notes (by date or topic) |
| `pfj-retention` | Any time — daily spaced repetition report; shows which research notes are due for review today |
| `pfj-review` | End of day — close the day, extract wiki entries, seed tomorrow |

### Journal structure

```
$PFJ_PATH/
├── today.md              # daily goals + journal
├── goals/
│   ├── goal.md           # lifetime goals
│   └── YYYY/
│       ├── goal.md       # yearly
│       ├── goal-MM.md    # monthly
│       └── goal-MM-WNN.md # weekly
├── wiki/                 # persistent knowledge entries
├── Journal/              # archived daily entries
├── discuss/              # pfj-grill HTML reports
├── review/               # pfj-review HTML reports
└── research/             # pfj-research markdown notes + HTML reports
    ├── YYYY/
    │   └── MM-DD-<slug>.md
    └── reports/
        └── YYYY/
            ├── MM-DD-<scope>.html          # pfj-research-report
            └── retention-MM-DD.html        # pfj-retention
```

---

## Other Skills

| Skill | What it does |
|-------|-------------|
| `grill-me` | Interview relentlessly about any plan or design until shared understanding is reached |
| `caveman` | Ultra-compressed output mode — ~75% fewer tokens, no filler |
| `write-a-skill` | Create or review agent skills with proper structure and checklist |
