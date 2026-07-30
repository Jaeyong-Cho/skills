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
 |  (create a directory to hold this goal's context)
 v
Question / Hypothesis          e.g. "SQLite vs Postgres: which is
 |                                   reliable enough here?"
 v
/experiment  ------------->  cheapest method that resolves the question
 |                            (builds a /viewpoints gallery over raw results)
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
 ├─ /fs-plan  (full self-plan, full AI implementation)
 └─ /co-plan  (collaborative plan, holes for human implementation)
```

Once `/auto-action` genuinely finishes (regular plan, or a self-plan after every hole passes review), it moves the plan unchanged from `.context/inbox/plan/` to `.context/done/plan/`.

All workflow skills are user-invoked. Artifacts land in `.context/`. All skills work on new development and fixing existing code.

### Implementation Paths

The branch happens at planning, not execution — `/auto-action` always runs, but behaves differently depending on which plan type it finds:

| Path | Test | Working Steps | Holes to Fill |
|------|------|---------------|---------------|
| **/fs-plan → /auto-action** | AI writes | AI writes (100%) | — |
| **/co-plan → /auto-action** | AI writes | AI writes (~70%) | You fill (~30%) |

### Philosophy: least-effort human participation

`/co-plan` + `/auto-action` exist because full automation isn't always the goal — sometimes the point is for the human to actually understand the codebase, not just review a diff of it. The design question was never "how much can AI write?" but "what's the smallest, most load-bearing set of decisions a human must make by hand to genuinely learn this code?"

- **Budget, not vibes.** Holes land near 30% of implementation lines, working code the other ~70% — tallied across the whole plan, not per step. Below that and there's nothing to learn; above it and the human is doing AI's job.
- **Two hole kinds, never a whole function.** A hole is either the line where a stage hands its result to the next stage (flow-connecting), or the one line that embodies a stage's own core decision (key-change) — infrastructure, loops, error handling, and the rest of a stage's algorithm stay working code, written by AI.
- **Guide, don't quiz.** Each hole's TODO names the general technique, breaks it into numbered steps, and gives one worked example with different values than the paired test — enough that a competent human can apply it without guessing the approach from scratch. The effort spent is in application, not archaeology.
- **Read order follows the flow, not the build order.** `/co-plan` emits a Recommended Human Work Order — holed steps reordered top-down (entry point → algorithm) — separate from the Action Sequence's TDD build order, which is often bottom-up. Filling holes should follow the story the code tells, not the order tests happened to be written in.
- **AI closes the loop.** On the re-run, `/auto-action` checks every hole against its recorded intent and runs the tests itself — the human fills the gap once, then AI reports whether it landed. Nobody has to independently re-verify correctness by hand.

## Skills

| Skill | Output | What it does |
|-------|--------|-------------|
| `/fs-plan` | `.context/inbox/plan/` | Sequence a design into ordered TDD implementation steps, then write a regular plan, fully written and executed by AI |
| `/co-plan` | `.context/inbox/plan/` | Sequence a design into ordered TDD steps, and for each implementation step decide — block-by-block — what's a hole (for you to fill) vs working code (AI-written); writes a plan marked `**Type:** Self-Plan` |
| `/auto-action` | code changes, `.context/done/plan/` | Runs an inbox plan. Regular plan: write tests → write code → verify. Self-plan: first write working parts and hole TODOs; then, after the human fills every hole, review and test. Once successful, move the plan from `inbox/` to `done/`. |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grilling` | — | Interview relentlessly about a plan, one question at a time, until every branch resolves; notes where recorded preferences live. Called directly or from within other skills |
| `/to-docs` | user-selected path | Write the current session's work as a report-style document |
| `/create-agent` | `.claude/agents/*.md` or `.github/agents/*.agent.md` | Grill to design a project-specific subagent wired to existing skills, then write it |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |
| `/study-guide` | HTML file | Explain a document or codebase and quiz the reader on it — background, core concepts with worked examples, walkthrough, and a 5-question interactive quiz, rendered via bundled `render.py` |
| `/experiment` | `experiments/{slug}/report.md` (+ `raw/`, `gallery/`) | Turn a request into a scientific-method run — hypothesis, method, execution, analysis, verdict — building a `/viewpoints` gallery over the raw results before writing the report |
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

## Peon Ping (sound notifications)

A separate, unrelated add-on: character-voice sound cues for session events (start, task complete, errors, and more).

| Skill | What it does |
|-------|--------------|
| `/peon-ping-toggle` | Mute/unmute peon-ping sounds (master switch); routes any other config request to `/peon-ping-config` |
| `/peon-ping-config` | Update settings — volume, active/rotating sound packs, category toggles, per-directory pack bindings |
| `/peon-ping-use` | Set the character voice pack for the current session only |
| `/peon-ping-log` | Log pushup/squat reps for the Peon Trainer |

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
| `todo-hole.md` | Wording rule for a self-plan hole's TODO: junior-developer guidance, no line cap — real signature names, the general technique, numbered steps, one worked example with concrete values different from the paired test |
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
| `self-plan.md` | `/co-plan` — written to `.context/inbox/plan/{timestamp}-{slug}.md`, marked `**Type:** Self-Plan`; `/auto-action` moves it to `.context/done/plan/` once every hole is reviewed and tests pass |
| `adr.md` | — Architectural Decision Record format; currently unused (no skill writes it) |
| `architecture.md` | — Architecture document format (Static/Dynamic View); currently unused |
| `requirements.md` | — Requirement Decision Record format; currently unused (no skill writes it) |
