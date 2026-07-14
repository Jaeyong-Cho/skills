---
name: merge-req
description: Merges a draft Requirement Decision Record (RDR) into its committed spec after implementation is done. Use when invoked as /merge-req.
disable-model-invocation: true
---

# Merge Req

Folds a draft RDR from `.context/req/rdr/` — the record `/req` produced and `/planning`/`/auto-action` built against — into its committed spec, `.context/req/{slug}.md`, now that implementation is finished.

A draft RDR is named `{timestamp}-{slug}.md`; a merged one is `{timestamp}-{slug}.merged.md` — the filename is the state, no in-file marker to parse.

1. Find the slug: read `.context/adr/` for the ADR `/auto-action` just executed (most recently modified; if ambiguous, list candidates and ask the user which one) and take `{slug}` from its filename `{timestamp}-{slug}.md`.
2. In `.context/req/rdr/`, find draft RDR files (no `.merged.md` suffix) whose filename ends in `-{slug}.md`. If none, tell the user there's nothing to merge and stop. If more than one, list them and ask the user which to merge.
3. Copy that file's content, unchanged, to `.context/req/{slug}.md`, overwriting it entirely if it already exists — the RDR is newer and wins; don't preserve anything it superseded.
4. Rename the RDR file in place from `{timestamp}-{slug}.md` to `{timestamp}-{slug}.merged.md` — keep it as permanent decision history, never delete it.
5. Tell the user the committed spec path and the RDR's new filename.

Completion criterion: the matching RDR file is renamed to `.merged.md`, and `.context/req/{slug}.md` holds its content.
