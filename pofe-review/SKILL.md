---
name: pofe-review
description: |
  End-of-day review for the POFE knowledge base. Reads today.md and today's goal file, writes a structured daily report, marks goal progress, propagates completions to weekly/monthly goals, extracts wiki entries and insights, updates work patterns, archives today.md, seeds tomorrow's goal and today.md with the next plan, and suggests a git commit message.
  Triggers: "end of day", "daily review", "review today", "pofe review", "wrap up today", "end of work", or any request to summarize today's journal and plan tomorrow.
---

# pofe-review: End-of-Day Review

**Goal**: Close the day — assess progress against the full goal hierarchy, adjust goals based on what was learned, grow the knowledge base, update achievement archive, analyze work patterns, and hand off a clean starting point for tomorrow.

---

## Step 1: Load today's files and full goal hierarchy

1. Find `today.md` in the repo root. If missing, stop and tell the user.
2. Determine today's date (from the `<!-- today: YYYY-MM-DD -->` comment, or current date).
3. Read the daily goals from the `## Goals` section at the top of `today.md` — this is the daily goal, not a separate file.
4. Load the **persistent goal hierarchy**:
   - `goals/goal.md` (total/lifetime)
   - `goals/YYYY/goal.md` (yearly)
   - `goals/YYYY/goal-MM.md` (monthly)
   - `goals/YYYY/goal-MM-WNN.md` (weekly)
5. Load N most recent archived journals from `Journal/` for context (default N=5; override if user specifies).

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
| ... | ... | ✅ done / 🔄 partial / ❌ skipped | ... |

### Related Knowledge
- [title](../wiki/slug.md) — why relevant

### Knowledge Saved
- [title](../wiki/slug.md) — one-line summary

### Next Work Plan

#### (Topic)
- [ ] Task *(High)*
- [ ] Task *(Medium)*

#### (Topic)
- [ ] Task *(High)*
```

Fill every section with real content. The Next Work Plan should be specific enough to start tomorrow without re-reading anything — infer from unfinished tasks, open questions, and logical next steps.

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

### 4c — Adjust goals based on journal insights

Read `today.md` and the recent journals carefully. The journal often reveals things that should change higher-level goals — act on them. When deciding which level to update, respect each level's scope:

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

## Step 6: Update work patterns

Read `patterns.md`. Based on today's journal and goal file:

1. Identify the work category (e.g., `debugging`, `research`, `implementation`, `reading`, `writing`, `review`, `meeting`, `devops`). Infer from content — a day spent fixing bugs is `debugging`, reading papers is `research`, etc. Multiple categories are fine.
2. Increment the count for each matched category in the frequency table.
3. If a pattern or automation opportunity becomes apparent (e.g., debugging has been the top category for 5+ days), add an entry under Automation Opportunities or Insights.
4. Update the `Last updated` date.

---

## Step 7: Update achievement archive

Append today's achievements to the archive files:

**archive/YYYY/archive-MM-WNN.md** — append under `## Achievements`:
```markdown
- YYYY-MM-DD — brief summary of what was accomplished `#tag`
```

**archive/YYYY/archive-MM.md** — same format.

If the weekly or monthly goal was completed today, update the Goal Completion table in the respective archive file.

**Archive file format** (for reference when creating new files):
```markdown
# Archive · YYYY-MM (or WNN or YYYY)

## Achievements
- YYYY-MM-DD — summary `#tag`

## Goal Completion
| Goal | Status | Notes |
|------|--------|-------|
| ... | ✅ / 🔄 / ❌ | ... |

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

```markdown
<!-- today: YYYY-MM-DD -->

## Goals

> [Weekly](goals/YYYY/goal-MM-WNN.md) · [Monthly](goals/YYYY/goal-MM.md)

### (Topic)
- [ ] Specific action *(High)* — why this completes/advances the weekly deliverable *(→ Weekly: deliverable name)*
- [ ] Specific action *(Medium)* — rationale *(→ Weekly: deliverable name)*

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
