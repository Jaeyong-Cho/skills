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

`/grilling` and `/grill-me` are not local skills in this repo — they're installed from the `mattpocock-skills` plugin (marketplace `mattpocock`, repo `mattpocock/skills`; see `install.sh`). `dev-grill-me` below depends on `/grilling` being installed (named to avoid colliding with the plugin's own `/grill-me`).

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/dev-grill-me` | — | Run `/grilling` covering both feature and fix concerns in one pass: intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan |
| `/refact-grill-me` | — | Run `/grilling` to build understanding of an unfamiliar target through four lenses — architecture fit (meta-pattern), interface depth (deep-modules), naming, simplicity (ponytail) — then value, behavior-preservation proof, impact scope, testability, release plan — run before `/to-plan` |
| `/end-of-day` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD-report.md`, `.../YYYY-MM-DD-report/index.html` | Run `/d-handoff` and `/advisor`, then compile the day's journal/research/handoff/advisor findings into a ToC report with an Introduction/Abstraction/Detailed section per topic, plus a themed, servable HTML gallery with an insight diagram per topic |
| `/d-handoff` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD-handoff.md` | Distill today's open items and key decisions into a dated file for tomorrow's session |
| `/advisor` | `~/wiki/advisor/YYYY/MM/YYYY-MM-DD.md` | Scan the last 14 days of journal/research notes for recurring friction and turn it into automation candidates (script, custom agent, or AI-usage change) |
| `/to-plan` | `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{slug}/plans/nn-{slug}.md` | Write up this session's decisions as a plan: spec changes, acceptance criteria, and `- [ ]` action items — run after `/dev-grill-me` |
| `/do-plan` | `{plan-file}.report.md` | Execute a `/to-plan` document's action items in order, checking each off in place; verify acceptance criteria against real repo state; write up the run as a report |
| `/explore` | `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{slug}/explores/nn-{slug}.md` | Search the codebase/docs to answer a question with cited evidence; escalates to `/experiment` if exploring alone can't resolve it |
| `/experiment` | `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{slug}/experiments/nn-{slug}.md` | Plan the cheapest method that would answer a question (via `/ponytail`), act on it for real, then analyze the result into a verdict — supported, refuted, or inconclusive |
| `/to-docs` | user-selected path | Write the current session's work as a report-style document |
| `/to-todo` | inbox `TODO.md` | Turn a completed `/breakdown` tree (external to this repo) into an inbox TODO: objective/background/scope framing, a checkbox body numbered by the breakdown's dotted ids, and a conclusion with critical path and parallel-ready execution order |
| `/run-n-view` | `run-n-view/{slug}/raw/`, `run-n-view/{slug}/gallery/index.html` | Bare run+view primitive — launch/drive a command, script, or app for real via `run`, then build a `/viewpoints` gallery over the captured output |
| `/categorize` | `{dir}/{category}/`, `{dir}/index.md` | Sort a directory's loose files into MECE topic sub-directories, then write an `index.md` table of contents over the result |
| `/viewpoints` | `gallery/{slug}/index.html` | Build a gallery of complementary chart/diagram views on a dataset or structure instead of picking one form |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |

All skills above are user-invoked, except `/experiment`, `/d-handoff`, and `/advisor`, which the agent can also fire on its own — `/experiment` when a question needs something actually run to get evidence; `/d-handoff` and `/advisor` when the user wants to wrap up the day or get workflow advice, or when `/end-of-day` reaches for them before drafting. Most artifacts land in a skill-named directory at the project root; `/end-of-day`, `/d-handoff`, `/advisor`, `/to-plan`, `/explore`, and `/experiment` instead read and write the global `~/wiki/` layout documented in `CLAUDE.md`'s Context Structure section (journal/research/advisor/handoff), since they're personal daily-workflow tools rather than per-project outputs.

## References

Referenced by workflow skills — loaded at the point they're needed.

| Reference | What it covers |
|-----------|---------------|
| `archi.md` | Architecture layers: what question each layer answers, DDD equivalents |
| `meta-pattern.md` | Architecture decomposition: Abstractness, Subdomain, Sharding axes |
| `deep-modules.md` | Hide complexity, widen interfaces |
| `naming.md` | Intention-revealing names; a smells table (disinformative, noise words, encoded, mismatched part of speech, synonym drift, mental-mapping) |
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
| `spec-convention.md` | A target project's spec documents live under `spec/**/*.md` (format: `template/spec.md`), indexed by `spec/index.md` |
| `top-down-decompose.md` | MECE top-down decomposition methodology to split a goal into atomic sub-goals |
