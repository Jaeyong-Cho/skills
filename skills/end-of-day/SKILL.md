---
name: end-of-day
description: Run d-handoff, then compile today's journal, research notes, and handoff into a report with a table of contents and an Introduction/Abstraction/Detailed breakdown per topic. Invoke as /end-of-day.
disable-model-invocation: true
---

# End of Day

Read `../references/document-style.md` first — its Introduction/Abstraction/Detailed structure and priority order (key-value > table > bullets > prose) govern every section this skill writes.

1. **Run the day's other skills first** — invoke `@skills/d-handoff` and record its output file path. It reads today's in-progress work from `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/`. Completion criterion: it has run and its path is recorded.
2. **Archive today's working files** — run `bash scripts/archive_today.sh` (relative to this skill's directory). It moves `~/wiki/today/journal.md` into `~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` and each remaining `~/wiki/today/research/NN-{job}/` entry into `~/wiki/research/YYYY/MM/YYYY-MM-DD/`, then removes `~/wiki/today/`. The date used is `today/journal.md`'s creation date, not the date the script happens to run on — a session that starts in the evening and is archived after midnight still files under the day it started. Run this after step 1, not before — d-handoff still needs `today/` in place. Completion criterion: the script ran and `~/wiki/today/` no longer exists.
3. **Seed tomorrow's work context** — write a fresh `~/wiki/today/journal.md` (`mkdir -p` the parent; step 2 just removed this file, so create it new — don't reuse an old one), with one section:
   - `## Context to Continue` — from the handoff file written in step 1, its "Open Items" and "Carried Decisions" copied as bullets, exact not paraphrased, capped at 10 bullets total (highest-priority/most-recent first, drop the rest), plus the handoff file's path for full detail. Skip this section if the handoff has neither.
   If the section is skipped, skip the whole step and say so. Completion criterion: `~/wiki/today/journal.md` exists with the section populated at 10 bullets or fewer, or an explicit "nothing to carry" note.
4. **Gather today's sources** — read today's journal file (`~/wiki/journal/YYYY/MM/YYYY-MM-DD.md`), today's research directories (`~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/`), and the file from step 1, all in full. Completion criterion: every source is either read in full or confirmed absent.
5. **Split into content items** — one item per topic, task, or research job from the journal/research, plus one "Handoff" item from the handoff file. Completion criterion: every entry from step 4, including the handoff file, is assigned to exactly one content item.
6. **Draft each content item** in three phases per `../references/document-style.md`: Introduction (1-3 sentences, why/what), Abstraction (the objects, interactions, and relationships involved), Detailed (one representative concrete example, including any research result or finding). Completion criterion: every content item has all three phases, each obeying that file's size limits.
7. **Build the table of contents** — list content item titles in the order they appear, each linking to its section. Completion criterion: ToC entry count equals the content item count from step 5.
8. **Write the markdown report** — assemble ToC + all content items into `~/wiki/journal/YYYY/MM/YYYY-MM-DD-report.md` (`mkdir -p` the parent directory if needed). If it would exceed the 500-word file cap in `../references/document-style.md`, split the largest content items into separate linked files instead of shrinking their phases. Completion criterion: the file exists with a ToC and every content item's three phases.

Tell the user the markdown report path.
