---
name: explore
description: Explore the codebase or docs to answer a question, escalating to /experiment when exploring alone can't resolve it. Invoke as /explore.
disable-model-invocation: true
---

# Explore

Answer a question by reading and searching before falling back to running anything.

1. **Explore.** Search the codebase, web, known things and docs for the answer. Completion criterion: the question is answered with cited evidence, or exploring genuinely can't resolve it.
2. **Escalate if unresolved.** If step 1 can't answer the question (It is needed to test, run, need to read large data, files, etc) , run `/experiment` (Skill tool) to find the answer by doing.
3. **MUST Record it.** Write the results and evidence to `~/wiki/research/{date}/{NN}-{slug}/explore.md`, in `../references/document-style.md` style — `{date}` from `date +%Y/%m/%Y-%m-%d`, `{slug}` a kebab-case slug of the question, `{NN}` the next zero-padded sequence number for that day (count existing `NN-*` directories under the day's folder).

Completion criterion: the question has a written answer with evidence, filed under the research directory.
