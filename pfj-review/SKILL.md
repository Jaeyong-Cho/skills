---
name: pfj-review
description: |
  End-of-day review for POFE knowledge base. Reads today.md, extracts wiki entries, recommends next tasks. Human writes own todo list.
  Triggers: "end of day", "daily review", "review today", "pfj review", "wrap up today", "end of work", or any request to summarize today's journal.
---

# pfj-review: End-of-Day Review

Read journal. Extract knowledge. Surface next steps. Human decides.

**Source of truth:**
- Human-written: `## HH:MM:SS` (no label) or freeform below `<!-- Write freely below -->` → ground truth.
- AI-written: `## HH:MM:SS (label)` → trust facts/outcomes, not voice/reflection.

## Step 1: Load files

Find `today.md` — missing → stop, tell user. Read full journal. Load 3 most recent `Journal/` archives for context.

## Step 2: Load wiki

Infer topics from journal. Scan first 3 lines of each `wiki/` file for tag line. Read only files with matching tags.

## Step 3: Extract wiki entries

Save knowledge worth keeping: non-obvious techniques, tool/API insights, design decisions + reasoning, research findings, recurring workflows. Skip obvious/ephemeral. Update existing, no duplicates.

See [REFERENCE.md](REFERENCE.md#wiki-format) for format. Wiki conflicts journal → fix wiki, add `*Updated: YYYY-MM-DD — reason*`.

## Step 4: Update SUMMARY.md

Add new wiki entries under Wiki section (alphabetical).

## Step 5: Recommend next tasks

Output only — human writes their own list.

```
## Recommended next
- <task> — <why: what it unblocks>
```

High-value only. Keep short.

## Step 6: HTML report

Read `../pfj-grill/kanagawa.css`. Embed verbatim in `<style>` tag.
Save: `$PFJ_PATH/review/YYYY/MM-DD.html`

See [REFERENCE.md](REFERENCE.md#html-report-spec) for diagram rules and required sections.

```
Review saved: $PFJ_PATH/review/YYYY/MM-DD.html
```

## Step 7: Show commit message

Don't commit. Just show:

```
review: YYYY-MM-DD — <one-line summary>

- wiki/slug.md (new/updated)
- review/YYYY/MM-DD.html (generated)
```

## Step 8: Archive today.md

Read date from `<!-- today: YYYY-MM-DD -->`. Copy `today.md` → `Journal/YYYY/MM-DD.md`. Exact copy, no edits.

## Step 9: Reset today.md

Compute tomorrow (today + 1). Find weekly goal path for tomorrow. Carry over only `- [ ]` tasks from `## Goals` — drop `- [x]` and dropped. Keep `###` sections + priority order. Sub-tasks under parent. New week → update weekly link. No Adjustment Log or freeform carry-over.

See [REFERENCE.md](REFERENCE.md#todaymd-reset-template) for template.
