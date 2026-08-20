---
type: Spec Story
title: kb ingestion
description: A new skill that builds and maintains ~/wiki/kb/ — synthesized, cross-referenced pages compounded from journal/ — invoked by end-of-day and backfilled once over existing history.
tags: [spec, llm-wiki]
timestamp: 2026-08-20T11:17:17Z
---

# kb ingestion

## Value to user

Instead of every session re-deriving context from raw journal entries, the agent reads a small set of synthesized pages that already reflect everything ingested so far — cross-references, updates, and all — per karpathy's LLM-wiki pattern. `~/wiki/kb/` keeps compounding automatically at the end of each day.

## Completion criteria

- `skills/kb-ingest/` exists, invokable standalone (`/kb-ingest`) and from `/end-of-day`.
- `~/wiki/kb/index.md` and `~/wiki/kb/log.md` exist and follow the OKF reserved-filename convention (no frontmatter on those two).
- Every page under `~/wiki/kb/pages/*.md` carries the six-field OKF frontmatter block.
- `/end-of-day` captures the work date (via `bash scripts/archive_today.sh --date`) before the archive step deletes `~/wiki/today/journal.md`, and passes that captured date directly to `/kb-ingest`, never re-deriving it afterward.
- The existing ~14 days of history (post-restructure, per `restructure-raw-archive`) have been backfilled into `~/wiki/kb/` at least once.
- `qmd collection add ~/wiki/kb --name kb` (from `qmd-search-setup`) returns non-zero indexed files after backfill.

## Spec

New skill `skills/kb-ingest/SKILL.md` — no `disable-model-invocation` (same as `d-handoff`: user-invokable as `/kb-ingest [YYYY-MM-DD]` *and* agent-fireable from `/end-of-day`), default date today per `archive_today.sh --date`:

1. Read `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,research/**}` in full for the target date (skip files that don't exist).
2. Read `~/wiki/kb/index.md` (create with a `# Knowledge Base` heading if absent) to see what pages already exist — this is the whole point of an index-first read (`document-style/frontmatter.md`'s progressive disclosure), not opening every page.
3. For each distinct topic/entity/decision found in step 1: decide new page or update to an existing one (LLM judgment, no fixed taxonomy — this is deliberately open per karpathy's pattern: "your agent will build out the specifics in collaboration with you"). A single day's ingest may touch several pages.
4. Write/update pages at `~/wiki/kb/pages/{slug}.md`: OKF frontmatter (`type: Wiki Page`), then free-form content — cross-link related pages with relative links (`[other page](./other-slug.md)`), and where a new day's content contradicts or supersedes something already on the page, say so explicitly rather than silently overwriting (karpathy: "noting where new data contradicts old claims").
5. Update `~/wiki/kb/index.md` — one line per page: link + one-line description (content-oriented catalog, per `document-style/frontmatter.md`'s definition of `index.md`).
6. Append one line to `~/wiki/kb/log.md` via `skills/kb-ingest/scripts/append_log.sh {date} {comma-separated page slugs touched}` — format `## [YYYY-MM-DD] ingest | {source}` per karpathy's grep-parseable convention (chronological, append-only, no frontmatter — OKF reserved filename).
7. Run `qmd embed -c kb` (or `qmd update -c kb` if the collection already exists) so the new/changed pages are searchable immediately, not just after the next scheduled embed.

`skills/kb-ingest/scripts/append_log.sh` is the one deterministic, testable sliver of this skill (mirrors `end-of-day/scripts/archive_today.sh`'s `--test` convention) — it only formats and appends the log line; it does not decide what to write, that's the LLM's job in steps 3-4.

`end-of-day/SKILL.md` gets two steps: first (step 2, "Archive today's working files") captures the work date by running `bash scripts/archive_today.sh --date` before calling the real `bash scripts/archive_today.sh`, recording the output as `{work-date}` while `~/wiki/today/journal.md` still exists — the date is based on that file's creation time, not the calendar date. Then (step 3, "Update the kb layer") invokes `@skills/kb-ingest {work-date}`, passing the captured date directly, never re-deriving it after the archive deletes the journal file (a re-derive at that point returns today's wall-clock date instead, silently wrong when a session crosses midnight). This replaces no existing step; the plain `mv` in `archive_today.sh` still runs first (raw archive stays immutable and separate from synthesis, per grill-me's layering decision).

Backfill: once, over every existing dated `journal/YYYY/MM/YYYY-MM-DD/` directory (post-`restructure-raw-archive`, ~14 days per the wiki's current history) — `/do-plan` executing this STORY runs `/kb-ingest {date}` once per existing date, oldest first, so later days can build on/cross-reference pages earlier days created.

## AC

|AC|Category|Verification Method|
|--|--|--|
|Given a target date with no `~/wiki/kb/log.md` yet - When `append_log.sh` runs for that date with pages "a,b" - Then `~/wiki/kb/log.md` is created and contains one line matching `## [YYYY-MM-DD] ingest \| a, b`|Normal|self-test: `skills/kb-ingest/scripts/append_log.sh --test`|
|Given `~/wiki/kb/log.md` already has entries - When `append_log.sh` runs again for a new date - Then the new line is appended, existing lines are untouched, and `grep "^## \[" log.md \| tail -1` returns the newest entry|Normal|self-test: `skills/kb-ingest/scripts/append_log.sh --test`|
|Given `/end-of-day` runs for a day with journal content - When it reaches the new kb-layer step - Then `~/wiki/kb/index.md` lists at least one page that didn't exist before that run|Normal|manual test: run `/end-of-day` against a fixture day, diff `kb/index.md` before/after|
|Given every page under `~/wiki/kb/pages/*.md` after backfill - When each is opened - Then every one has all six OKF frontmatter fields (or the optional `resource` line correctly omitted)|Normal|query: a small grep/frontmatter-parse check across `~/wiki/kb/pages/*.md`, run once post-backfill|
|Given `qmd collection add ~/wiki/kb --name kb` runs after backfill - When `qmd status` or `qmd collection show kb` runs - Then indexed file count is greater than 0|Normal|query: `qmd collection show kb`|
|Given `~/wiki/today/journal.md` was created on a prior calendar day (a session spanning midnight) - When `/end-of-day` runs to completion - Then `/kb-ingest` is invoked for that prior day's date, matching the `journal/YYYY/MM/YYYY-MM-DD/` directory `archive_today.sh` actually archived into, not the wall-clock date|Boundary|manual: read `skills/end-of-day/SKILL.md` steps 2-3 — confirm `{work-date}` is captured via `bash scripts/archive_today.sh --date` *before* the real `bash scripts/archive_today.sh` call runs (the call that deletes `today/journal.md`), and step 3 passes that captured `{work-date}` value as `@skills/kb-ingest {work-date}`'s argument instead of calling `--date` again|
|Given `skills/kb-ingest/SKILL.md`'s existing "called with a date argument, use that" branch (step 1, unchanged by this plan) - When `end-of-day` invokes it as `@skills/kb-ingest {work-date}` - Then `kb-ingest` uses `{work-date}` directly and never falls back to its own `--date` call|Normal|manual: read `skills/kb-ingest/SKILL.md` step 1 — confirm the explicit-date branch is what `end-of-day`'s corrected step 3 now exercises|
