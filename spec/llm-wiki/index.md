# LLM Wiki

## Business value

Agents (this skills repo's own `/explore`, `/recon`, `/advisor`→removed, `/end-of-day`, per-project `/do-plan`) currently can only find prior context by hand-walking `index.md` chains — there's no search. That means every session either re-explains context the user already wrote down, or misses it entirely. This EPIC adds `qmd` (local hybrid BM25/vector search) over `~/wiki`, and a self-maintaining synthesized "kb" layer per [karpathy's LLM-wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) that compounds instead of forcing re-derivation from raw logs every time — for both the personal wiki and, per-project, work planned via `/to-plan`+`/do-plan`.

## Completion criteria

All four STORIES below shipped:
- Raw `~/wiki` archive restructured (`journal/research` merged, `advisor` removed) via a reusable, idempotent skill.
- `qmd` installed and indexing `~/wiki` as named collections.
- `~/wiki/kb/` exists, synthesized from `journal/` on every `/end-of-day`, searched before the `index.md`-chain fallback.
- Every project touched via `/do-plan` gets its own `~/wiki/projects/{slug}/wiki/`, kept current and independently searchable.

## Overview

Full design history: `~/wiki/today/research/00-llm-wiki/` (this session's `/grill-me` transcript settled every decision below; nothing here was silently assumed).

Layering (karpathy pattern — additive, immutable raw + LLM-synthesized layer):
- `journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/NN-{job}/...}` — raw, immutable log. Replaces today's flat `journal/YYYY/MM/YYYY-MM-DD.md` + separate top-level `research/YYYY/MM/YYYY-MM-DD/`.
- `~/wiki/kb/` — new. LLM-synthesized pages, built only from `journal/` (not `roadmap/`, not `today/`).
- `roadmap/` and `today/` — untouched in shape; still indexed for search, just not synthesized from.
- `advisor/` — removed entirely, no replacement (skill, history, and its "friction/automation candidate" capability all gone).
- `~/wiki/projects/{project-slug}/wiki/` — per-project mirror of `kb/`, fed narrowly from `/to-plan`+`/do-plan` output for that project (using `/to-plan`'s existing "Target project" field), not a broad sweep.

Search: `qmd` CLI only (no MCP), default local embedding model. Collections mirror top-level dirs 1:1 (`qmd`'s real model is one root directory per named collection, confirmed by testing — no multi-root merge under one name): `kb`, `journal`, `roadmap`, `today` personally, one `{project-slug}` collection per project. "Search the wiki first" = `-c kb`; "search the raw archive" = `-c journal -c roadmap -c today` (multi-`-c` filtering, confirmed working). `index.md`-chain-walk is the fallback for what isn't indexed yet.

Out of scope (explicitly, from the grill-me session): MCP server, any lint/health-check pass for either wiki layer, resurrecting advisor's friction-hunting in any form.

## Stories
- [restructure-raw-archive](./restructure-raw-archive.md)
- [qmd-search-setup](./qmd-search-setup.md)
- [kb-ingestion](./kb-ingestion.md)
- [project-wiki](./project-wiki.md)
