---
name: merge-archi
description: Merges the draft ADR into its committed file, then derives the paired architecture doc (Static/Dynamic View) from the implemented result. Use when invoked as /merge-archi.
disable-model-invocation: true
---

# Merge Archi

Folds the draft ADR `/archi` produced and `/fs-plan` or `/co-plan`/`/auto-action` built against — from `.context/adr/` — into its committed file, `.context/adr/{slug}.md`, now that implementation is finished. Then derives the architecture doc from the merged ADR and the actual implemented code — more accurate written now, after the fact, than it would have been at design time.

A draft ADR is named `{timestamp}-{slug}.md`; a merged one is `{timestamp}-{slug}.merged.md` — the filename is the state, no in-file marker to parse.

1. Find the slug: read `.context/plan/` for the plan `/auto-action` just executed (most recently modified; if ambiguous, list candidates and ask the user which one) and take `{slug}` from its filename `{timestamp}-{slug}.md`.
2. In `.context/adr/`, find the draft ADR file (no `.merged.md` suffix) whose filename ends in `-{slug}.md`. If none, tell the user there's nothing to merge and stop. If more than one, list them and ask the user which to merge.
3. Read the source files the merged ADR's Decision names, and the requirements spec's User Scenario section, Update the architecture document with well structured it to `.context/archi/{slug}.md` with this stype `../references/document-style.md`, and template `../template/architecture.md`'s Static View and Dynamic View from what's actually there — the real classes/files as implemented, the real call flow per scenario — not just what the ADR proposed. Update the changed if there is an already existing same topic architecture documents if needed.
4. Rename the ADR file in place from `{timestamp}-{slug}.md` to `{timestamp}-{slug}.merged.md` — keep it as permanent decision history, never delete it.
5. Tell the user the committed ADR path, the ADR's new filename, and the architecture doc path.

`mkdir -p .context/archi` if needed.

Completion criterion: the matching ADR file is renamed to `.merged.md`, and `.context/archi/{slug}.md` reflects the implemented Static/Dynamic View.
