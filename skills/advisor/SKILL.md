---
name: advisor
description: Advisor for recurring work-pattern friction and unclaimed value — scans the last 14 days of journal and research notes, turns repeated friction into automation candidates (script, custom agent, or AI-usage change), and surfaces valuable items, open tasks, and project ideas mentioned but not pursued. Use when the user wants advice on improving their workflow, asks what to automate, wants a work-pattern review, or wants ideas for what to do next; also reached by end-of-day before drafting.
---

# Advisor

Read `../references/document-style.md` first — it governs how the advisor file in step 5 is formatted.

1. **Gather the window** — read every journal file and research directory from the last 14 days (`~/wiki/journal/YYYY/MM/YYYY-MM-DD.md` and `~/wiki/research/YYYY/MM/YYYY-MM-DD/NN-{job}/`); for today specifically, read `~/wiki/today/journal.md` and `~/wiki/today/research/NN-{job}/` instead, since today's work hasn't been archived to a dated path yet. If the user names a different range, use that instead. The window commonly spans two `MM` (or `YYYY`) directories — check both, not just the current month's. Completion criterion: every day in the window is either read in full or confirmed absent.
2. **Hunt friction** — across the window, flag anything that recurs: the same manual steps redone more than once, the same blocker hit more than once, a task whose effort repeatedly outweighs its value, or the same question re-asked or re-researched. A single occurrence is not friction; the bar is at least two dated occurrences. Completion criterion: every recurring pattern in the window is named, each backed by its dated occurrences.
3. **Surface opportunities** — across the same window, flag valuable items that aren't friction: an idea mentioned in passing but never picked up, a task flagged as worth doing but deprioritized, a gap noticed during other work, or a project idea raised once. Bar is a single dated mention, but note it as speculative unless something in the notes signals real intent (a "should do", a deadline, a stated want). Completion criterion: every opportunity found is named with its date and source note.
4. **Turn findings into candidates** — for each friction point, propose exactly one fix, typed as script (a deterministic, repeatable transform), custom agent (needs judgment or context across steps), or AI-usage change (a better prompt, workflow, or skill to reach for); state what it replaces and cite the occurrence count as evidence. For each opportunity, propose exactly one next action, typed as task (a concrete, boundable piece of work) or project idea (open-ended, needs scoping); state the source date. Completion criterion: every item from steps 2 and 3 has exactly one typed candidate.
5. **Write the advisor file** — write the window scanned, the friction list, the opportunity list, and their candidates to `~/wiki/advisor/YYYY/MM/YYYY-MM-DD.md` (today's date; `mkdir -p` the parent if needed). Completion criterion: the file exists and every candidate from step 4 appears once.

Tell the user the file's path when done.
