---
name: goal-init
description: Bootstrap a new goal — write the goal statement and its open questions to `goal.md` at the project root, create a `questions/{slug}/` directory for each question, and (re)build `questions/index.html`, a dashboard linking every question's report and viewpoint gallery. Use when starting a new goal per the Goal-to-Implementation Loop, when adding a new question to an existing goal, or whenever the dashboard needs refreshing.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Goal Init

Opens the Goal-to-Implementation Loop (see project root `README.md`): record the goal and its open questions, give each question its own directory, and surface every question's result so its gallery is one click away instead of buried in `questions/*/gallery/`. This is where `/explore` -> `/experiment` -> `/viewpoints` (see `../experiment/references/pipeline.md`) get the directory they write into — none of those three creates one itself.

## Steps

1. **Record the goal statement.** Ask the user for a one-line goal if they haven't given one. Write it to `goal.md` — create if missing; if it exists, prepend under a `## {today's date}` heading rather than overwriting (a project can carry more than one goal over its life).

2. **Record the open questions.** Ask what question(s) need resolving toward this goal, if not already given (one or several; more can be added later by re-running this step). Append each as its own `## Question N` heading, continuing numbering rather than restarting at 1:

   ```
   ## Question 3
   Does the cache TTL bound P99 latency?
   ```

3. **Create each question's directory.** For every `## Question N` heading without one yet, slugify its text into `{slug}` (kebab-case, e.g. `cache-ttl-bound-p99-latency`) and create `questions/{slug}/` — empty is enough; `/explore`, `/experiment`, `/viewpoints` fill it in later.

4. **Build the questions dashboard.** Run `python scripts/build_dashboard.py questions questions/index.html` (path relative to this skill's directory). Scans `questions/{slug}/report.md` for hypothesis/verdict and `questions/{slug}/gallery/index.html` for a thumbnail, writes a card grid plus stats bar to `questions/index.html`. A question with no `report.md` yet is skipped, not shown broken. `/experiment` calls this same script at the end of its own Publish step — don't reimplement it elsewhere.

5. **Serve the dashboard.** Copy `scripts/serve.sh` to `questions/` (binds `0.0.0.0:4800`; pass a second arg to override the port), then report the URL: http://localhost:4800. MUST NOT run the server — the user runs it manually.
