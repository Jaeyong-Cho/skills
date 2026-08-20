---
type: Spec Story
title: Project wiki
description: A per-project mirror of the kb layer, fed narrowly from /to-plan+/do-plan output for that project and triggered when /do-plan finishes.
tags: [spec, llm-wiki]
timestamp: 2026-08-20T11:17:17Z
---

# Project wiki

## Value to user

Coming back to a project after time away, the agent reads a handful of synthesized pages about *that project* — architecture, standing decisions, gotchas — instead of re-reading every past plan/report to reconstruct what it already figured out.

## Completion criteria

- `skills/project-wiki/` exists, invokable standalone and from `/do-plan`'s finishing step.
- `/do-plan` invokes it once per run, using the plan's Target project field, after writing the report.
- `~/wiki/projects/{project-slug}/wiki/{index.md,log.md,pages/*.md}` exist for at least one real project after its next `/do-plan` run.
- A `qmd` collection named `{project-slug}` exists over that project's wiki dir, created the first time `/project-wiki` runs for it.

## Spec

New skill `skills/project-wiki/SKILL.md` (no `disable-model-invocation`, same as `kb-ingest`), invoked as `/project-wiki {target-project-path} {plan-file} {report-file}`:

1. Derive `{project-slug}` from `{target-project-path}` — kebab-case basename (e.g. `/Users/x/workspace/idle-engine` → `idle-engine`), same slugging convention `/roadmap` already uses for `{project}`, so the same project has one consistent slug across `roadmap/`, `~/wiki/projects/`, and its `qmd` collection name.
2. Read the plan file and its `{plan-file}.report.md` in full (this is the STORY's whole input — narrow per grill-me Q14, not a broad sweep of everything mentioning the project).
3. Read `~/wiki/projects/{project-slug}/wiki/index.md` (create with a `# {project-slug} wiki` heading if this is the first run for this project).
4. Decide new/updated pages under `~/wiki/projects/{project-slug}/wiki/pages/{slug}.md` — same OKF-frontmatter, cross-linked, contradiction-noting convention as `kb-ingest` step 4 (LLM judgment, no fixed taxonomy).
5. Update `index.md`, and append one line to `log.md` via `../kb-ingest/scripts/append_log.sh ~/wiki/projects/{project-slug}/wiki/log.md {today's date} {slugs touched}` (reusing `kb-ingest`'s script — same log-line format, one implementation, two callers).
6. If `qmd collection show {project-slug}` fails (doesn't exist yet): `qmd collection add ~/wiki/projects/{project-slug}/wiki --name {project-slug}` and `qmd context add qmd://{project-slug} "Synthesized project knowledge for {project-slug}"`. Then `qmd embed -c {project-slug}` (or `qmd update -c {project-slug}` if it already existed).

`skills/kb-ingest/scripts/append_log.sh` generalized to take the log file path as its first argument (currently hardcoded to `~/wiki/kb/log.md` per the `kb-ingestion` STORY draft) — this STORY changes that signature to `append_log.sh <log-file> <date> <slugs>`, and `kb-ingest`'s own call site updates to pass `~/wiki/kb/log.md` explicitly. One script, two callers, no duplicated bookkeeping logic (deep module).

`do-plan/SKILL.md` gets one new step 5, after the existing step 4 (write report) and before "tell the user the report path": "**Update the project's wiki** — invoke `@skills/project-wiki {target-project} {plan-file} {report-file}`, reading `{target-project}` from the plan's Target project field. Skip if the plan has no Target project (a plan that isn't scoped to one repo)." Existing step 4/"tell the user" ordering is otherwise unchanged.

## AC

|AC|Category|Verification Method|
|--|--|--|
|Given `append_log.sh` is called with an explicit log-file path, a date, and slugs - When it runs - Then that exact file gets the appended line, not a hardcoded default|Normal|self-test: `skills/kb-ingest/scripts/append_log.sh --test` (updated fixture covers a non-default path)|
|Given a `/do-plan` run against a plan with a Target project field and no prior `~/wiki/projects/{slug}/wiki/` - When `/do-plan` finishes - Then `~/wiki/projects/{slug}/wiki/index.md` and at least one page under `pages/` now exist|Normal|manual test: run `/do-plan` against a fixture plan, check the resulting directory|
|Given a `/do-plan` run against a plan with no Target project field - When `/do-plan` finishes - Then no `~/wiki/projects/` directory is created and no error is raised|Boundary|manual test: run `/do-plan` against a fixture plan lacking that field|
|Given `{project-slug}`'s qmd collection doesn't exist yet - When `/project-wiki` runs for that project the first time - Then `qmd collection show {project-slug}` succeeds afterward and its indexed file count is greater than 0|Normal|query: `qmd collection show {project-slug}`|
|Given `{project-slug}`'s qmd collection already exists - When `/project-wiki` runs again for the same project - Then it uses `qmd update` instead of erroring on a duplicate `qmd collection add`|Exception|query: run `/project-wiki` twice for the same fixture project, assert second run's exit code is 0|
