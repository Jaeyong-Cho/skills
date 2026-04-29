---
name: pofe-review
description: |
  End-of-day review for the POFE knowledge base. Reads today.md and today's goal file, writes a structured daily report, marks goal progress, propagates completions to weekly/monthly goals, extracts wiki entries and insights, updates work patterns, archives today.md, seeds tomorrow's goal and today.md with the next plan, and suggests a git commit message.
  Triggers: "end of day", "daily review", "review today", "pofe review", "wrap up today", "end of work", or any request to summarize today's journal and plan tomorrow.
---

# pofe-review: End-of-Day Review

**Goal**: Close the day — assess progress against goals, grow the knowledge base, update achievement archive, analyze work patterns, and hand off a clean starting point for tomorrow.

---

## Step 1: Load today's files

1. Find `today.md` in the repo root. If missing, stop and tell the user.
2. Determine today's date (from the `<!-- today: YYYY-MM-DD -->` comment, or current date).
3. Load `goals/YYYY/goal-MM-DD.md` (today's goal file). If missing, note that no goal was set for today.
4. Load N most recent archived journals from `Journal/` for context (default N=5; override if user specifies).

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

## Step 4: Mark goal progress

Update `goals/YYYY/goal-MM-DD.md`:
- Check off completed tasks: `- [x]`
- Add `*(partial)*` or `*(skipped)*` annotations to incomplete ones

Then propagate upward:
- `goals/YYYY/goal-MM-WNN.md` — check off tasks completed this week (across all daily goals this week)
- `goals/YYYY/goal-MM.md` — same for month

Only mark a weekly/monthly task done if it's fully achieved, not just started.

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
3. Create a fresh `today.md`:

```markdown
<!-- today: YYYY-MM-DD -->
<!-- Write freely below. No format required. -->

## Plan

(paste Next Work Plan tasks here)
```

4. Create `goals/YYYY/goal-MM-DD.md` for tomorrow, pre-populated from the Next Work Plan:

```markdown
# YYYY-MM-DD

> [Monthly](goal-MM.md) · [Weekly](goal-MM-WNN.md)

## Tasks

### (Topic)
- [ ] Task *(High)*
- [ ] Task *(Medium)*

## Adjustment Log
```

Compute the correct weekly file link for tomorrow's date. If tomorrow crosses into a new week, create the new `goal-MM-WNN.md` for that week as well (seeded from the monthly goal's remaining tasks).

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
