---
name: to-preference
description: Sweep this session for confirmed decisions and corrections that generalize beyond it, and record them as standing preferences. Invoke as /to-preference.
disable-model-invocation: true
---

# To-Preference

Read `../../references/preference-format.md` first — it defines the standing-vs-one-off test, file locations, and entry format that every step below uses.

1. **Scope the session** — reread the full session, not just the last few turns. For every place the user corrected an approach, confirmed a non-obvious recommendation, or stated an explicit rule, note a candidate: the rule in one line, and one line on why it's standing rather than specific to this session's task. Completion criterion: every correction or confirmation in the session is checked, and each surviving candidate has both lines. If no candidates survive, tell the user nothing qualified and stop.
2. **Classify scope** — for each candidate, pick cross-project vs this-project-only per `../../references/preference-format.md`, then check that topic file (and related topic files) for an existing bullet covering the same ground. Completion criterion: every candidate has a target file path, and any that would duplicate or contradict an existing bullet is flagged with what it conflicts with.
3. **Confirm with the user** — list the candidates (rule, target file, new or flagged) and ask the user to approve, edit, or drop each. This skill infers preferences after the fact rather than recording them live like `get-me` does, so nothing gets written without approval. Completion criterion: the user has approved a final set, possibly empty.
4. **Write** — append each approved candidate to its target file per `../../references/preference-format.md`'s entry format, creating the topic file (and `.context/preferences/` directory) if it doesn't exist. Completion criterion: every approved candidate appears in its target file exactly once; no flagged duplicate was written twice.

Tell the user which files were touched, or that nothing was written, when done.
