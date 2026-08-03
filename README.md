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
preferences/  cross-project standing preferences
template/     shared artifact templates
bin/          installed helper scripts
```

Skills refer to shared root-level resources with `../../references/...`, `../../template/...`, or `../../preferences/...` because their `SKILL.md` files live one directory deeper under `skills/`.

The script detects which AI agents are installed and sets up each one:

| Agent | What gets configured |
|-------|----------------------|
| Claude Code | Copies `skills/`, `references/`, `preferences/`, and `template/` to `~/.claude/skills/`; configures the `~/.claude/CLAUDE.md` symlink, `rtk init -g` hooks, and Understand-Anything plugin |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` symlink, `rtk init -g --copilot` hooks, Understand-Anything plugin |

---

## Goal-to-Implementation Loop

The macro loop this repo is built around: validate the riskiest question as cheaply as possible before committing to a spec or writing code, then close the loop by testing the shipped result against that same question.

```
Goal
 |
 v
/goal-init                   writes goal.md's `## Question N` headings, creates
 |                            questions/{slug}/ per question, (re)builds the
 |                            questions dashboard (questions/index.html)
 v
Question                       e.g. "SQLite vs Postgres: which is
 |                                   reliable enough here?"
 v
/explore                     -> /experiment -> /viewpoints, each run and gated
 |                            separately (see /experiment's references/pipeline.md):
 |                            stop as soon as a stage resolves the question --
 |                            explore alone if it's a lookup, a verdict alone if
 |                            no visual is needed -- only running further stages
 |                            when the question genuinely requires it
 v
Ideas                        read the report (and gallery, if built), generate options
 |
 v
Direction                    pick how the goal will be resolved
 |
 v
/p4d -> /work                 plan the implementation, then execute it
 |                             step-by-step -- or /e2p instead, when the
 |                             direction is bridging an experiment's
 |                             findings into a specific product target
 v
/experiment                  re-test the implementation against the
 |                            original hypothesis
 v
Goal closed
```

- **Cheapest method first.** When requesting `/experiment`, the point is picking the cheapest way to resolve the question — a spike, a small script, existing data — not a full build. See `/experiment` in the Skills table below.
- **Ideas -> Direction -> Implementation.** The direction decided from the experiment's ideas feeds straight into `/p4d` (or `/e2p`, when bridging an experiment into a product target) — see Implementation below.
- **Same skill opens and closes the loop.** `/experiment` both answers the upfront hypothesis and, later, verifies the implementation actually resolved it — no separate test-writing step is needed for that check. It also writes a one-line `**Answer:**` back under the matching `## Question N` heading in `goal.md`, so the goal statement itself carries the answer, not just the report.
- **No questions yet?** Run `/question-brainstorm` right after `/goal-init` writes the goal statement — it proposes candidate questions from the goal plus existing context, lets you pick and edit, appends the chosen ones as `## Question N` headings in `goal.md`, then hands off back to `/goal-init` to create their directories and build the dashboard.

## Implementation

Two ways to turn a direction into code, depending on where it came from:

| Path | When | What it does |
|------|------|---------------|
| `/p4d` → `/work` | General implementation from any context (file, directory, URL, description) | `/p4d` reads the context and writes a plan as `plan/index.md` (group table) plus one `plan/group-{n}.md` per parallel-execution group; `/work` executes a plan step-by-step, verifying each step before moving to the next |
| `/e2p` | Direction is "take this experiment's findings into a specific product target" | Grills, explores, plans (via `/p4d`), implements (via `/work`), and reviews against the integration goal — or a single haiku dispatch fast track when the experiment's report already fully specifies a small change |

All skills are user-invoked. Artifacts land in `.context/`.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/goal-init` | `goal.md`, `questions/{slug}/` (each grilled at creation), `questions/index.html` | Bootstrap a new goal — write the goal statement and its `## Question N` headings to project-root `goal.md`, create each question's `questions/{slug}/` directory and grill it once for real intent/non-negotiables/constraints (`/experiment`'s core stage reuses this instead of re-grilling), and build/refresh a dashboard linking every question's report and viewpoint gallery |
| `/question-brainstorm` | `## Question N` headings in `goal.md` | Propose 3-5 candidate questions from the goal statement, existing context, and (when relevant) a fresh `/explore` pass; user picks/edits, then it appends the chosen ones to `goal.md` and hands off to `/goal-init` for directory creation |
| `/p4d` | `plan/index.md`, `plan/group-{n}.md` | Read a context location (file, directory, URL, or description), analyze the codebase if relevant, and write a step-by-step implementation plan as one file per parallel-execution group so a subagent dispatched to one group only needs that group's file |
| `/work` | code changes | Execute a `/p4d` plan (or one group of it) step-by-step: understand, act, verify, report, move forward — only proceeds past a step once its verification passes |
| `/e2p` | `.context/{timestamp}-{goal-slug}/` (intent, plan, implementation, review), code changes | Bridge an experiment's findings into a product target: grill for product-specific unknowns, explore, plan (`/p4d`, sonnet), implement (`/work`, haiku, per parallel-execution wave), review against the goal (sonnet) — or a single haiku dispatch fast track when the experiment's `report.md` already fully specifies a small integration |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grilling` | — | Interview relentlessly about a plan, one question at a time, until every branch resolves; notes where recorded preferences live. Called directly or from within other skills |
| `/to-docs` | user-selected path | Write the current session's work as a report-style document |
| `/create-agent` | `.claude/agents/*.md` or `.github/agents/*.agent.md` | Grill to design a project-specific subagent wired to existing skills, then write it |
| `/explore` | `.context/explore/{timestamp}-{task-slug}/{question-slug}.md` | Delegate fact-finding to a subagent tiered by question ambiguity (haiku for narrow lookups, sonnet for open-ended reconnaissance, never opus), one dispatch per tier bucket, writing an Answer + Evidence + Open gaps file per question so the calling context reads a complete answer instead of raw search output |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |
| `/experiment` | `questions/{slug}/report.md` (+ `raw/`, optional `gallery/`) | Middle stage of a three-gate pipeline (`/explore` -> `/experiment` -> `/viewpoints`, run separately by hand — see `references/pipeline.md`): reads the question's grilling output from `/goal-init` (re-grills only if missing), frames a hypothesis, then method, execution, then dispatches a sonnet subagent to analyze results and write `result.md` directly, verdict, publish (dispatched to a haiku subagent that assembles `report.md` and updates `goal.md`/README itself). Each stage gates on whether it already resolves the question, so a plain lookup can stop at `/explore` and a clear verdict can skip the `/viewpoints` gallery entirely |
| `/run-n-view` | `run-n-view/{slug}/raw/`, `run-n-view/{slug}/gallery/index.html` | Bare run+view primitive — launch/drive a command, script, or app for real via `run`, then build a `/viewpoints` gallery over the captured output. No hypothesis or report; use `/experiment` when those are needed |
| `/viewpoints` | `gallery/{slug}/index.html` | Build a gallery of complementary chart/diagram views on a dataset or structure instead of picking one form |
| `/to-todo` | inbox `TODO.md` | Turn a completed `/breakdown` tree (external to this repo) into an inbox TODO: objective/background/scope framing, a checkbox body numbered by the breakdown's dotted ids, and a conclusion with critical path and parallel-ready execution order |

### Peon Ping

Session sound-notification utilities, unrelated to the engineering workflow above.

| Skill | What it does |
|-------|--------------|
| `/peon-ping-config` | Update volume, pack rotation, categories, active pack, and other settings |
| `/peon-ping-toggle` | Mute/unmute, pause/resume sounds during a session |
| `/peon-ping-use` | Set the voice pack (character voice) for the current session |
| `/peon-ping-log` | Log exercise reps (pushups, squats, ...) for the Peon Trainer |

## Preferences

Two preference stores keep settled decisions from being re-asked every pass:

- `preferences/{topic}.md` — general engineering/style rules true regardless of which project (e.g. `preferences/api-design.md`). Lives in this skills repo, so it travels with the install.
- `.context/preferences/{topic}.md` — this project's own recorded choices (e.g. `.context/preferences/tech-stack.md`).

Neither is pre-populated — the first standing rule (not a one-off, feature-specific answer) on a topic creates its file, and later ones append to it. Preference files are concise decision ledgers: one direct decision per bullet, no report sections or diagrams. `/grilling` only notes where these files live during an interview; it doesn't read, skip on, or write to them itself. Edit or delete an entry directly if it's wrong; nothing else enforces it.

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
| `good-harness.md` | Turn a natural-language constraint into a local, executable pass/fail check: Layer/Determinism axes, harness-by-shape table, anti-patterns |
| `document-style.md` | Structured-format style, key-value format: priority order (diagram/table > bullets > prose), when to use a flow diagram vs a table, Introduction/Body/Conclusion structure — covers both chat/plans and standalone docs |
| `preference-format.md` | Standing-vs-one-off test, file location (`../../preferences/` vs `.context/preferences/`), and entry format for recorded preferences |
| `requirement-engineering.md` | Elicitation, analysis, specification, validation, management — the five requirement-engineering activities |
| `top-down-decompose.md` | MECE top-down decomposition methodology to split a goal into atomic sub-goals |

## Templates

Auto-discovered by `/grilling`; filled in and written to `.context/` by the workflow skill that needs them.

| Template | Used by |
|----------|---------|
| `plan.md` | — Regular plan format; currently unused (`/p4d` writes `plan/index.md` + `plan/group-{n}.md` directly instead) |
| `review-plan.md` | — Review-Plan format; currently unused (`/co-plan`, its only consumer, was removed) |
| `adr.md` | — Architectural Decision Record format; currently unused (no skill writes it) |
| `architecture.md` | — Architecture document format (Static/Dynamic View); currently unused |
| `requirements.md` | — Requirement Decision Record format; currently unused (no skill writes it) |
