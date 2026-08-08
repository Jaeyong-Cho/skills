---
name: to-goal
description: Turn this session's ongoing effort into a persistent, multi-day goal via `ng` — registers it in ~/wiki/goals.md, creates ~/wiki/goals/{slug}/, and links it into today's research. Invoke as /to-goal.
disable-model-invocation: true
---

# To-Goal

Turn what this session is working toward into a tracked goal instead of letting it stay a one-off session.

1. **Follow document style.** Read `../references/document-style.md` — the description in step 3 is bound by its 1-3 sentence limit.
2. **Scope the effort** — reread the session and name the ongoing, multi-day effort this should track (not a one-off task — it needs to still matter tomorrow). If the session covers more than one such effort, or none, ask the user which. Completion criterion: one effort named, with a reason it's multi-day.
3. **Derive slug and description** — a kebab-case slug (`ng` requires `^[a-z0-9][a-z0-9-]*$`) and a 1-sentence description. Confirm both with the user if not obvious from the session.
4. **Check for an existing goal first** — run `ng list`. If a goal with the same or an overlapping slug already exists, stop and ask the user whether they meant to continue that one instead of creating a duplicate.
5. **Create it** — run `ng <slug> "<description>"`. This registers the goal under `## Active` in `~/wiki/goals.md`, creates `~/wiki/goals/<slug>/`, links it into `~/wiki/today/research/NN-<slug>`, and appends a checklist entry to today's journal. Completion criterion: command exits 0.

Tell the user the goal's slug when done, and that `/end-of-day` re-links it into `today/research/` daily until it's moved to `## Done` in `goals.md`.
