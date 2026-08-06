---
name: d-handoff
description: Distill today's journal and research notes into open items and carried decisions for tomorrow, written to a dated handoff file. Invoke as /d-handoff.
disable-model-invocation: true
---

# Handoff

Read `../references/document-style.md` first — it governs how the handoff file is formatted.

1. **Gather today's sources** — read today's journal file (`~/wiki/journal/YYYY/YYYY-MM-DD.md`) in full and list today's research directories (`~/wiki/research/YYYY/YYYY-MM-DD/NN-{job}/`). If neither exists, tell the user and stop. Completion criterion: every journal entry and every research directory for today is either read in full or confirmed absent.
2. **Extract handoff items** — for every entry from step 1, decide keep or drop: keep an unfinished task, a blocker, an open question, a next concrete action, or a decision/fact whose consequences reach past today; drop only what's fully closed and inconsequential tomorrow. Completion criterion: every entry from step 1 has an explicit keep/drop decision, not a silent skim.
3. **Write the handoff** — format kept items per `../references/document-style.md` (key-value/bullets, no prose padding), under two headings: "Open Items" (each with its next concrete action) and "Carried Decisions" (each with why it matters tomorrow). Write to `~/wiki/journal/YYYY/YYYY-MM-DD-handoff.md` (today's date; `mkdir -p` the parent if needed). Completion criterion: file exists and every kept item from step 2 appears once, under the correct heading.
4. **Breadcrumb today's journal** — append one line to today's journal file naming the handoff file's path, so a session reading forward from today's log finds it. Completion criterion: today's journal file contains that line.

Tell the user the file path when done.
