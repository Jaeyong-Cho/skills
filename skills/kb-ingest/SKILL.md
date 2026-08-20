---
name: kb-ingest
description: Ingest today's journal and research into the knowledge base (~/wiki/kb/), creating or updating synthesized pages with cross-references per karpathy's LLM-wiki pattern. Invoke as /kb-ingest [YYYY-MM-DD].
---

# KB Ingestion

Per karpathy's LLM-wiki pattern, synthesize and cross-reference the day's journal and research into compounding knowledge pages. This is an agent-executed skill — the LLM decides which pages to create/update, not a deterministic script.

1. **Get the target date** — if called with a date argument `/kb-ingest YYYY-MM-DD`, use that; otherwise use today via `bash ../end-of-day/scripts/archive_today.sh --date`. Completion criterion: a date in `YYYY-MM-DD` format is set.

2. **Read the target day's sources** — read `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,research/**/*.md}` in full for the target date. Skip any files that don't exist. If no journal entry exists for this date at all, tell the user and stop. Completion criterion: every file that exists for the target date is read in full.

3. **Read the knowledge base index** — read `~/wiki/kb/index.md` in full to see what pages already exist. If the file doesn't exist, create it with a single line: `# Knowledge Base`. Completion criterion: the index is read or created.

4. **Decide what to create/update** — for each distinct topic, entity, or decision found in step 2, decide: (a) new page, (b) update an existing page from step 3, or (c) skip entirely. This is LLM judgment; there's no fixed taxonomy. A single day's ingest may touch several pages, or none if the day repeats established themes. Completion criterion: every topic from step 2 has an explicit decision.

5. **Write or update pages** — for each topic from step 4 that needs a new page or an update:
   - Create or edit `~/wiki/kb/pages/{slug}.md` with OKF frontmatter (`type: Wiki Page`, your chosen `title`/`description`/`tags`, today's `timestamp`, omit `resource` unless this page is about a specific canonical URI).
   - Include free-form content, cross-linking related pages with relative links: `[other page](./other-slug.md)`.
   - If new day content contradicts or supersedes existing material, note the change explicitly (per karpathy: "noting where new data contradicts old claims") rather than silently overwriting.
   - Completion criterion: every page from step 4 exists with frontmatter and content.

6. **Update the index** — edit `~/wiki/kb/index.md` to add or update one line per page touched in step 5: link + one-line description (e.g., `- [Foo Concept](./foo-concept.md) — How foo and bar interact.`). Keep the index as a simple catalog. Completion criterion: every page from step 5 has an entry in the index.

7. **Append the log** — call `bash scripts/append_log.sh ~/wiki/kb/log.md {date-from-step-1} {comma-separated page slugs from step 5}` (relative to this skill's directory). This records what was ingested today; it creates the log if it doesn't exist. Completion criterion: `~/wiki/kb/log.md` contains one new line matching `## [YYYY-MM-DD] ingest | {slugs}`.

8. **Index for search** — run `qmd update -c kb` if the collection already exists, or `qmd embed -c kb` if this is the first run. This makes new/updated pages searchable immediately. Completion criterion: the command succeeds and `qmd collection show kb` reports indexed file count > 0.

Tell the user the target date and how many pages were touched.
