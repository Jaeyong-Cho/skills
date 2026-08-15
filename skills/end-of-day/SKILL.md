---
name: end-of-day
description: Run d-handoff, then compile today's journal, research notes, and handoff into a report with a table of contents and an Introduction/Abstraction/Detailed breakdown per topic. Invoke as /end-of-day.
disable-model-invocation: true
---

# End of Day

Read `../references/document-style.md` first — its Introduction/Abstraction/Detailed structure and priority order (key-value > table > bullets > prose) govern every section this skill writes.

1. **Run the day's other skills first** — invoke `@skills/d-handoff` and record its output file path. It reads today's in-progress work from `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/`. Completion criterion: it has run and its path is recorded.
2. **Resolve finished goals** — check `~/wiki/today/research/NN-{job}/` for any entry that is a symlink to `~/wiki/goals/{slug}/` (a multi-day effort, not a one-off job). For each, ask the user (AskUserQuestion, multi-select) which are now finished. For each finished slug, `mv ~/wiki/goals/{slug} ~/wiki/goals/YYYY/MM/NN-{slug}/` (current year/month, next free `NN-` in that month) and remove the now-dangling symlink from `today/research/`. Leave still-active symlinks in place — step 3 archives them as-is. Skip silently if no such symlinks exist. Completion criterion: every goal symlink has been asked about, and finished ones are moved under `~/wiki/goals/YYYY/MM/` before step 3 runs.
3. **Archive today's working files** — run `bash scripts/archive_today.sh` (relative to this skill's directory). It moves `~/wiki/today/journal.md` into `~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` and each remaining `~/wiki/today/research/NN-{job}/` entry (plain dirs and any still-active goal symlinks) into `~/wiki/research/YYYY/MM/YYYY-MM-DD/`, then removes `~/wiki/today/`. The date used is `today/journal.md`'s creation date, not the date the script happens to run on — a session that starts in the evening and is archived after midnight still files under the day it started. Run this after steps 1-2, not before — d-handoff still needs `today/` in place, and step 2's finished goals need to already be moved out. Completion criterion: the script ran and `~/wiki/today/` no longer exists.
4. **Seed tomorrow's work context** — write a fresh `~/wiki/today/journal.md` (`mkdir -p` the parent; step 3 just removed this file, so create it new — don't reuse an old one), with one section:
   - `## Context to Continue` — from the handoff file written in step 1, its "Open Items" and "Carried Decisions" copied as bullets, exact not paraphrased, plus the handoff file's path for full detail. Skip this section if the handoff has neither.
   If the section is skipped, skip the whole step and say so. Completion criterion: `~/wiki/today/journal.md` exists with the section populated, or an explicit "nothing to carry" note.
5. **Gather today's sources** — read today's journal file (`~/wiki/journal/YYYY/MM/YYYY-MM-DD.md`), today's research directories (`~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/`), and the file from step 1, all in full. Completion criterion: every source is either read in full or confirmed absent.
6. **Split into content items** — one item per topic, task, or research job from the journal/research, plus one "Handoff" item from the handoff file. Completion criterion: every entry from step 5, including the handoff file, is assigned to exactly one content item.
7. **Draft each content item** in three phases per `../references/document-style.md`: Introduction (1-3 sentences, why/what), Abstraction (the objects, interactions, and relationships involved), Detailed (one representative concrete example, including any research result or finding). Completion criterion: every content item has all three phases, each obeying that file's size limits.
8. **Build the table of contents** — list content item titles in the order they appear, each linking to its section. Completion criterion: ToC entry count equals the content item count from step 6.
9. **Write the markdown report** — assemble ToC + all content items into `~/wiki/journal/YYYY/MM/YYYY-MM-DD-report.md` (`mkdir -p` the parent directory if needed). If it would exceed the 500-word file cap in `../references/document-style.md`, split the largest content items into separate linked files instead of shrinking their phases. Completion criterion: the file exists with a ToC and every content item's three phases.

Tell the user the markdown report path.
