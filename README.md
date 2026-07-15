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
/drilling  →  /req  →  /archi  →  /planning  →  /auto-action  →  /merge-req, /merge-archi
```

`/drilling` is optional for goals small enough to spec in one pass — start straight at `/req` for those. For a broad goal, `/drilling` builds the whole tree of atomic sub-goals in one pass; it doesn't pick an order. You choose which leaf to send through `/req` next, and re-run `/drilling` any time to check status or extend the tree.

All workflow skills are user-invoked. Artifacts land in `.context/`. All skills work on new development and fixing existing code.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/drilling` | `.context/tree/` | Split a broad goal top-down into a tree of atomic, junior-developer-executable sub-goals, one per leaf small enough for `/req` |
| `/req` | `.context/rdr/` | Grill to find the goal, elicit functional/non-functional requirements, and write a draft Requirement Decision Record |
| `/archi` | `.context/adr/` | Grill to resolve architecture, design, observability, test-loop, and verification criteria against `archi.md`, then write an ADR |
| `/planning` | `.context/plan/` | Sequence the ADR's design into ordered TDD implementation steps, then write a plan |
| `/auto-action` | code changes | Execute the plan's action sequence straight through, no confirmation between steps |
| `/merge-req` | `.context/req/{slug}.md` | Merge the draft RDR into its committed spec once implementation is done; the RDR is kept and renamed `*.merged.md` |
| `/merge-archi` | `.context/adr/{slug}.md`, `.context/archi/{slug}.md` | Merge the draft ADR into its committed file, then derive the architecture doc (Static/Dynamic View) from the implemented result; the draft ADR is kept and renamed `*.merged.md` |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grilling` | — | Interview relentlessly about a plan, one question at a time, until every branch resolves. Called directly or from within other skills |
| `/create-agent` | `.claude/agents/*.md` or `.github/agents/*.agent.md` | Grill to design a project-specific subagent wired to existing skills, then write it |
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
| `top-down-decompose.md` | Split a goal top-down into a full tree of atomic, junior-developer-executable sub-goals before deciding execution order |

## Templates

Auto-discovered by `/grilling`; filled in and written to `.context/` by the workflow skill that needs them.

| Template | Used by |
|----------|---------|
| `adr.md` | `/archi` — written to `.context/adr/{timestamp}-{slug}.md`, later merged into `.context/adr/{slug}.md` by `/merge-archi`, which renames it to `*.merged.md` |
| `architecture.md` | `/merge-archi` — derived from the merged ADR and the implemented code, written directly to `.context/archi/{slug}.md` (no draft/merged state) |
| `plan.md` | `/planning` — written to `.context/plan/{timestamp}-{slug}.md`, pairs with an ADR of the same slug |
| `requirements.md` | `/req` — written to `.context/rdr/{timestamp}-{slug}.md`, later merged into `.context/req/{slug}.md` by `/merge-req`, which renames it to `*.merged.md` |
| `tree.md` | `/drilling` — written to `.context/tree/{slug}.md`, updated in place as the tree is drilled and leaves complete (no draft/merged state) |
