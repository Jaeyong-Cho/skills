---
name: advisor
description: Scan recent journal and research notes for recurring friction and turn it into automation candidates (script, custom agent, or AI-usage change), written as a research note. Invoke as /advisor.
disable-model-invocation: true
---

# Advisor

Read `../references/document-style.md` first — it governs how the research note in step 4 is formatted.

1. **Gather the window** — read every journal file and research directory from the last 14 days (`~/wiki/journal/YYYY/YYYY-MM-DD.md` and `~/wiki/research/YYYY/YYYY-MM-DD/NN-{job}/`); if the user names a different range, use that instead. Completion criterion: every day in the window is either read in full or confirmed absent.
2. **Hunt friction** — across the window, flag anything that recurs: the same manual steps redone more than once, the same blocker hit more than once, a task whose effort repeatedly outweighs its value, or the same question re-asked or re-researched. A single occurrence is not friction; the bar is at least two dated occurrences. Completion criterion: every recurring pattern in the window is named, each backed by its dated occurrences.
3. **Turn friction into automation candidates** — for each named friction, propose exactly one fix, typed as script (a deterministic, repeatable transform), custom agent (needs judgment or context across steps), or AI-usage change (a better prompt, workflow, or skill to reach for). State what it replaces and cite the occurrence count as evidence. Completion criterion: every friction point from step 2 has exactly one typed candidate with its evidence count.
4. **Write the research note** — under `~/wiki/research/YYYY/YYYY-MM-DD/NN-work-pattern-advisor/` (today's date, next unused `NN`), write the window scanned, the friction list, and the automation candidates. Completion criterion: the note exists and every candidate from step 3 appears once.

Tell the user the note's path when done.
