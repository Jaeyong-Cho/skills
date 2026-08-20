---
type: Spec Story
title: Restructure raw archive
description: Merge journal+research into nested per-day dirs and remove advisor, via a small reusable/idempotent skill so the same restructuring can run on another machine's ~/wiki.
tags: [spec, llm-wiki]
timestamp: 2026-08-20T11:17:17Z
---

# Restructure raw archive

## Value to user

`~/wiki`'s raw archive stops being split across two top-level trees (`journal/`, `research/`) plus a third (`advisor/`) that's being dropped outright. One nested-per-day shape, and a skill the user can re-run on any machine holding a `~/wiki` copy instead of migrating by hand each time.

## Completion criteria

- `~/wiki/research/` and `~/wiki/advisor/` no longer exist.
- Every existing dated entry now lives at `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/NN-{job}/...}` (only the files that existed for that day).
- `skills/wiki-restructure/scripts/migrate.sh` exists, is idempotent (a second run is a no-op), and its `--test` self-test passes.
- `skills/advisor/` is deleted from the repo; no remaining reference to `/advisor` in `README.md`, `CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`, or any `SKILL.md`.
- `skills/end-of-day` and `skills/d-handoff` read/write the new nested paths.

## Spec

New skill `skills/wiki-restructure/` (invoked as `/wiki-restructure`, `disable-model-invocation: true` — same convention as `end-of-day`/`roadmap`) wrapping one idempotent script, `scripts/migrate.sh`, mirroring `skills/end-of-day/scripts/archive_today.sh`'s style (plain bash, a `--test` flag running a self-test against a `mktemp -d` fixture, no framework).

`migrate.sh $WIKI_DIR` (default `$HOME/wiki`) does, per existing `journal/YYYY/MM/YYYY-MM-DD.md`:
1. Skip the day if `journal/YYYY/MM/YYYY-MM-DD/` already exists as a directory (idempotent).
2. `mkdir -p journal/YYYY/MM/YYYY-MM-DD/`, move `YYYY-MM-DD.md` → `YYYY-MM-DD/journal.md`, `YYYY-MM-DD-handoff.md` → `YYYY-MM-DD/handoff.md` (if present), `YYYY-MM-DD-report.md` → `YYYY-MM-DD/report.md` (if present).
3. If `research/YYYY/MM/YYYY-MM-DD/` exists, move it to `journal/YYYY/MM/YYYY-MM-DD/research/`.
4. Fix `journal/YYYY/MM/index.md` link lines from `./YYYY-MM-DD.md` to `./YYYY-MM-DD/journal.md`.
5. After all days processed: `rm -rf research/` and `rm -rf advisor/` (whole trees — this is derived/raw data per the grill-me decision, not migrated).

Skill edits required for the new layout (all under `skills/`):
- `end-of-day/scripts/archive_today.sh`: archive into `journal/$year/$month/$today_date/{journal.md,research/}` instead of the current flat `journal/$year/$month/$today_date.md` + top-level `research/$year/$month/$today_date/`; drop the top-level `research/` destination entirely; update its own `--test` self-test fixture assertions to match.
- `end-of-day/SKILL.md`: step 2's destination description, step 4's source paths (`journal/YYYY/MM/YYYY-MM-DD.md`, `research/YYYY/MM/YYYY-MM-DD/NN-{job}/`), step 8's output path (`journal/YYYY/MM/YYYY-MM-DD-report.md` → `.../YYYY-MM-DD/report.md`).
- `d-handoff/SKILL.md`: step 3's output path (`journal/YYYY/MM/YYYY-MM-DD-handoff.md` → `.../YYYY-MM-DD/handoff.md`).
- `advisor/`: delete the whole directory.
- `explore/SKILL.md`, `recon/SKILL.md` (context only, no path in it besides `today/research/`), `to-context/SKILL.md`, `to-plan/SKILL.md`, `experiment/SKILL.md`: each has one trailing sentence "`@skills/end-of-day` archives `today/research/` into the dated `~/wiki/research/` path at day's end" — change `~/wiki/research/` to `~/wiki/journal/.../research/`.
- `references/document-style/frontmatter.md`: drop `Advisor Report` from the `type` examples list.

Repo-doc edits:
- `README.md`: remove the `/advisor` row; remove "and `/advisor`" / advisor findings from `/end-of-day`'s description and path column (now `.../YYYY-MM-DD/report.md`); remove `/advisor` from the footnote line listing agent-fireable skills and the personal-daily-workflow-tools list; update `/d-handoff`, `/to-plan`, `/explore`, `/experiment` path columns to the nested `journal/.../research/` shape.
- `CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`: in the Context Structure section, delete the "Advisor:" line; update "Journal:" and "Research:" lines to describe the single nested `journal/YYYY/MM/YYYY-MM-DD/` shape (research folded in as its `research/` subdirectory, no longer its own top-level line).

Install-side note (documented, not scripted — `install.sh` already supports it): running `install.sh --clean` after this merges removes `~/.claude/skills/advisor/` (and other agents' copies) via its existing stale-skill manifest tracking; plain `install.sh` alone would leave it behind.

## AC

|AC|Category|Verification Method|
|--|--|--|
|Given a `~/wiki` fixture with a flat `journal/2026/01/2026-01-15.md`, a matching `research/2026/01/2026-01-15/00-demo/`, and no prior nested dir - When `migrate.sh` runs - Then `journal/2026/01/2026-01-15/journal.md` and `journal/2026/01/2026-01-15/research/00-demo/` both exist and the old flat/`research/` paths are gone|Normal|self-test: `skills/wiki-restructure/scripts/migrate.sh --test`|
|Given a `~/wiki` fixture already migrated (nested dir exists) - When `migrate.sh` runs again - Then nothing changes and it exits 0|Boundary|self-test: `skills/wiki-restructure/scripts/migrate.sh --test`|
|Given a `~/wiki` fixture with an `advisor/2026/01/2026-01-15.md` - When `migrate.sh` runs - Then `advisor/` no longer exists anywhere under the fixture|Normal|self-test: `skills/wiki-restructure/scripts/migrate.sh --test`|
|Given today's work has been written to `~/wiki/today/journal.md` and `~/wiki/today/research/00-x/` - When `/end-of-day` runs its archive step - Then the result lands at `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,research/00-x/}`, not the old flat/top-level-research shape|Normal|self-test: `skills/end-of-day/scripts/archive_today.sh --test`|
|Given the repo after this STORY merges - When grepping `README.md`, `CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`, and every `skills/*/SKILL.md` for `advisor` - Then zero matches remain|Normal|query: `grep -ril advisor README.md CLAUDE.md AGENTS.md copilot-instructions.md skills/*/SKILL.md` exits 1 (no output)|
