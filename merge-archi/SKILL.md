---
name: merge-archi
description: Merges a draft ADR into its committed architecture doc after implementation is done. Use when invoked as /merge-archi.
disable-model-invocation: true
---

# Merge Archi

Folds a draft ADR from `.context/adr/` — the record `/archi` produced and `/planning`/`/auto-action` built against — into its committed architecture doc, `.context/adr/{slug}.md`, now that implementation is finished.

A draft ADR is named `{timestamp}-{slug}.md`; a merged one is `{timestamp}-{slug}.merged.md` — the filename is the state, no in-file marker to parse.

1. Find the slug: read `.context/plan/` for the plan `/auto-action` just executed (most recently modified; if ambiguous, list candidates and ask the user which one) and take `{slug}` from its filename `{timestamp}-{slug}.md`.
2. In `.context/adr/`, find the draft ADR file (no `.merged.md` suffix) whose filename ends in `-{slug}.md`. If none, tell the user there's nothing to merge and stop. If more than one, list them and ask the user which to merge.
3. Copy that file's content, unchanged, to `.context/adr/{slug}.md`, overwriting it entirely if it already exists — the ADR is newer and wins; don't preserve anything it superseded.
4. Rename the ADR file in place from `{timestamp}-{slug}.md` to `{timestamp}-{slug}.merged.md` — keep it as permanent decision history, never delete it.
5. Tell the user the committed doc path and the ADR's new filename.

Completion criterion: the matching ADR file is renamed to `.merged.md`, and `.context/adr/{slug}.md` holds its content.
