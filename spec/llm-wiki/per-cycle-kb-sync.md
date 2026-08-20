---
type: Spec Story
title: per-cycle kb sync
description: KB context compounds within a single day, not just across days — later /do-plan cycles see earlier same-day cycle findings.
tags: [spec, llm-wiki]
timestamp: 2026-08-20T00:00:00Z
---

# Per-cycle kb sync

## Value to user

KB context compounds within a single day, not just across days. Before this story, each `/do-plan` cycle had to wait until `/end-of-day` to see the KB updated — a same-day later cycle couldn't build on an earlier cycle's synthesized page. Now `/do-plan` updates `~/wiki/kb/` directly on every cycle (via `kb-ingest`'s new per-cycle mode), so later cycles can find and extend what earlier cycles already recorded. Combined with the search-first instruction becoming imperative (not descriptive), this enforces the workflow without friction.

## Completion criteria

- `kb-ingest` accepts both `/kb-ingest [YYYY-MM-DD]` (whole-day mode) and `/kb-ingest {plan-file} {report-file}` (per-cycle mode), byte-for-byte backward-compatible in whole-day mode.
- `do-plan` calls `kb-ingest` unconditionally in per-cycle mode every cycle (step 6), removing the old standalone sync step.
- `CLAUDE.md`'s search-first instruction is imperative ("run qmd query first"), not descriptive ("are indexed by qmd").

## Spec

Extend `kb-ingest` with a second input mode for per-cycle invocation (mirroring `project-wiki`'s own input pattern). Wire it into `do-plan` unconditionally as step 6 (no Target project gate, since kb is global), removing the old step 6 ("Refresh search index") entirely. Reword CLAUDE.md's search bullet from descriptive to imperative.

### kb-ingest changes

**Step 1 ("Get the target source")** — two invocation modes:
- *Whole-day mode*: if called with date argument `/kb-ingest YYYY-MM-DD`, use that; otherwise use `bash ../end-of-day/scripts/archive_today.sh --date`. Set a date in `YYYY-MM-DD` format.
- *Per-cycle mode*: if called with `/kb-ingest {plan-file} {report-file}`, those are the source; no date resolved. Set both file paths.
- Completion criterion: either date is set (whole-day) or both file paths are set (per-cycle).

**Step 2 ("Read the sources")** — two invocation modes:
- *Whole-day mode*: read `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,research/**/*.md}` exactly as today. Skip missing files; stop if no journal entry exists.
- *Per-cycle mode*: read `{plan-file}` and `{report-file}` in full, skipping either that doesn't exist yet. If neither exists, stop.
- Completion criterion: every file that exists for the target source is read in full.

**Step 7 ("Append the log")** — change `{date-from-step-1}` to `{date}`. Add: `{date}` is the target date from step 1 in whole-day mode, or today's actual date (`date +%Y-%m-%d`) in per-cycle mode, since a cycle's ingest always happens on the day it runs.

### do-plan changes

**Step 6** — replace "Refresh search index" with "Update the global kb": invoke `@skills/kb-ingest {plan-file} {report-file}` unconditionally, every cycle (no Target project gate — global kb isn't project-scoped). Per-cycle mode is new; the cycle's plan and report are the delta, no day-wide re-read. `kb-ingest` step 8 already refreshes every `qmd` collection (removing need for standalone sync step). Completion criterion: skill completes and `~/wiki/kb/log.md` has a new line for today.

### CLAUDE.md changes

**Search bullet** — reword from descriptive ("are indexed by qmd") to imperative ("run qmd query first"). Example: "Search: before reading any file under `~/wiki` or a project's `~/wiki/projects/{slug}/wiki/` directly, run `qmd query` first per `references/qmd-search.md` — don't grep/read/walk the `index.md` chains until it returns nothing."

## AC

|AC|Category|Verification Method|
|--|--|--|
|Given `/kb-ingest {plan-file} {report-file}` is invoked with both files existing - When step 1-2 run - Then the skill reads exactly those two files as its source (no date resolved, no day-wide journal read) and proceeds through steps 3-8 unchanged|Normal|manual: read `skills/kb-ingest/SKILL.md` steps 1-2 — confirm the per-cycle branch reads only the two named files|
|Given `/kb-ingest [YYYY-MM-DD]` is invoked exactly as before (whole-day mode) - When step 1-2 run - Then behavior is byte-for-byte unchanged from the current implementation|Normal|manual: read `skills/kb-ingest/SKILL.md` steps 1-2 — confirm the whole-day branch's wording is untouched from the pre-plan version|
|Given a `/do-plan` run for a plan with no `Target project` field - When step 5 (project-wiki) is skipped - Then step 6 (kb-ingest) still runs, unconditionally|Boundary|manual: read `skills/do-plan/SKILL.md` step 6 — confirm it has no `Target project` gate, unlike step 5|
|Given `kb-ingest` is invoked in per-cycle mode - When step 7 (append the log) runs - Then the log line's date is today's actual calendar date (`date +%Y-%m-%d`), not blank or re-derived from a missing step-1 date variable|Boundary|manual: read `skills/kb-ingest/SKILL.md` step 7 — confirm the per-cycle branch names `date +%Y-%m-%d` explicitly|
|Given `do-plan`'s old standalone "Refresh search index" step - When this plan's edits are applied - Then that step no longer exists in `skills/do-plan/SKILL.md`, and no other step references it|Normal|manual: `grep -n "qmd_sync" skills/do-plan/SKILL.md` — confirm zero matches after the edit|
|Given `CLAUDE.md`'s Search bullet - When this plan's edit is applied - Then the bullet reads as an imperative instruction (query before reading), still pointing at `references/qmd-search.md`, still one bullet (no new section added)|Normal|manual: read `CLAUDE.md`'s Context Structure section — confirm exactly one Search bullet, imperative wording|
