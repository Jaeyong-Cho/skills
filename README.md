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
/goal-init                   creates `.context/`, and (re)builds the
 |                            experiments dashboard (experiments/index.html)
 v
Question / Hypothesis          e.g. "SQLite vs Postgres: which is
 |                                   reliable enough here?"
 v
/experiment  ------------->  cheapest method that resolves the question
 |                            (builds a /viewpoints gallery over raw results,
 |                             refreshes the experiments dashboard on exit)
 v
Ideas                        read the gallery/report, generate options
 |
 v
Direction                    pick how the goal will be resolved
 |
 v
/spec   (Goal -> SCN -> REQ -> CMP -> SEQ)
 |
 v
/fs-plan or /co-plan  ->  /auto-action     implement
 |
 v
/experiment                  re-test the implementation against the
 |                            original hypothesis
 v
Goal closed
```

- **Cheapest method first.** When requesting `/experiment`, the point is picking the cheapest way to resolve the question — a spike, a small script, existing data — not a full build. See `/experiment` in the Skills table below.
- **Ideas -> Direction -> Spec.** The direction decided from the experiment's ideas is the "goal" that `/spec`'s `to_scen` stage consumes; see Spec Pipeline below.
- **Same skill opens and closes the loop.** `/experiment` both answers the upfront hypothesis and, later, verifies the implementation actually resolved it — no separate test-writing step is needed for that check.

## Workflow

```
(choose planning path)  →  /auto-action
 ├─ /fs-plan  (regular plan, full AI implementation)
 └─ /co-plan  (review plan, full AI implementation + a Review Sequence for the human)
```

Once `/auto-action` genuinely finishes (regular plan, or a review-plan after the human confirms every Review Sequence entry), it moves the plan unchanged from `.context/inbox/plan/` to `.context/done/plan/`.

All workflow skills are user-invoked. Artifacts land in `.context/`. All skills work on new development and fixing existing code.

### Implementation Paths

The branch happens at planning, not execution — `/auto-action` always runs, but behaves differently depending on which plan type it finds:

| Path | Test | Implementation | Closeout |
|------|------|-----------------|----------|
| **/fs-plan → /auto-action** | AI writes | AI writes (100%) | Test |
| **/co-plan → /auto-action** | AI writes | AI writes (100%) | Test + you confirm the Review Sequence |

### Philosophy: review by tracing the flow, not by guessing at a diff

`/co-plan` + `/auto-action` exist because full automation isn't always the goal — sometimes the point is for the human to actually understand the codebase, not just skim a diff of it. AI writes the entire implementation, same as `/fs-plan`; what `/co-plan` adds is a **Review Sequence**: the same steps, reordered along the code's real data flow so a human can trace input → output through the finished code instead of reviewing files in whatever order they happened to change.

- **No holes.** Every implementation step is complete, working code — `/auto-action` writes and tests the whole sequence in one pass, exactly like a regular plan.
- **Read order follows the flow, not the build order.** `/co-plan` emits a Review Sequence — every step reordered top-down (entry point → algorithm) — separate from the Action Sequence's TDD build order, which is often bottom-up. Reviewing should follow the story the code tells, not the order tests happened to be written in.
- **Each entry names a concrete thing to verify.** Not "read this file," but the specific behavior to confirm at that stage (e.g., "the cache is checked before the DB call and its result short-circuits the DB path").
- **The human closes the loop.** Since there's no syntactic marker left behind (no holes, no TODOs), `/auto-action` can't detect review completion from the code — it asks the human to confirm each Review Sequence entry on the next run, then marks Closeout and moves the plan to `done/`.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/goal-init` | `goal.md`, `experiments/index.html` | Bootstrap a new goal — write the goal statement to project-root `goal.md`, and build/refresh a dashboard linking every experiment's report and viewpoint gallery |
| `/workflow` | one plan in `.context/done/plan/`, code changes | Grill the goal, then run `/explore` once for both the grilled intent (one haiku-tier question) and any codebase facts the plan needs, straight into `/fs-plan` as the design (no `/spec` stage, no SCN/REQ/CMP/SEQ docs, no Review Sequence), then dispatch a subagent to run `/auto-action`'s Full Execution pass (haiku model), then visualize the result with `/viewpoints` as the review step |
| `/fs-plan` | `.context/inbox/plan/` | Sequence a design into ordered TDD implementation steps, then write a regular plan, fully written and executed by AI |
| `/co-plan` | `.context/inbox/plan/` | Sequence a design into ordered TDD steps, fully written by AI like `/fs-plan`, then derive a Review Sequence — the same steps reordered along the code's flow (entry point → algorithm) — so a human can review the finished code in that order; writes a plan marked `**Type:** Review-Plan` |
| `/auto-action` | code changes, `.context/done/plan/` | Runs an inbox plan. Regular plan: write tests → write code → verify. Review-plan: first write and test the whole sequence; then, once the human confirms every Review Sequence entry against the finished code, mark Closeout. Once successful, move the plan from `inbox/` to `done/`. |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grilling` | — | Interview relentlessly about a plan, one question at a time, until every branch resolves; notes where recorded preferences live. Called directly or from within other skills |
| `/to-docs` | user-selected path | Write the current session's work as a report-style document |
| `/create-agent` | `.claude/agents/*.md` or `.github/agents/*.agent.md` | Grill to design a project-specific subagent wired to existing skills, then write it |
| `/explore` | `.context/explore/{timestamp}-{task-slug}/{question-slug}.md` | Delegate fact-finding to a subagent tiered by question ambiguity (haiku for narrow lookups, sonnet for open-ended reconnaissance, never opus), one dispatch per tier bucket, writing an Answer + Evidence + Open gaps file per question so the calling context reads a complete answer instead of raw search output |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |
| `/study-guide` | HTML file | Explain a document or codebase and quiz the reader on it — background, core concepts with worked examples, walkthrough, and a 5-question interactive quiz, rendered via bundled `render.py` |
| `/experiment` | `experiments/{slug}/report.md` (+ `raw/`, `gallery/`) | Turn a request into a scientific-method run — grill the user's real intent/question (folded into `/explore` as one haiku-tier question), frame a hypothesis, then method, execution, analysis, verdict — routing a research-shaped method through `/explore` for its raw results, building a `/viewpoints` gallery over them before writing the report |
| `/run-n-view` | `run-n-view/{slug}/raw/`, `run-n-view/{slug}/gallery/index.html` | Bare run+view primitive — launch/drive a command, script, or app for real via `run`, then build a `/viewpoints` gallery over the captured output. No hypothesis or report; use `/experiment` when those are needed |
| `/viewpoints` | `gallery/{slug}/index.html` | Build a gallery of complementary chart/diagram views on a dataset or structure instead of picking one form |
| `/scaffold-skeleton-code` | skeleton file + test file | Generate function signatures, TODO hints, and a matching test file so the user implements just the logic |

## Spec Pipeline

`/spec` advances one stage of a separate documentation pipeline, or records a decision. Each stage reads the artifact above it and writes filled-in docs below.

```
Goal --to_scen--> SCN --to_req--> REQ --to_cmp--> CMP --to_seq--> SEQ
                                   |                |     ^_________|
                                   |                |   (to_seq reads REQ + CMP)
                            to_rdr |         to_adr |
                                   v                v
                                  RDR              ADR
```

| Arg | Reads | Writes |
|-----|-------|--------|
| `to_scen` | a goal | `spec/scen/SCN-*.md` |
| `to_req` | SCN docs | `spec/req/REQ-*.md` |
| `to_cmp` | REQ docs | `spec/cmp/CMP-*.md` |
| `to_seq` | REQ + CMP docs | `spec/seq/SEQ-*.md` |
| `to_rdr` | REQ docs | `spec/rdr/RDR-*.md` |
| `to_adr` | CMP + SEQ docs | `spec/adr/ADR-*.md` |

`to_rdr` and `to_adr` run as needed, recording the decisions taken while shaping REQ and CMP.

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
| `document-style.md` | Structured-format report style for written docs: priority order (diagram/table > bullets > prose), when to use a flow diagram vs a table, Introduction/Body/Conclusion structure |
| `communication-style.md` | Same structured-format priority, scoped to chat responses, plans, and `AskUserQuestion` calls rather than standalone docs |
| `preference-format.md` | Standing-vs-one-off test, file location (`../../preferences/` vs `.context/preferences/`), and entry format for recorded preferences |
| `requirement-engineering.md` | Elicitation, analysis, specification, validation, management — the five requirement-engineering activities |
| `top-down-decompose.md` | MECE top-down decomposition methodology to split a goal into atomic sub-goals |

## Templates

Auto-discovered by `/grilling`; filled in and written to `.context/` by the workflow skill that needs them.

| Template | Used by |
|----------|---------|
| `plan.md` | `/fs-plan` — written to `.context/inbox/plan/{timestamp}-{slug}.md`; `/auto-action` moves it to `.context/done/plan/` on completion |
| `review-plan.md` | `/co-plan` — written to `.context/inbox/plan/{timestamp}-{slug}.md`, marked `**Type:** Review-Plan`; `/auto-action` moves it to `.context/done/plan/` once tests pass and the human confirms every Review Sequence entry |
| `adr.md` | — Architectural Decision Record format; currently unused (no skill writes it) |
| `architecture.md` | — Architecture document format (Static/Dynamic View); currently unused |
| `requirements.md` | — Requirement Decision Record format; currently unused (no skill writes it) |
