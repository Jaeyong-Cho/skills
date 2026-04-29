---
name: pofe-review
description: |
  End-of-day review for the POFE knowledge base. Reads today.md and today's goal file, writes a structured daily report, marks goal progress, propagates completions to weekly/monthly goals, extracts wiki entries and insights, updates work statistics, archives today.md, seeds tomorrow's goal and today.md with the next plan, and suggests a git commit message.
  Triggers: "end of day", "daily review", "review today", "pofe review", "wrap up today", "end of work", or any request to summarize today's journal and plan tomorrow.
---

# pofe-review: End-of-Day Review

**Goal**: Close the day — assess progress against the full goal hierarchy, adjust goals based on what was learned, grow the knowledge base, update achievement archive, analyze work patterns, and hand off a clean starting point for tomorrow.

---

## Source of Truth

**The human's journal text is always correct. Everything else is an AI inference that may be wrong.**

When the journal conflicts with a goal file, wiki entry, archive, or report — the journal wins. Correct the other file, not the journal. Specifically:

- If the journal describes work that contradicts a goal's stated direction → update the goal to match reality.
- If the journal says a task is done but the goal file says it isn't (or vice versa) → trust the journal.
- If the journal reveals that a wiki entry contains an error or outdated information → correct the wiki entry.
- If the journal describes a different scope, priority, or outcome than what the goal files assumed → update the goal files.
- Never silently ignore a mismatch. Either fix it or leave a note explaining the discrepancy.

---

## Step 1: Load today's files and full goal hierarchy

1. Find `today.md` in the repo root. If missing, stop and tell the user.
2. Determine today's date (from the `<!-- today: YYYY-MM-DD -->` comment, or current date).
3. Read the daily goals from the `## Goals` section at the top of `today.md`.
4. Load N most recent archived journals from `Journal/` for context (default N=5; override if user specifies).
5. Load the **persistent goal hierarchy** — check each file:
   - `goals/goal.md` (total/lifetime)
   - `goals/YYYY/goal.md` (yearly)
   - `goals/YYYY/goal-MM.md` (monthly)
   - `goals/YYYY/goal-MM-WNN.md` (weekly)

   **If any file is missing or empty**, do not stop — proceed to Step 1b.

---

## Step 1b: Bootstrap missing goal files from journal

For each goal file that is missing or empty, infer its content from `today.md` and the recent journals. Read the work done, topics covered, and direction implied — then create the file with content appropriate to its scope:

- **Total (`goals/goal.md`)**: Infer the user's overarching long-term direction. Write 1–3 abstract goal titles with an **Effect** line each. These should capture the ultimate "why" behind all the work observed in the journal.
- **Yearly (`goals/YYYY/goal.md`)**: Infer major milestones the user is working toward this year. Each milestone should state what success looks like by year end and why it advances a total goal. Include `*(→ Total: goal title)*` reference.
- **Monthly (`goals/YYYY/goal-MM.md`)**: Infer concrete objectives for this month from the journal. Each task should explain why it advances the yearly milestone. Include `*(→ Yearly: milestone name)*` reference.
- **Weekly (`goals/YYYY/goal-MM-WNN.md`)**: Infer specific deliverables for this week. Each task should explain why it serves the monthly objective. Include `*(→ Monthly: objective name)*` reference.

If a file already exists and has content, load it normally — do not overwrite. Updates to existing goals happen in Step 4c.

After creating any missing files, also create the corresponding empty archive files if they don't exist:
- `archive/YYYY/archive-MM.md`
- `archive/YYYY/archive-MM-WNN.md`

Reading the full hierarchy is essential — the next-day plan and goal adjustments must stay aligned with the bigger picture, not just today's leftover tasks.

---

## Step 2: Load related wiki entries

Infer key topics/tags from today's journal and goal file. Scan the first 3 lines of each file in `wiki/` to find the tag line. Fully read only the files whose tags overlap with today's topics. This keeps context lean as the wiki grows.

---

## Step 3: Write the Daily Report

Append to the end of `today.md`. Do not modify anything above. If a `## Daily Report` section already exists, overwrite it rather than appending a second one.

```markdown
---

## Daily Report · YYYY-MM-DD

### Achievements
- ...

### Goal Progress
| Task | Topic | Status | Notes |
|------|-------|--------|-------|
| ... | ... | done / partial / skipped | ... |

### Related Knowledge
- [title](../wiki/slug.md) — why relevant

### Knowledge Saved
- [title](../wiki/slug.md) — one-line summary

### Next Work Plan

> Trigger first (background):
> - Task name — estimated duration; start immediately so it runs while other work proceeds

#### (Topic)
- [ ] Task *(High)*
  - [ ] Sub-step one
  - [ ] Sub-step two
- [ ] Task *(Medium)*
  - [ ] Sub-step one

#### (Topic)
- [ ] Task *(High)*
```

Fill every section with real content. The Next Work Plan should be specific enough to start tomorrow without re-reading anything — infer from unfinished tasks, open questions, and logical next steps.

**Sub-tasks**: Break each task into 1-level sub-steps (indented `  - [ ]`). Sub-steps are concrete, sequential actions that make the task executable without further thought. Aim for 2–4 sub-steps per task; omit sub-steps only if the task is already a single atomic action.

**Background task identification**: Before listing topics, scan tomorrow's tasks for anything that runs independently and takes significant time (tests, builds, downloads, training runs, long scripts). List these under `> Trigger first (background):` so they get started at the beginning of the day and run in parallel with other work. Omit this block if no background tasks exist.

---

## Step 4: Update and adjust the full goal hierarchy

### 4a — Mark today's goal progress
Update the `## Goals` section in `today.md` (in place, before archiving):
- Check off completed tasks: `- [x]`
- Add `*(partial)*` or `*(skipped)*` annotations to incomplete ones

### 4b — Propagate completions upward
- `goals/YYYY/goal-MM-WNN.md` — check off tasks completed this week
- `goals/YYYY/goal-MM.md` — same for month
- `goals/YYYY/goal.md` — same for year

Only mark a higher-level task done if fully achieved, not just started.

### 4c — Reconcile and adjust goals based on journal

**First, reconcile**: compare the journal with each loaded goal file. Look for mismatches — tasks marked in the wrong state, goals that describe a direction the journal contradicts, scope that no longer reflects what is actually being worked on. Fix every mismatch in favor of the journal. Log each correction in the Adjustment Log with `*(reconciled: reason)*`.

Then adjust for new insights. Read `today.md` and the recent journals carefully. The journal often reveals things that should change higher-level goals — act on them. When deciding which level to update, respect each level's scope:

| Level | Scope | Contains |
|-------|-------|----------|
| Total (`goal.md`) | Lifetime direction | Abstract goal titles + Effect (impact). Never tasks. |
| Yearly | Major milestones | Outcomes for the year. Update only if direction fundamentally changes. |
| Monthly | Concrete objectives | Measurable goals for the month. Update when scope or priorities shift. |
| Weekly | Specific deliverables | Tasks completable in 1–3 days. Update freely based on weekly progress. |
| Daily (today.md) | Actionable steps | Single concrete actions executable today. Generated fresh each day. |

**Scope violations to avoid**: don't add vague milestones to the weekly goal, don't add single-day tasks to the monthly goal, don't add "Effect" language to weekly/daily.

Adjustments to make:
- **New objective discovered** → add at the right level. If it spans multiple months → yearly. If it's this month's work → monthly. If it's this week → weekly.
- **Goal no longer relevant** → mark `*(dropped: reason)*` at its level
- **Task too large** → split into sub-tasks one level down (monthly task → weekly deliverables)
- **Priority shift** → reorder within topic section at the appropriate level
- **Blocked** → add `*(blocked: reason)*` at weekly or monthly level

After adjusting, write a brief **Goal Adjustment Log** entry at the bottom of each modified goal file:
```markdown
## Adjustment Log
- YYYY-MM-DD — <what changed> — <why, inferred from journal>
```

---

## Step 5: Extract and save wiki entries

Identify knowledge worth preserving — good candidates:

- A technique, pattern, or approach that solved a non-obvious problem
- A tool, library, or API insight that took real effort to figure out
- A design decision and the reasoning behind it
- A research finding, mental model, or concept that clarified something
- A recurring workflow or setup step worth referencing again
- An insight — an observation, hypothesis, or "aha" moment, even if tentative

Skip obvious or ephemeral things. Check filenames and tag-matched files already loaded before creating a new entry.

**Reconcile existing entries**: if a loaded wiki entry conflicts with what the journal says — wrong technique, outdated approach, incorrect conclusion — correct the wiki entry to match the journal. Note the correction with `*Updated: YYYY-MM-DD — reason*` at the bottom of the entry.

**Wiki entry format** (`wiki/<slug>.md`):
```markdown
# Title

#tag1 #tag2 #tag3

Clear explanation for your future self.

## Details

Code snippets, diagrams, examples.
Use mermaid blocks when a visual genuinely helps.

---
*First noted: YYYY-MM-DD*
```

Tag guidelines:
- Use specific reusable tags: `#rust`, `#debugging`, `#ml`, `#architecture`, `#research`, `#devops`, `#insight`
- Use `#insight` for observations and hypotheses
- 2–5 tags per entry; prefer existing tags over new ones

Update existing entries rather than creating duplicates — add new learnings in a sub-section and update the date footer.

---

## Step 6: Update work statistics

Read `stats.md`. Based on today's journal:

**1. Classify today's work into types.**

Standard types — use these before inventing new ones:

| Type | What counts |
|------|-------------|
| `research` | reading papers, exploring new tools/techniques, literature review |
| `implementation` | writing new code, building features |
| `debugging` | fixing bugs, diagnosing failures, investigating unexpected behavior |
| `experiment` | running trials, training models, evaluating results |
| `writing` | documentation, reports, notes, planning docs |
| `review` | code review, reading others' code, PR feedback |
| `devops` | CI/CD, infra, deployment, environment setup |
| `meeting` | sync, discussion, pair work |
| `reading` | books, articles, non-paper content |

A day may have multiple types. Assign each type that had meaningful time today.

**2. Estimate hours per type.**

Scan the journal for explicit time mentions (`"spent 2h"`, `"all morning"`, `"quick 30 min"`). Use those directly. For types with no explicit mention, estimate proportionally: divide the working day (assume ~6h if no total is mentioned) across the types based on how much journal content describes each.

Round to the nearest 0.5h. Record `~` prefix when estimated (e.g., `~2.0`).

**3. Update the four stats files.**

Stats live in separate files mirroring the goal hierarchy:

| File | Scope |
|------|-------|
| `stats/stats.md` | All-time totals + Insights + Automation Candidates |
| `stats/YYYY/stats.md` | Yearly totals |
| `stats/YYYY/stats-MM.md` | Monthly totals |
| `stats/YYYY/stats-MM-WNN.md` | Weekly totals |

For each of the four files, for each type active today:
- Increment `Sessions` by 1
- Add today's hours to `Est. Hours`
- Update `Last Active` to today's date (all-time file only)
- Create a new row if the type doesn't exist yet
- Keep rows sorted by `Est. Hours` descending

**New period**: if the current week, month, or year file doesn't exist yet, create it from the seed format before writing. Never modify a past period's file.

**4. Update Insights.**

Rewrite the `## Insights` section using all four period levels:
- **All time**: most time-consuming type; most frequent type; effectiveness ratio (high-value vs overhead — flag if overhead > 30%)
- **Trend**: compare the current week's top type against last week's (or current month vs last month) — note any shift in focus
- Any notable ratio across periods (e.g., "this week is 80% experiment vs monthly avg of 50%")

Overwrite the previous Insights — it should always reflect the current totals, not accumulate stale notes.

**5. Update Automation Candidates.**

Rewrite the `## Automation Candidates` section. For each type where the data suggests time or attention is being spent on repetitive, low-value, or scriptable work, write one bullet:

```
- TypeName (Xh, N sessions) — what specifically could be automated or made faster — concrete suggestion
```

Use these heuristics to identify candidates:

| Signal | What it suggests |
|--------|-----------------|
| `devops` with many sessions and low hours each | repetitive manual setup steps → write scripts or use a Makefile |
| `debugging` with high total hours | insufficient logging or test coverage → add structured logs, increase test coverage |
| `review` with many sessions | checklist-driven work → automate with linters, formatters, or review templates |
| `experiment` with many sessions | manual trial setup → parameterize and script experiment runs |
| `writing` with many sessions | recurring doc patterns → create templates |
| `meeting` with high hours relative to implementation | scheduling overhead or lack of async → consider async updates |
| any type where hours/session is low but sessions are high | frequent context-switching → batch similar work into blocks |

Only include types where the data actually supports the signal. Skip types with fewer than 3 sessions — not enough data. If no candidates exist yet, write `_Not enough data yet._`.

**6. Update the `Last updated` date in each file.**

**stats/stats.md**:
```markdown
# Stats · All Time

| Type | Sessions | Est. Hours | Last Active |
|------|----------|------------|-------------|
| experiment | 14 | 42.0 | 2026-04-30 |
| research | 20 | 38.5 | 2026-04-29 |
| implementation | 10 | 18.0 | 2026-04-28 |
| debugging | 8 | 12.0 | 2026-04-27 |
| devops | 6 | 4.5 | 2026-04-25 |

## Insights

- Most hours: experiment (42h, ~3h/session avg); most frequent: research (20 sessions)
- Effectiveness: 85% high-value; this week → experiment dominant, research sessions dropped vs last week
- This month: debugging high (4 sessions) — may indicate unstable experiment pipeline

## Automation Candidates

- devops (4.5h, 6 sessions, ~0.75h each) — frequent short setup tasks → write a Makefile or setup script
- debugging (12h, 8 sessions) — high total hours → add structured logging and expand test coverage

*Last updated: 2026-04-30*
```

**stats/2026/stats.md**:
```markdown
# Stats · 2026

| Type | Sessions | Est. Hours |
|------|----------|------------|
| experiment | 14 | 42.0 |
| research | 20 | 38.5 |
| implementation | 10 | 18.0 |

*Last updated: 2026-04-30*
```

**stats/2026/stats-04.md**:
```markdown
# Stats · 2026-04

| Type | Sessions | Est. Hours |
|------|----------|------------|
| experiment | 8 | 24.0 |
| research | 7 | 14.0 |
| debugging | 4 | 6.5 |

*Last updated: 2026-04-30*
```

**stats/2026/stats-04-W18.md**:
```markdown
# Stats · 2026 W18 · Apr 28 – May 4

| Type | Sessions | Est. Hours |
|------|----------|------------|
| experiment | 3 | 9.0 |
| research | 2 | 4.0 |

*Last updated: 2026-04-30*
```

---

## Step 7: Update achievement archive

Append today's achievements to the archive files. Each entry must explain **why the achievement is meaningful** for the final goal — not just what was done, but what it moves forward.

**archive/YYYY/archive-MM-WNN.md** — append under `## Achievements`:
```markdown
- YYYY-MM-DD — what was accomplished — why this matters for the final goal `#tag` *(→ Total: goal title)*
```

**archive/YYYY/archive-MM.md** — same format.

If the weekly or monthly goal was completed today, update the Goal Completion table in the respective archive file.

**Archive file format** (for reference when creating new files):
```markdown
# Archive · YYYY-MM (or WNN or YYYY)

## Achievements
- YYYY-MM-DD — what was accomplished — why it matters `#tag` *(→ Total: goal title)*

## Goal Completion
| Goal | Status | Notes |
|------|--------|-------|
| ... | done / partial / skipped | ... |

## Patterns Observed
- ...
```

---

## Step 8: Archive today.md and seed tomorrow

1. Create `Journal/YYYY/` if needed.
2. Move `today.md` → `Journal/YYYY/MM-DD.md`.
3. Create a fresh `today.md` with tomorrow's daily goals at the top, seeded from the full hierarchy:
   - Start with uncompleted High tasks from the weekly goal not yet done
   - Add carried-over tasks from today (partial or skipped)
   - Pull in monthly goal tasks due this week
   - Respect topic structure and high→medium→low order
   - **Each task must include a rationale** — one phrase explaining why this action matters and which weekly deliverable it advances. Carry rationale forward from the weekly goal when available; write new rationale when breaking a task down further.
   - **Background tasks**: mark any long-running independent task with `*(bg)*` and place it first within its topic. Also list it under `> Trigger first` at the top of Goals so it gets started immediately.
   - **AI leverage**: for each task, consider whether AI assistance would meaningfully accelerate it. If yes, add `*(ai)*` after the priority annotation and append a brief note on how — e.g., `*(ai: draft the lit review section)*`, `*(ai: generate boilerplate, you review)*`, `*(ai: suggest debugging hypotheses)*`. Only add `*(ai)*` where it genuinely saves time; skip for tasks that require your own judgment or domain knowledge exclusively.

```markdown
<!-- today: YYYY-MM-DD -->

## Goals

> [Weekly](goals/YYYY/goal-MM-WNN.md) · [Monthly](goals/YYYY/goal-MM.md)

> Trigger first (background):
> - Task name *(~Xh)* — start now; runs while other work proceeds

### (Topic)
- [ ] Long-running task *(High)* *(bg)* — rationale *(→ Weekly: deliverable name)*
  - [ ] Sub-step one
- [ ] Specific action *(High)* *(ai: how AI helps here)* — why this completes/advances the weekly deliverable *(→ Weekly: deliverable name)*
  - [ ] Sub-step one
  - [ ] Sub-step two
- [ ] Specific action *(Medium)* — rationale *(→ Weekly: deliverable name)*
  - [ ] Sub-step one

## Adjustment Log

---

<!-- Write freely below. No format required. -->

```

If tomorrow crosses into a new week, also create `goals/YYYY/goal-MM-WNN.md` for that week, seeded from the monthly goal's remaining tasks and the yearly goal's priorities for this period.

---

## Step 9: Update SUMMARY.md

- Add archived journal: `- [YYYY-MM-DD](Journal/YYYY/MM-DD.md)` under Journal, descending order.
- Add new wiki entries under Wiki, alphabetically.

---

## Step 10: Show the commit message

Do **not** commit — just show:

```
pofe: YYYY-MM-DD — <one-line summary of today's main work>

- wiki/slug.md (new/updated)
```

---

## Notes

- Never modify the original diary text in today.md — only append the report section.
- For research days with no code: plan should reference papers, experiments, analysis — not code tasks.
- After a vacation gap, the skill still works — it uses the last N archived journals regardless of date gap.
- Mermaid diagrams in wiki entries should add real clarity, not decoration.
