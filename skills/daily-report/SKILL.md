---
name: daily-report
description: Compile today's journal and research notes into a report with a table of contents and an Introduction/Abstraction/Detailed breakdown per topic. Invoke as /daily-report.
disable-model-invocation: true
---

# Daily Report

Read `../references/document-style.md` first — its Introduction/Abstraction/Detailed structure and priority order (key-value > table > bullets > prose) govern every section this skill writes.

1. **Gather today's sources** — read today's journal file (`~/wiki/journal/YYYY/YYYY-MM-DD.md`) in full and list today's research directories (`~/wiki/research/YYYY/YYYY-MM-DD/NN-{job}/`). If neither exists, tell the user and stop. Completion criterion: every journal entry and every research directory for today is either read in full or confirmed absent.
2. **Split into content items** — group today's raw entries into distinct content items, one per topic, task, or research job. Completion criterion: every journal entry and every research directory is assigned to exactly one content item, and none are dropped.
3. **Draft each content item** in three phases per `../references/document-style.md`: Introduction (1-3 sentences, why/what), Abstraction (the objects, interactions, and relationships involved), Detailed (one representative concrete example). Completion criterion: every content item has all three phases, each obeying that file's size limits.
4. **Build the table of contents** — list content item titles in the order they appear, each linking to its section. Completion criterion: ToC entry count equals the content item count from step 2.
5. **Write the report** — assemble ToC + all content items into `~/wiki/journal/YYYY/YYYY-MM-DD-report.md` (`mkdir -p` the parent directory if needed). If the assembled file would exceed the 500-word file cap in `../references/document-style.md`, split the largest content items into separate linked files instead of shrinking their phases. Completion criterion: the file exists at that path with a ToC and every content item's three phases present.

Tell the user the file path when done.
