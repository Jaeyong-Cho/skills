---
name: project-wiki
description: Synthesize a project-scoped wiki from /do-plan's output, mirroring the kb layer but narrowly fed from that project's plan/report. Invoke as /project-wiki {target-project-path} {plan-file} {report-file}.
---

# Project Wiki

Synthesize and cross-reference a project's plan and report into compounding knowledge pages, scoped to one project. This mirrors `kb-ingest` but stays narrowly focused on that project's decisions and findings.

1. **Derive the project slug** — extract the basename from `{target-project-path}` (e.g., `/Users/x/workspace/my-proj` → `my-proj`), then kebab-case it to match `/roadmap`'s convention. Assertion: the derived slug must match `^[a-z0-9][a-z0-9-]*$` before using it in any path or qmd collection name — this catches paths that don't kebab-case cleanly (e.g., with spaces or mixed case) and fails fast instead of silently creating a broken directory. Completion criterion: a validated slug is set.

2. **Read the plan and report** — read the provided `{plan-file}` in full, then read `{plan-file}.report.md` in full. These files are the STORY's whole input (narrow focus per the spec: only the project's own plan/report, not all project mentions). If either file is missing or unreadable, log a warning and continue with what exists. Completion criterion: plan and report content are available (both or partial).

3. **Read the project wiki index** — read `~/wiki/projects/{project-slug}/wiki/index.md` in full if it exists. If it doesn't, create it with OKF frontmatter (`type: Project Wiki Index`, `title: {project-slug} wiki`, today's `timestamp`) and a single heading: `# {project-slug} wiki`. Completion criterion: the index is read or created with heading.

4. **Decide what to create/update** — for each distinct decision, finding, or architecture note from the plan and report, decide: (a) new page, (b) update an existing page from step 3, or (c) skip. This is LLM judgment; there's no fixed taxonomy. A single `/do-plan` run may touch several pages or none if the plan repeats established patterns. Completion criterion: every distinct topic has an explicit decision.

5. **Write or update pages** — for each page from step 4 that needs creation or update:
   - Create or edit `~/wiki/projects/{project-slug}/wiki/pages/{slug}.md` with OKF frontmatter (`type: Project Note`, your chosen `title`/`description`/`tags`, today's `timestamp`, omit `resource` unless this page is about a specific canonical URI).
   - Include free-form content, cross-linking related pages with relative links: `[other page](./other-slug.md)`.
   - If new findings contradict existing material, note the change explicitly (per `kb-ingest` pattern: "noting where new data contradicts old claims") rather than silently overwriting.
   - Completion criterion: every page from step 4 exists with frontmatter and content.

6. **Update the index** — edit `~/wiki/projects/{project-slug}/wiki/index.md` to add or update one line per page touched in step 5: link + one-line description (same style as `kb-ingest`). Keep the index as a simple catalog. Completion criterion: every page from step 5 has an entry in the index.

7. **Append the log** — call `bash ../kb-ingest/scripts/append_log.sh ~/wiki/projects/{project-slug}/wiki/log.md {today's date} {comma-separated page slugs from step 5}`. This records what was synthesized for the project today; it creates the log if it doesn't exist. Completion criterion: `~/wiki/projects/{project-slug}/wiki/log.md` contains one new line matching `## [YYYY-MM-DD] ingest | {slugs}`.

8. **Index for search** — check if the qmd collection exists: run `qmd collection show {project-slug}`. If it fails (collection doesn't exist):
   - Create it: `qmd collection add ~/wiki/projects/{project-slug}/wiki --name {project-slug}`.
   - Add context: `qmd context add qmd://{project-slug} "Synthesized project knowledge for {project-slug}"`.

   Assertion (postcondition): before the next line, exactly one of the following must be true: (a) the collection existed before this run, or (b) the collection was just created. If neither or both are somehow true, a race or swallowed error has occurred — fail hard rather than silently leave the project un-indexed.

   Then, either way, run `bash ../kb-ingest/scripts/qmd_sync.sh` — this refreshes every collection, not just this project's (cheap, and catches anything else that's lagged behind).

   Completion criterion: the command runs, no errors, and `qmd collection show {project-slug}` reports indexed file count > 0.

Tell the user the project slug and how many pages were touched.
