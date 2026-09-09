# Skills

A collection of agent skills for software engineering and personal productivity.

---

## Installation

Clone this repo to `~/.claude/skills`, then run the install script:

```bash
git clone git@github.com:Jaeyong-Cho/skills.git ~/.claude/skills
~/.claude/skills/install.sh
```

To configure Pi subagents, run:

```bash
~/.claude/skills/install.sh --subagent
```

This dedicated mode installs only `pi-interactive-subagents`: it lists the models available to Pi, asks for a model and thinking effort, updates Pi's subagent defaults, then copies `agents/*.md` to `~/.pi/agent/agents/` with those values in each agent's frontmatter. It skips all other plugins, skills, hooks, and helper binaries. The normal installer does not install or configure `pi-interactive-subagents`. Without `--subagent`, the normal installer runs and the repository's agent defaults are copied unchanged. `PI_SUBAGENT_MODEL`, `PI_SUBAGENT_THINKING`, and `--subagent-thinking` set prompt/default values for scripted or repeated installs.

## Repository Layout

```
skills/       executable skills; each skill owns its SKILL.md and optional resources
references/   shared guidance loaded by skills
agents/       global Pi subagent definitions
bin/          installed helper scripts
```

Skills refer to shared root-level resources with `../references/...` because their `SKILL.md` files land as siblings of `references/` once installed (`skills/` flattens directly under the install target).

The script detects which AI agents are installed and sets up each one:

| Agent | What gets configured |
|-------|----------------------|
| Claude Code | Copies `skills/`, `references/`, and `template/` to `~/.claude/skills/`; configures the `~/.claude/CLAUDE.md` symlink, `rtk init -g` hooks, and the `ponytail` plugin (marketplace install) |
| GitHub Copilot CLI | Copies `skills/`, `references/`, and `template/` to `~/.copilot/skills/`; configures the `~/.copilot/copilot-instructions.md` symlink, `rtk init -g --copilot` hooks, and the same plugin |
| pi coding agent | Copies `agents/` to `~/.pi/agent/agents/`; with `--subagent`, interactively applies one selected Pi model/thinking effort to every copied agent; enables Pi truecolor and installs `ponytail` plus the Pi UI packages |

`references/` and `template/` are copied alongside `skills/`, so installed skills can resolve sibling resources through paths such as `../references/...`.

The script also copies `skills/`, `references/`, and `template/` to `~/.agents/skills/`, the global directory defined by the [Agent Skills standard](https://agentskills.io/specification) — read by `pi` and other harnesses that follow it, independent of Claude/Copilot.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grill-me` | — | Personal grilling engine: interview one question at a time from a design-tree frontier; when the user can't answer, drop into progressive-disclosure clarification before returning to the question |
| `/now` | — | Break out of whatever's running — a `/grill-me` round, any conversation — and get one task done immediately, no plan/round/confirmation, then resume the interrupted flow exactly where it paused |
| `/dev-grill-me` | — | Run `/grill-me` covering both feature and fix concerns in one pass: intent, scope, value, root cause, architecture, impact, observability/monitoring, testability, release plan |
| `/req-grill-me` | — | Run `/grill-me` to build an agile Story in one pass: persona, user value, trigger, happy/alternate/edge/negative scenarios, dependencies, INVEST check |
| `/refact-grill-me` | — | Run `/grill-me` to refactor a named function or usecase sequence against `abstraction-levels.md`'s L1/L2/L3 rule: current shape and smells, behavior-preservation baseline, target decomposition |
| `/l1-grill-me` | — | Run `/grill-me` to nail down one L1 orchestration flow's step sequence: trigger, ordered L2/L3 calls, branches, end state — feeds `/l1-implement` |
| `/l2-grill-me` | — | Run `/grill-me` to nail down one L2 business rule: domain input, decision logic/branches, L3 interface dependency (if any), output — feeds `/l2-implement` |
| `/l3-grill-me` | — | Run `/grill-me` to nail down one L3 technical operation: interface, mechanism, failure modes — feeds `/l3-implement` |
| `/l1-implement` | — | Implement one L1 orchestration function directly from a plain-language use-case description, per `abstraction-levels.md`: decompose into L2/L3, reuse before creating, stub every missing dependency as a loud TODO (never build it here), code only — no plan file, lighter than `/dev-grill-me` |
| `/l2-implement` | — | Implement one L2 domain function directly from a plain-language business-rule description, per `abstraction-levels.md`: depends on L3 only through an interface, never a concrete implementation, code only |
| `/l3-implement` | — | Implement one L3 mechanism function directly from a plain-language technical-operation description, per `abstraction-levels.md`: exposes a simple interface upward, no business decisions inside, code only |
| `/req` | `spec/<epic>/<slice>.md` per slice | Turn prototype/context into an approved vertical-slice inventory, then write one requirement document per slice with concrete edge cases and deterministic acceptance criteria |
| `/ood` | `design/<epic>/<slice>.md` per slice | Design the approved requirement batch and write one object-oriented design-and-contract document per slice |
| `/end-of-day` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD/report.md`, `.../YYYY-MM-DD/report/index.html` | Run `/d-handoff`, then compile the day's journal/research/handoff findings into a ToC report with an Introduction/Abstraction/Detailed section per topic, plus a themed, servable HTML gallery with an insight diagram per topic |
| `/d-handoff` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD/handoff.md` | Distill today's open items and key decisions into a dated file for tomorrow's session |
| `/to-plan` | `plans/{nn}-{slice}.md` (or the confirmed wiki path) | Write one independently executable plan per vertical slice with the lowest-cost sufficient tests/checks, acceptance criteria, action items, review gate, and commit/merge/release gates |
| `/do-plan` | `{plan-file}.report.md` | Execute a `/to-plan` document's action items in order, checking each off in place; verify acceptance criteria against real repo state; write up the run as a report |
| `/experiment` | `~/wiki/journal/YYYY/MM/YYYY-MM-DD/research/NN-{slug}/experiments/nn-{slug}.md`, `.../nn-{slug}.raw/` | Plan the cheapest method that would answer a question (via `/ponytail`), act on it for real, analyze the result into a verdict — supported, refuted, or inconclusive — then write it up as a linted Title/Abstract/.../Conclusion markdown report |
| `/wayfinder` | — | Record each way's purpose, expected result, hypothesis, and assumptions, then plan `EXPLORE`, `EXPERIMENT`, `IMPL`, or `CHECKOUT` tasks using the cheapest reliable method |
| `/next-way` | recorded way outcomes, dependencies, readiness, and implementation evidence | Find the next actionable way; follow the recorded task approach without imposing a fixed process, then review implementation evidence against the expected result and way purpose before dependent work proceeds |
| `/to-way` | `ways/{nn}-{slug}/0-goal.md` and nested work-package files | Record a Wayfinder plan while preserving task kinds, Why/What/How details, dependency links, execution guidance, and done-task evidence |
| `/to-context` | `~/wiki/today/research/NN-{slug}/contexts/nn-{slug}.md` | Write up this session as a context document — objective, background, key facts, current state — so a fresh session can resume it cold |
| `/to-intents` | `intents/{nn}-{slug}.md` (or the confirmed wiki research topic) | Extract the user's goals, desired outcome, motivation, constraints, boundaries, decisions, and open questions into a reusable intent document |
| `/to-journal` | `~/wiki/today/journal.md` | Summarize this session very short, ELI5-simple, and append it as a formatted entry to today's journal |
| `/to-anki` | `{slug}.anki.csv` | Turn a requested topic, notes file, or explicit Q&A list into an Anki-importable flashcard CSV — one atomic fact per Front/Back row, with the `#separator`/`#columns` header Anki's importer auto-detects |
| `/grill-ai` | — | Toggle mode: clarify unclear requests before answering, then answer in layers (core answer first, depth only on request), in plain ELI5 language |
| `/follow-ai` | — | Start from what the user already understands and resolve one curiosity through small, interactive `/grill-ai`-style steps |
| `coding-interview` | `~/study/**` | Software-engineering mastery coach for coding-interview prep — mentor, interviewer, code reviewer, and design coach against a persistent `~/study/` workspace, a 500-problem curriculum, and a CS-fundamentals topic order/method paraphrased from jwasham/coding-interview-university; triggers on "start", "study mode", "interview me", code review, or logging real engineering experience |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |
| `diagram-design` | — | Vendored from [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) (MIT). Draw architecture, flowchart, sequence, state-machine, ER, and other diagram types as standalone HTML/SVG/PNG, including redrawing existing `.drawio`/Mermaid sources |
| `frontend-design` | — | Vendored from [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Apache 2.0). Guidance for distinctive, intentional visual design when building or reshaping UI — deliberate palette/typography/layout choices, one justified aesthetic risk, avoiding the generic AI-design defaults |
| `review-loop` | — | Orchestrate the recommended Outcome → Risk → Test → Clean review loop, with one targeted fix and re-review at a time |
| `review-outcome` | — | Review whether the change delivers its intended observable outcome |
| `review-risk` | — | Review material failure, boundary, integrity, and concurrency risks |
| `review-test` | — | Review whether tests provide reliable confidence in important behavior |
| `review-clean` | — | Review whether the change leaves the code simpler, clearer, and safer to change |

All skills above are user-invoked, except `/experiment`, `/d-handoff`, `/req`, `/ood`, `/to-plan`, `/do-plan`, `/follow-ai`, and `coding-interview`, which the agent can also fire on its own — `/experiment` when a question needs something actually run to get evidence; `/d-handoff` when the user wants to wrap up the day, or when `/end-of-day` reaches for it before drafting; the planning and implementation skills when their specific work is needed; `/follow-ai` when the user asks to learn or follow a topic step by step; `coding-interview` when the user says "interview me"/"study mode"/pastes code for interview practice, without needing to name it. Project development artifacts use the target repository's conventions. `/end-of-day`, `/d-handoff`, and `/experiment` retain the global `~/wiki/` layout documented in `CLAUDE.md`'s Context Structure section.


## References

Referenced by workflow skills — loaded at the point they're needed.

| Reference | What it covers |
|-----------|---------------|
| `abstraction-levels.md` | L1/L2/L3 function abstraction levels, dependency direction, smells |
| `meta-pattern.md` | Architecture decomposition: Abstractness, Subdomain, Sharding axes |
| `deep-modules.md` | Hide complexity, widen interfaces |
| `naming.md` | Intention-revealing names; a smells table (disinformative, noise words, encoded, mismatched part of speech, synonym drift, mental-mapping) |
| `prototype.md` | Throwaway happy-path prototypes as an experiment method |
| `testing-guidelines.md` | Choose the lowest-cost test level that provides confidence in important behavior and regressions |
| `tdd.md` | Optional test-driven development technique |
| `tdd-tests.md` | How to write good tests |
| `tdd-mocking.md` | When and how to mock |
| `tdd-refactoring.md` | Refactoring checklist — only after all tests pass |
| `test-loop.md` | Build a tight harness that mirrors real system: real result, debug output, logs |
| `deterministic-evaluation.md` | Choose an integration or E2E test with a repeatable pass/fail signal |
| `model-selection.md` | Pick opus/sonnet/haiku by task ambiguity, mistake cost, and verifiability |
| `good-harness.md` | Turn a natural-language constraint into a local, executable pass/fail check: Layer/Determinism axes, harness-by-shape table, anti-patterns |
| `document-style.md` | Structured-format style, key-value format: priority order (diagram/table > bullets > prose), when to use a flow diagram vs a table, Introduction/Body/Conclusion structure — covers both chat/plans and standalone docs |
| `requirement-engineering.md` | Elicitation, analysis, specification, validation, management — the five requirement-engineering activities |
| `spec-convention.md` | A target project's spec documents live under `spec/{epic-slug}/{story-slug}.md` (format: `template/spec.md`), indexed by `spec/{epic-slug}/index.md` and the top-level `spec/index.md` |
| `top-down-decompose.md` | MECE top-down decomposition methodology to split a goal into atomic sub-goals |
| `question-format.md` | Format human checkpoints with ❓ questions and ➡️ recommendations |
