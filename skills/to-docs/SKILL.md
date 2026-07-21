---
name: to-docs
description: Write up the current session's work as a document in the repo's report style. Invoke as /to-docs.
disable-model-invocation: true
---

# To-Docs

Read `../references/document-style.md` first — its structure and tone are what the draft in step 3 must follow.

1. **Scope the session** — reread the full session, not just the last few turns. Pull out the objective or trigger, what was tried, the key facts/decisions/findings, and the outcome. Completion criterion: every distinct piece of work in the session is accounted for, and you can state its objective, its key facts, and its outcome each in one sentence. If the session covers more than one unrelated task, ask the user which one(s) to document.
2. **Ask for the destination** — ask the user for the file path to write to. Do not assume a location. Completion criterion: user has given a concrete file path.
3. **Draft in document style** — using `../references/document-style.md`, write: an Introduction (objective, background, scope, methodology), a Body (facts, analysis, findings, evidence), and a Conclusion (key takeaways, recommendations, next actions). Short sentences, one idea each, key information first. Before defaulting to bullets, check each chunk of Body content against the priority order: a sequence of steps/stages the session went through → ASCII flow diagram; options weighed, before/after, or other parallel-attribute content → Markdown table; only content with no flow or comparison shape stays as bullets.
4. **Write the file** — `mkdir -p` the parent directory if needed, then write the draft to the confirmed path. Completion criterion: the file exists at that path and its Introduction/Body/Conclusion each reflect facts from step 1, not invented ones.

Tell the user the file path when done.
