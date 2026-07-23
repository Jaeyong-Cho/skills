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

## Workflow

```
/req  →  /archi  →  (choose planning path)  →  /auto-action
                     ├─ /fs-plan  (full self-plan, full AI implementation)
                     └─ /co-plan  (collaborative plan, holes for human implementation)

/test  →  verify a plan's tests, or discover and run all tests — standalone, any time
```

Once `/auto-action` genuinely finishes (regular plan, or a self-plan after every hole passes review), it folds any inbox RDR/ADR for that slug into `.context/req/{slug}.md`, derives `.context/archi/{slug}.md`, then moves the RDR, ADR, and plan unchanged from `.context/inbox/` to `.context/done/` — no separate merge step to run.

All workflow skills are user-invoked. Artifacts land in `.context/`. All skills work on new development and fixing existing code.

### Implementation Paths

The branch happens at planning, not execution — `/auto-action` always runs, but behaves differently depending on which plan type it finds:

| Path | Test | Working Steps | Holes to Fill |
|------|------|---------------|---------------|
| **/fs-plan → /auto-action** | AI writes | AI writes (100%) | — |
| **/co-plan → /auto-action** | AI writes | AI writes (~70%) | You fill (~30%) |
| **/test** | Runs only | — | — |

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
| `/req` | `.context/inbox/rdr/` | Use `/grilling` to find the goal, elicit and prioritize functional/non-functional requirements, and write a draft Requirement Decision Record |
| `/archi` | `.context/inbox/adr/` | Use `/grilling` to resolve architecture, design, observability, test-loop, and verification criteria against `archi.md`, then write an ADR |
| `/fs-plan` | `.context/inbox/plan/` | Sequence the ADR's design into ordered TDD implementation steps, then write a regular plan, fully written and executed by AI |
| `/co-plan` | `.context/inbox/plan/` | Sequence the ADR's design into ordered TDD steps, and for each implementation step decide — block-by-block — what's a hole (for you to fill) vs working code (AI-written); writes a plan marked `**Type:** Self-Plan` |
| `/auto-action` | code changes, `.context/req/{slug}.md`, `.context/archi/{slug}.md`, `.context/done/` | Runs an inbox plan. Regular plan: write tests → write code → verify. Self-plan: first write working parts and hole TODOs; then, after the human fills every hole, review and test. Once successful, fold the RDR into the committed spec, derive the architecture doc, and move the RDR, ADR, and plan from `inbox/` to `done/`. |
| `/test` | test results | Run tests for a plan or discover and run all tests in the project. Verification only. |

## Utilities

| Skill | Output | What it does |
|-------|--------|-------------|
| `/grilling` | — | Interview relentlessly about a plan, one question at a time, until every branch resolves; notes where recorded preferences live. Called directly or from within other skills |
| `/to-preference` | `../../preferences/`, `.context/preferences/` | Sweep the whole session for confirmed decisions or corrections that generalize beyond it, and record the approved ones as standing preferences |
| `/to-todo` | `.context/inbox/todo/` | Turn the current `/breakdown` tree into a checkbox TODO; manually move the file unchanged to `.context/done/todo/` after every item is checked |
| `/to-docs` | user-selected path | Write the current session's work as a report-style document |
| `/create-agent` | `.claude/agents/*.md` or `.github/agents/*.agent.md` | Grill to design a project-specific subagent wired to existing skills, then write it |
| `writing-great-skills` | — | Reference for writing and editing skills well; read directly when authoring a skill, not invoked via workflow |
| `/breakdown` | — | Break any goal into a MECE tree of atomic, actionable sub-goals, then order the leaves into a dependency-respecting execution sequence |
| `/study-guide` | HTML file | Explain a document or codebase and quiz the reader on it — background, core concepts with worked examples, walkthrough, and a 5-question interactive quiz, rendered via bundled `render.py` |

## Preferences

`/to-preference` grows two preference stores instead of re-asking the same settled question every pass:

- `preferences/{topic}.md` — general engineering/style rules true regardless of which project (e.g. `preferences/api-design.md`). Lives in this skills repo, so it travels with the install.
- `.context/preferences/{topic}.md` — this project's own recorded choices (e.g. `.context/preferences/tech-stack.md`).

Neither is pre-populated — the first standing rule (not a one-off, feature-specific answer) on a topic creates its file, and later ones append to it. Preference files are concise decision ledgers: one direct decision per bullet, no report sections or diagrams. `/to-preference` sweeps a whole session and asks for confirmation before writing. `/grilling` only notes where these files live during an interview; it doesn't read, skip on, or write to them itself. Edit or delete an entry directly if it's wrong; nothing else enforces it.

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
| `preference-format.md` | Standing-vs-one-off test, file location (`../../preferences/` vs `.context/preferences/`), and entry format for recorded preferences — used by `/to-preference` |
| `requirement-engineering.md` | Elicitation, analysis, specification, validation, management — the five activities `/req` draws on |
| `top-down-decompose.md` | MECE top-down decomposition methodology `/breakdown` applies to split a goal into atomic sub-goals |

## Templates

Auto-discovered by `/grilling`; filled in and written to `.context/` by the workflow skill that needs them.

| Template | Used by |
|----------|---------|
| `adr.md` | `/archi` — written to `.context/inbox/adr/{timestamp}-{slug}.md`; `/auto-action` moves it to `.context/done/adr/` after successful implementation |
| `architecture.md` | `/auto-action` — derived from the completed ADR and implemented code, written directly to `.context/archi/{slug}.md` |
| `plan.md` | `/fs-plan` — written to `.context/inbox/plan/{timestamp}-{slug}.md`, pairs with an ADR of the same slug; `/auto-action` moves it to `.context/done/plan/` on completion |
| `self-plan.md` | `/co-plan` — written to `.context/inbox/plan/{timestamp}-{slug}.md`, marked `**Type:** Self-Plan`, pairs with an ADR of the same slug; `/auto-action` moves it to `.context/done/plan/` once every hole is reviewed and tests pass |
| `requirements.md` | `/req` — written to `.context/inbox/rdr/{timestamp}-{slug}.md`; `/auto-action` folds it into `.context/req/{slug}.md` then moves it to `.context/done/rdr/` |
