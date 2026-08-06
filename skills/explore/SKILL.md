---
name: explore
description: Explore the codebase or docs to answer a question, escalating to /experiment when exploring alone can't resolve it. Invoke as /explore.
disable-model-invocation: true
---

# Explore

Answer a question by reading and searching before falling back to running anything.

1. **Explore.** Search the codebase, web, known things and docs for the answer. Completion criterion: the question is answered with cited evidence, or exploring genuinely can't resolve it.
2. **Escalate if unresolved.** If step 1 can't answer the question (It is needed to test, run, need to read large data, files, etc) , run `/experiment` (Skill tool) to find the answer by doing.
3. **MUST Record it.** If this session already wrote an `explores/{nn}-{slug}.md` file for the same question, update that file in place with the new findings instead of creating another one. Otherwise write the results and evidence to `~/wiki/research/{date}/{NN}-{slug}/explores/{nn}-{slug}.md`, in `../references/document-style.md` style — `{date}` from `date +%Y/%m/%Y-%m-%d`, `{slug}` a kebab-case slug of the question, `{NN}` the zero-padded sequence number for that day, starting at `00` (count existing `NN-*` directories under the day's folder), `{nn}` the next zero-padded sequence number inside `explores/` (count existing files there; starts at `01`).

Completion criterion: the question has a written answer with evidence, filed under the research directory.
