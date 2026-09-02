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
| Claude Code | Copies `skills/` and `preferences/` to `~/.claude/skills/`; configures the `~/.claude/CLAUDE.md` symlink, `rtk init -g` hooks, and the `ponytail` plugin (marketplace install) |
| GitHub Copilot CLI | Copies `skills/` and `preferences/` to `~/.copilot/skills/`; `~/.copilot/copilot-instructions.md` symlink, `rtk init -g --copilot` hooks, and the same plugin |
| pi coding agent | Installs `ponytail`'s skill commands via [skills.sh](https://www.skills.sh/) (`npx skills add DietrichGebert/ponytail -a pi -g -y`) |

`references/` is not copied by the installer — skills read it from this repo's own path (`../references/...`), since `skills/` and `references/` land as siblings either way.

The script also copies `skills/`, `references/`, and `template/` to `~/.agents/skills/`, the global directory defined by the [Agent Skills standard](https://agentskills.io/specification) — read by `pi` and other harnesses that follow it, independent of Claude/Copilot.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grill-me` | — | Personal grilling engine: interview one question at a time from a design-tree frontier; when the user can't answer, drop into progressive-disclosure clarification before returning to the question |
| `/dev-grill-me` | — | Run `/grill-me` covering both feature and fix concerns in one pass: intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan |
| `/req-grill-me` | — | Run `/grill-me` to build an agile Story in one pass: persona, user value, trigger, happy/alternate/edge/negative scenarios, dependencies, INVEST check |
| `/refact-grill-me` | — | Run `/grill-me` to refactor a named function or usecase sequence against `abstraction-levels.md`'s L1/L2/L3 rule: current shape and smells, behavior-preservation baseline, target decomposition |
| `/l1-grill-me` | — | Run `/grill-me` to nail down one L1 orchestration flow's step sequence: trigger, ordered L2/L3 calls, branches, end state — feeds `/l1-implement` |
| `/l1-implement` | — | Implement one L1 orchestration function directly from a plain-language use-case description, per `abstraction-levels.md`: decompose into L2/L3, reuse before creating, stub every missing dependency as a loud TODO (never build it here), code only — no plan file, lighter than `/dev-grill-me` |
| `/l2-implement` | — | Implement one L2 domain function directly from a plain-language business-rule description, per `abstraction-levels.md`: depends on L3 only through an interface, never a concrete implementation, code only |
| `/l3-implement` | — | Implement one L3 mechanism function directly from a plain-language technical-operation description, per `abstraction-levels.md`: exposes a simple interface upward, no business decisions inside, code only |
| `/func-test` | — | Write and run a real test for one existing function — the decoupled test step for `/l1-implement`/`/l2-implement`/`/l3-implement` — choosing L1 integration / L2 domain-rule / L3 real-mechanism shape per `abstraction-levels.md`'s Testing by level |
| `/end-of-day` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD/report.md`, `.../YYYY-MM-DD/report/index.html` | Run `/d-handoff`, then compile the day's journal/research/handoff findings into a ToC report with an Introduction/Abstraction/Detailed section per topic, plus a themed, servable HTML gallery with an insight diagram per topic |
| `/d-handoff` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD/handoff.md` | Distill today's open items and key decisions into a dated file for tomorrow's session |
| `/to-plan` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD/research/NN-{slug}/plans/nn-{slug}.md` | Write up this session's decisions as a plan: spec changes, acceptance criteria, and `- [ ]` action items — run after `/dev-grill-me` |
| `/do-plan` | `{plan-file}.report.md` | Execute a `/to-plan` document's action items in order, checking each off in place; verify acceptance criteria against real repo state; write up the run as a report |
| `/experiment` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD/research/NN-{slug}/experiments/nn-{slug}.md`, `.../nn-{slug}.raw/` | Plan the cheapest method that would answer a question (via `/ponytail`), act on it for real, analyze the result into a verdict — supported, refuted, or inconclusive — then write it up as a linted Title/Abstract/.../Conclusion markdown report |
| `/to-context` | `~/wiki/today/research/NN-{slug}/contexts/nn-{slug}.md` | Write up this session as a context document — objective, background, key facts, current state — so a fresh session can resume it cold |
| `/to-journal` | `~/wiki/today/journal.md` | Summarize this session very short, ELI5-simple, and append it as a formatted entry to today's journal |
| `/categorize` | `{dir}/{category}/`, `{dir}/index.md` | Sort a directory's loose files into MECE topic sub-directories, then write an `index.md` table of contents over the result |
| `/to-paper` | `{slug}-research-paper/{index.html,manifest.json,assets/*.svg}` | Write a short HTML research paper — numbered Introduction/Background/Methodology/Results/Conclusion, at least 5 figures (diagram-design-themed SVGs drawn as HTML then exported per its export.md, and/or tables) — from a manifest.json, linted for writing-quality rules and built with a script; never hand-edit the HTML |
| `/grill-ai` | — | Toggle mode: clarify unclear requests before answering, then answer in layers (core answer first, depth only on request), in plain ELI5 language |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |
| `diagram-design` | — | Vendored from [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) (MIT). Draw architecture, flowchart, sequence, state-machine, ER, and other diagram types as standalone HTML/SVG/PNG, including redrawing existing `.drawio`/Mermaid sources |
| `frontend-design` | — | Vendored from [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Apache 2.0). Guidance for distinctive, intentional visual design when building or reshaping UI — deliberate palette/typography/layout choices, one justified aesthetic risk, avoiding the generic AI-design defaults |
| `thermo-nuclear-code-quality-review` | — | Vendored from [cursor/plugins](https://github.com/cursor/plugins/tree/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review) (MIT). An unusually strict maintainability review — abstraction quality, file-size/spaghetti smells, code-judo restructurings — for the current branch's diff |

All skills above are user-invoked, except `/experiment` and `/d-handoff`, which the agent can also fire on its own — `/experiment` when a question needs something actually run to get evidence; `/d-handoff` when the user wants to wrap up the day, or when `/end-of-day` reaches for it before drafting. Most artifacts land in a skill-named directory at the project root; `/end-of-day`, `/d-handoff`, `/to-plan`, and `/experiment` instead read and write the global `~/wiki/` layout documented in `CLAUDE.md`'s Context Structure section (journal/research/handoff), since they're personal daily-workflow tools rather than per-project outputs.

## References

Referenced by workflow skills — loaded at the point they're needed.

| Reference | What it covers |
|-----------|---------------|
| `abstraction-levels.md` | L1/L2/L3 function abstraction levels, dependency direction, smells |
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
| `requirement-engineering.md` | Elicitation, analysis, specification, validation, management — the five requirement-engineering activities |
| `spec-convention.md` | A target project's spec documents live under `spec/{epic-slug}/{story-slug}.md` (format: `template/spec.md`), indexed by `spec/{epic-slug}/index.md` and the top-level `spec/index.md` |
| `top-down-decompose.md` | MECE top-down decomposition methodology to split a goal into atomic sub-goals |
