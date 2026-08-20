---
type: Spec Story
title: qmd search setup
description: Install qmd and index ~/wiki as named collections so agents can search instead of hand-walking index.md chains.
tags: [spec, llm-wiki]
timestamp: 2026-08-20T11:17:17Z
---

# qmd search setup

## Value to user

An agent can run one CLI command and get ranked results across the whole personal wiki, instead of manually walking `index.md` chains and grepping frontmatter. This is the search layer everything else in the EPIC (kb ingestion, project wikis) is queried through.

## Completion criteria

- `qmd` installed globally (confirmed: `npm install -g @tobilu/qmd` works, version 2.8.3 tested).
- Four personal collections exist: `kb` (→ `~/wiki/kb`), `journal` (→ `~/wiki/journal`), `roadmap` (→ `~/wiki/roadmap`), `today` (→ `~/wiki/today`).
- `qmd search`/`qmd query` return results from at least one real file in each collection.
- `references/document-style/frontmatter.md`'s "Reading `~/wiki`" section documents `qmd` as the first search step, `index.md`-chain-walk as fallback.

## Spec

Confirmed by direct testing this session (not assumed): `qmd collection add <dir> --name <name>` binds exactly one root directory per name — a second `add` with the same `--name` errors ("Collection already exists"), it does not merge roots. So "search the wiki first" / "search the raw archive as one bucket" (grill-me Q10) is implemented as a *query-time* convention, not a single physical collection: `-c` accepts multiple collection names in one call (tested: `qmd search "..." -c a -c b` searches both).

Collections (personal, global qmd index — this machine only, `~/.cache/qmd/index.sqlite`; `~/wiki/kb/` doesn't exist until STORY `kb-ingestion` creates it, so `qmd collection add ~/wiki/kb --name kb` must run after that, or on an empty dir it's fine, `qmd` just indexes 0 files until content lands):
```
qmd collection add ~/wiki/kb --name kb
qmd collection add ~/wiki/journal --name journal
qmd collection add ~/wiki/roadmap --name roadmap
qmd collection add ~/wiki/today --name today
qmd context add qmd://kb "Synthesized, cross-referenced knowledge — check here first"
qmd context add qmd://journal "Raw dated journal/research log — provenance, what happened when"
qmd context add qmd://roadmap "Live EPIC/STORY/Task project plans"
qmd context add qmd://today "In-flight work not yet archived for the day"
qmd embed
```
Convention (documented in `frontmatter.md`, used by every skill touched in `kb-ingestion` STORY): "search the wiki" = `qmd query "..." -c kb`; "search the raw archive" = `qmd query "..." -c journal -c roadmap -c today`; fall back to the existing `index.md`-chain-walk only for what a fresh `qmd search`/`qmd query` genuinely misses (e.g., a file written this session, before the next `qmd embed`/`qmd update` runs).

No MCP server (grill-me Q3 — CLI only). Default embedding model (grill-me Q17 — whatever `qmd pull`/`qmd embed` fetches automatically, no manual model selection).

`references/document-style/frontmatter.md` edit: replace the "Reading `~/wiki` or `spec/` (progressive disclosure)" section's 3-step procedure's first step with a new first step — run `qmd query "<question>" -c kb`, then `-c journal -c roadmap -c today` if the first misses — and demote the existing `index.md`-chain-walk to "if `qmd` returns nothing (not yet embedded, or a project with no `qmd` collection), fall back to: [existing 3 steps]".

## AC

|AC|Category|Verification Method|
|--|--|--|
|Given `qmd` is not yet installed - When `npm install -g @tobilu/qmd` runs - Then `qmd --version` prints a version string|Normal|query: `qmd --version`|
|Given the four personal collections are added and `~/wiki/journal/` has at least one `.md` file - When `qmd search "<a word known to be in that file>" -c journal` runs - Then it returns that file|Normal|query: `qmd search "..." -c journal --format json`, assert non-empty array|
|Given collections `kb` and `journal` both exist - When `qmd search "..." -c kb -c journal` runs - Then results may come from either collection (multi-`-c` filtering, not an error)|Normal|query: same command, exit code 0|
|Given a second `qmd collection add <dir> --name kb` is attempted after `kb` already exists - When it runs - Then it errors instead of silently merging or overwriting|Exception|query: `qmd collection add ~/wiki/kb --name kb` (run twice), assert second run's exit code and stderr message|
|Given `frontmatter.md` after this STORY's edit - When an agent follows its "Reading `~/wiki`" section - Then the first action named is a `qmd query`/`qmd search` call, not an `index.md` read|Normal|query: `grep -n "qmd" references/document-style/frontmatter.md` shows it before the `index.md`-chain-walk text|
