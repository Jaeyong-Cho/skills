# Skills

A collection of agent skills for software engineering and personal productivity.

---

## Installation

Clone this repo to `~/.claude/skills`, then run the install script:

```bash
git clone git@github.com:Jaeyong-Cho/skills.git ~/.claude/skills
~/.claude/skills/install.sh
```

## Repository Layout

```
skills/       executable skills; each skill owns its SKILL.md and optional resources
references/   shared guidance loaded by skills
bin/          installed helper scripts
```

Skills refer to shared root-level resources with `../references/...` because their `SKILL.md` files land as siblings of `references/` once installed (`skills/` flattens directly under the install target).

The script detects which AI agents are installed and sets up each one:

| Agent | What gets configured |
|-------|----------------------|
| Claude Code | Copies `skills/` and `preferences/` to `~/.claude/skills/`; configures the `~/.claude/CLAUDE.md` symlink, `rtk init -g` hooks, and the `ponytail` and `mattpocock-skills` plugins (marketplace installs) |
| GitHub Copilot CLI | Copies `skills/` and `preferences/` to `~/.copilot/skills/`; `~/.copilot/copilot-instructions.md` symlink, `rtk init -g --copilot` hooks, and the same two plugins |

`references/` is not copied by the installer — skills read it from this repo's own path (`../references/...`), since `skills/` and `references/` land as siblings either way.

## Grilling and grill-me

`/grilling` and `/grill-me` are not local skills in this repo — they're installed from the `mattpocock-skills` plugin (marketplace `mattpocock`, repo `mattpocock/skills`; see `install.sh`). `feat-grill-me` and `fix-grill-me` below both depend on `/grilling` being installed.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/feat-grill-me` | — | Run `/grilling` scoped to a new feature: scope-in/out, expected state, architecture, observability, testability, release plan |
| `/fix-grill-me` | — | Run `/grilling` scoped to a bug fix: root cause, regeneration, impact scope, observation, monitoring |
| `/to-plan` | `plans/{timestamp}-{slug}.md` | Write up this session's decisions as a plan: spec changes, acceptance criteria, and `- [ ]` action items |
| `/do-plan` | `{plan-file}.report.md` | Execute a `/to-plan` document's action items in order, checking each off in place; verify acceptance criteria against real repo state; write up the run as a report |
| `/explore` | `.context/explore/{slug}/` | Search the codebase/docs to answer a question with cited evidence; escalates to `/experiment` if exploring alone can't resolve it |
| `/experiment` | `.context/experiment/{slug}/` | Plan the cheapest method that would answer a question (via `/ponytail`), act on it for real, then analyze the result into a verdict — supported, refuted, or inconclusive |
| `/to-docs` | user-selected path | Write the current session's work as a report-style document |
| `/to-todo` | inbox `TODO.md` | Turn a completed `/breakdown` tree (external to this repo) into an inbox TODO: objective/background/scope framing, a checkbox body numbered by the breakdown's dotted ids, and a conclusion with critical path and parallel-ready execution order |
| `/run-n-view` | `run-n-view/{slug}/raw/`, `run-n-view/{slug}/gallery/index.html` | Bare run+view primitive — launch/drive a command, script, or app for real via `run`, then build a `/viewpoints` gallery over the captured output |
| `/viewpoints` | `gallery/{slug}/index.html` | Build a gallery of complementary chart/diagram views on a dataset or structure instead of picking one form |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |

All skills above are user-invoked, except `/experiment` which the agent can also fire on its own when a question needs something actually run to get evidence. Artifacts land in `.context/` or a skill-named directory at the project root, per skill.

## References

Referenced by workflow skills — loaded at the point they're needed.

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
| `good-harness.md` | Turn a natural-language constraint into a local, executable pass/fail check: Layer/Determinism axes, harness-by-shape table, anti-patterns |
| `document-style.md` | Structured-format style, key-value format: priority order (diagram/table > bullets > prose), when to use a flow diagram vs a table, Introduction/Body/Conclusion structure — covers both chat/plans and standalone docs |
| `preference-format.md` | Standing-vs-one-off test and entry format for recorded preferences |
| `requirement-engineering.md` | Elicitation, analysis, specification, validation, management — the five requirement-engineering activities |
| `top-down-decompose.md` | MECE top-down decomposition methodology to split a goal into atomic sub-goals |
