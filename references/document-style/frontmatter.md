# Frontmatter (OKF)

**MUST**, every new document written under `~/wiki/**/*.md` — [Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing?hl=en). Out of scope: files written outside `~/wiki` (a target repo's `spec/`, a plan's `.report.md`, vendored skills like `teach`/`diagram-design` that keep their own format).

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

- `type` — a short, descriptive string; pick what fits, there's no central registry. Examples already implied by what writes into `~/wiki`: `Journal Entry`, `Handoff`, `Advisor Report`, `Research Explore`, `Research Experiment`, `Research Plan`, `Research Recon`, `Research Context`, `Roadmap Project`, `Roadmap Epic`, `Roadmap Story`, `Goal`.
- `title`, `description`, `tags` — what a search index or an `index.md` entry pulls from first.
- `resource` — the canonical URI the doc is *about* (a PR, a dashboard, a repo, an external doc). Most `~/wiki` entries describe work rather than a resource — omit the line rather than inventing one.
- `timestamp` — when the content was last meaningfully written, not the file's mtime.

`index.md` and `log.md` are OKF's reserved filenames — no frontmatter on those. `index.md` is what OKF calls progressive disclosure: a directory listing linking each document with its one-line description, letting an agent see what exists before opening any one file. This is already the convention throughout `~/wiki` (journal/research/goals/roadmap index chains); nothing new to add there beyond keeping those links current.

## Searching `~/wiki` (progressive disclosure)

When a task searches `~/wiki` for relevant material (`@skills/explore`, `@skills/recon`), read cheap-to-expensive:

1. Walk the `index.md` chain down from the relevant root (`journal/`, `research/`, `goals/`, `roadmap/`) toward the likely date/project — each `index.md` narrows which subdirectory to enter next.
2. Once in a candidate directory, `grep`/read just the frontmatter block (`type`/`title`/`description`/`tags`) of the `.md` files there to shortlist matches, instead of opening every file in full.
3. Open the full body only for files the frontmatter shortlisted.

This is the whole point of carrying frontmatter: a search should resolve from `index.md` + frontmatter alone whenever it can, and only pay for a full read on an actual candidate.

Skipped: OKF's provenance/trust/lifecycle families (`sources`, `verified`, `status`, `stale_after`) and Attested Computation concepts — built for a data catalog verifying BigQuery-grade claims, not a personal wiki. Add a field when a real need for it shows up (e.g. `status: deprecated` on a stale roadmap EPIC), not preemptively.
