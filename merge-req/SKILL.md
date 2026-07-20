---
name: merge-req
description: Merges a draft Requirement Decision Record (RDR) into its committed spec after implementation is done. Use when invoked as /merge-req.
disable-model-invocation: true
---

# Merge Req

Folds a draft RDR from `.context/rdr/` — the record `/req` produced and `/archi`/`/fs-plan` or `/co-plan`/`/auto-action` built against — into its committed spec, `.context/req/{slug}.md`, now that implementation is finished.

A draft RDR is named `{timestamp}-{slug}.md`; a merged one is `{timestamp}-{slug}.merged.md` — the filename is the state, no in-file marker to parse.

1. Find the slug: read `.context/plan/` for the plan `/auto-action` just executed (most recently modified; if ambiguous, list candidates and ask the user which one) and take `{slug}` from its filename — `{timestamp}-{slug}.md` if still in progress, `{timestamp}-{slug}.done.md` once `/auto-action` has marked it complete (strip both the timestamp prefix and the `.done` suffix, not just `.md`).
2. In `.context/rdr/`, find draft RDR files (no `.merged.md` suffix) whose filename ends in `-{slug}.md`. If none, tell the user there's nothing to merge and stop. If more than one, list them and ask the user which to merge.
3. Rewrite well structured requirement documents at the `.context/req/{slug}.md` with this style `../references/document-style.md`, updating changed if the already existing related topic requirement documents. — the RDR is newer and wins.
4. Rename the RDR file in place from `{timestamp}-{slug}.md` to `{timestamp}-{slug}.merged.md` — keep it as permanent decision history, never delete it.
5. Tell the user the committed spec path and the RDR's new filename.

Completion criterion: the matching RDR file is renamed to `.merged.md`, and `.context/req/{slug}.md` holds its content.
