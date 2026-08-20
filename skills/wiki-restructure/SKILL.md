---
name: wiki-restructure
description: Migrate ~/wiki from flat journal/research structure to nested journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/} structure. Invoke as /wiki-restructure.
disable-model-invocation: true
---

# Wiki Restructure

One-step skill to migrate the wiki archive structure from flat files to nested directories.

1. **Run the migration script** — invoke `bash scripts/migrate.sh`. This migrates all existing dated journal entries, research directories, and handoff/report files from the flat structure to the nested directory structure, then removes the now-empty `research/` and `advisor/` top-level directories. It is idempotent — running it twice changes nothing the second time. Completion criterion: script runs and exits 0.

Tell the user: migration complete. The wiki archive structure is now `~/wiki/journal/YYYY/MM/YYYY-MM-DD/{journal.md,handoff.md,report.md,research/}`.
