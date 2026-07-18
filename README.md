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
/req  →  /archi  →  (choose planning path)  →  /auto-action  →  /merge-req, /merge-archi
                     ├─ /fs-plan  (full self-plan, full AI implementation)
                     └─ /co-plan  (collaborative plan, holes for human implementation)

/test  →  verify a plan's tests, or discover and run all tests — standalone, any time
```

All workflow skills are user-invoked. Artifacts land in `.context/`. All skills work on new development and fixing existing code.

### Implementation Paths

The branch happens at planning, not execution — `/auto-action` always runs, but behaves differently depending on which plan type it finds:

| Path | Test | Working Steps | Holes to Fill |
|------|------|---------------|---------------|
| **/fs-plan → /auto-action** | AI writes | AI writes (100%) | — |
| **/co-plan → /auto-action** | AI writes | AI writes (~70%) | You fill (~30%) |
| **/test** | Runs only | — | — |

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/req` | `.context/rdr/` | Find the goal, elicit functional/non-functional requirements, and write a draft Requirement Decision Record — asks the user only where a decision is important or ambiguous |
| `/archi` | `.context/adr/` | Resolve architecture, design, observability, test-loop, and verification criteria against `archi.md`, then write an ADR — asks the user only where a decision is important or ambiguous |
| `/fs-plan` | `.context/plan/` | Sequence the ADR's design into ordered TDD implementation steps, then write a regular plan, fully written and executed by AI |
| `/co-plan` | `.context/plan/` | Sequence the ADR's design into ordered TDD steps, and for each implementation step decide — block-by-block — what's a hole (for you to fill) vs working code (AI-written); writes a plan marked `**Type:** Self-Plan` |
| `/auto-action` | code changes | Execute the plan's action sequence. Regular plan: write tests → write code → verify, fully autonomous. Self-plan: write tests and working parts complete, leave recorded holes as explanatory TODOs, no run-to-green. |
| `/test` | test results | Run tests for a plan or discover and run all tests in the project. Verification only. |
| `/merge-req` | `.context/req/{slug}.md` | Merge the draft RDR into its committed spec once implementation is done; the RDR is kept and renamed `*.merged.md` |
| `/merge-archi` | `.context/adr/{slug}.md`, `.context/archi/{slug}.md` | Merge the draft ADR into its committed file, then derive the architecture doc (Static/Dynamic View) from the implemented result; the draft ADR is kept and renamed `*.merged.md` |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grilling` | — | Interview relentlessly about a plan, one question at a time, until every branch resolves. Called directly or from within other skills |
| `/create-agent` | `.claude/agents/*.md` or `.github/agents/*.agent.md` | Grill to design a project-specific subagent wired to existing skills, then write it |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |
| `/breakdown` | — | Break any goal into a MECE tree of atomic, actionable sub-goals, then order the leaves into a dependency-respecting execution sequence |

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
| `todo-hole.md` | Wording rule for a self-plan hole's TODO: input→output using real signature names, one abstracted example, ≤2 lines, no rationale, no technique hint |
| `good-harness.md` | Turn a natural-language constraint into a local, executable pass/fail check: Layer/Determinism axes, harness-by-shape table, anti-patterns |

## Templates

Auto-discovered by `/grilling`; filled in and written to `.context/` by the workflow skill that needs them.

| Template | Used by |
|----------|---------|
| `adr.md` | `/archi` — written to `.context/adr/{timestamp}-{slug}.md`, later merged into `.context/adr/{slug}.md` by `/merge-archi`, which renames it to `*.merged.md` |
| `architecture.md` | `/merge-archi` — derived from the merged ADR and the implemented code, written directly to `.context/archi/{slug}.md` (no draft/merged state) |
| `plan.md` | `/fs-plan` — written to `.context/plan/{timestamp}-{slug}.md`, pairs with an ADR of the same slug |
| `self-plan.md` | `/co-plan` — written to `.context/plan/{timestamp}-{slug}.md`, marked `**Type:** Self-Plan`, pairs with an ADR of the same slug |
| `requirements.md` | `/req` — written to `.context/rdr/{timestamp}-{slug}.md`, later merged into `.context/req/{slug}.md` by `/merge-req`, which renames it to `*.merged.md` |
