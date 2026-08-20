# Frontmatter (OKF)

**MUST**, every new document written under `~/wiki/**/*.md` or a target repo's `spec/**/*.md` — [Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing?hl=en). Out of scope: everything else outside `~/wiki`/`spec/` (a plan's `.report.md`, vendored skills like `teach`/`diagram-design` that keep their own format).

Add a YAML frontmatter block at the top of the file, all six fields, every time:

```yaml
---
type: <Kind of document>
title: <Human-readable name>
description: <One-line summary>
resource: <Canonical URI this doc is about, or omit the line if none>
tags: [<tag>, ...]
timestamp: <ISO 8601 datetime, when this content was last meaningfully written>
---
```

- `type` — a short, descriptive string; pick what fits, there's no central registry. Examples already implied by what writes into `~/wiki`/`spec/`: `Journal Entry`, `Handoff`, `Advisor Report`, `Research Explore`, `Research Experiment`, `Research Plan`, `Research Recon`, `Research Context`, `Roadmap Project`, `Roadmap Epic`, `Roadmap Story`, `Goal`, `Spec Story`.
- `title`, `description`, `tags` — what a search index or an `index.md` entry pulls from first.
- `resource` — the canonical URI the doc is *about* (a PR, a dashboard, a repo, an external doc). Most `~/wiki` entries describe work rather than a resource — omit the line rather than inventing one.
- `timestamp` — when the content was last meaningfully written, not the file's mtime.

`index.md` and `log.md` are OKF's reserved filenames — no frontmatter on those. `index.md` is what OKF calls progressive disclosure: a directory listing linking each document with its one-line description, letting an agent see what exists before opening any one file. This is already the convention throughout `~/wiki` and `spec/` (journal/research/goals/roadmap index chains, `spec/index.md` → `spec/{epic-slug}/index.md`); nothing new to add there beyond keeping those links current.

## Searching `~/wiki` or `spec/` (progressive disclosure)

When a task searches `~/wiki` or a target repo's `spec/` tree for relevant material (`@skills/explore`, `@skills/recon`), read cheap-to-expensive:

1. Walk the `index.md` chain down from the relevant root (`journal/`, `research/`, `goals/`, `roadmap/`, or `spec/`) toward the likely date/project/EPIC — each `index.md` narrows which subdirectory to enter next.
2. Once in a candidate directory, `grep`/read just the frontmatter block (`type`/`title`/`description`/`tags`) of the `.md` files there to shortlist matches, instead of opening every file in full.
3. Open the full body only for files the frontmatter shortlisted.

This is the whole point of carrying frontmatter: a search should resolve from `index.md` + frontmatter alone whenever it can, and only pay for a full read on an actual candidate.

## Fixing existing documents (progressive, not a migration sweep)

No bulk migration — old `~/wiki`/`spec/` documents keep whatever shape they were written in until something touches them. When a skill opens an existing `~/wiki/**/*.md` or `spec/**/*.md` file for reading or editing and finds:

- **No frontmatter** — add the six-field block before writing the file back, inferring `type`/`title`/`description`/`tags`/`timestamp` from the content (`resource` only if one is genuinely named in the doc).
- **A path that no longer matches this repo's current convention** for that document (e.g. a roadmap STORY still filed as `{epic-slug}/{story-slug}/index.md` instead of `{epic-slug}/{story-slug}.md`, or a spec STORY filed outside `spec/{epic-slug}/{story-slug}.md`) — `mv` it to the current path and fix every `index.md` link that pointed at the old one, same as any other Fix in `@skills/roadmap`, or the "keep the spec in sync" step in `@skills/do-plan`.

Do this as part of whatever touched the file, not as a separate pass. A directory nobody opens keeps its old shape indefinitely, and that's fine.

Skipped: OKF's provenance/trust/lifecycle families (`sources`, `verified`, `status`, `stale_after`) and Attested Computation concepts — built for a data catalog verifying BigQuery-grade claims, not a personal wiki. Add a field when a real need for it shows up (e.g. `status: deprecated` on a stale roadmap EPIC), not preemptively.
