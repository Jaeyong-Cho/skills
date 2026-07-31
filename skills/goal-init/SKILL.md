---
name: goal-init
description: Bootstrap a new goal — create `.context/` to hold the goal's working context, and (re)build `experiments/index.html`, a dashboard linking every experiment's report and viewpoint gallery so results don't stay buried under `experiments/*/gallery/`. Use when starting a new goal per the Goal-to-Implementation Loop, or whenever the experiments dashboard needs refreshing.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Goal Init

Opens the Goal-to-Implementation Loop (see project root `README.md`): create the directory that holds this goal's context, and surface every experiment run so far so its viewpoint gallery is one click away instead of buried in `experiments/*/gallery/`.

## Steps

1. **Create the goal's context directory.** If `.context/` doesn't exist at the project root, create it. Ask the user for a one-line goal statement if they haven't already given one. Write it to `.context/goal.md` — create the file if missing; if it already exists, prepend the new goal under a `## {today's date}` heading rather than overwriting, since a project can carry more than one goal over its life. Done when `.context/goal.md` exists and contains the current goal statement.

2. **Build the experiments dashboard.** Run `python scripts/build_dashboard.py experiments experiments/index.html` from the project root (path relative to this skill's own directory — resolve it against wherever this `SKILL.md` was loaded from). It scans `experiments/{slug}/report.md` for each experiment's hypothesis and verdict, and `experiments/{slug}/gallery/index.html` for a thumbnail, then writes a card grid to `experiments/index.html`. Report the output path when it finishes. If `experiments/` doesn't exist yet or has no finished experiments, say so plainly — the dashboard renders an empty state, that's expected for a brand-new goal until `/experiment` produces its first result. Done when `experiments/index.html` exists and its card count matches the number of `experiments/*/report.md` files present.

`/experiment` calls this same script at the end of its own run (see its step 7) so the dashboard stays in sync without duplicating this logic — don't re-implement dashboard building elsewhere.
