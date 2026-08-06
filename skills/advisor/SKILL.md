---
name: advisor
description: Advisor for recurring work-pattern friction — scans the last 14 days of journal and research notes and turns repeated friction into automation candidates (script, custom agent, or AI-usage change). Use when the user wants advice on improving their workflow, asks what to automate, or wants a work-pattern review; also reached by daily-report before drafting.
---

# Advisor

Read `../references/document-style.md` first — it governs how the advisor file in step 4 is formatted.

1. **Gather the window** — read every journal file and research directory from the last 14 days (`~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` and `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/`); if the user names a different range, use that instead. The window commonly spans two `MM` (or `YYYY`) directories — check both, not just the current month's. Completion criterion: every day in the window is either read in full or confirmed absent.
2. **Hunt friction** — across the window, flag anything that recurs: the same manual steps redone more than once, the same blocker hit more than once, a task whose effort repeatedly outweighs its value, or the same question re-asked or re-researched. A single occurrence is not friction; the bar is at least two dated occurrences. Completion criterion: every recurring pattern in the window is named, each backed by its dated occurrences.
3. **Turn friction into automation candidates** — for each named friction, propose exactly one fix, typed as script (a deterministic, repeatable transform), custom agent (needs judgment or context across steps), or AI-usage change (a better prompt, workflow, or skill to reach for). State what it replaces and cite the occurrence count as evidence. Completion criterion: every friction point from step 2 has exactly one typed candidate with its evidence count.
4. **Write the advisor file** — write the window scanned, the friction list, and the automation candidates to `~/wiki/advisor/YYYY/MM/YYYY-MM-DD.md` (today's date; `mkdir -p` the parent if needed). Completion criterion: the file exists and every candidate from step 3 appears once.

Tell the user the file's path when done.
