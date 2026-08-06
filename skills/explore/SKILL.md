---
name: explore
description: Explore the codebase or docs to answer a question, escalating to /experiment when exploring alone can't resolve it. Invoke as /explore.
disable-model-invocation: true
---

# Explore

Answer a question by reading and searching before falling back to running anything.

1. **Explore.** Search the codebase and docs for the answer. Completion criterion: the question is answered with cited evidence, or exploring genuinely can't resolve it.
2. **Escalate if unresolved.** If step 1 can't answer the question (It is needed to test, run, need to read large data, files, etc) , run `/experiment` (Skill tool) to find the answer by doing.
3. **Record it.** Create a directory for this question, `explores/{slug}/` (kebab-case slug of the question), and write the results and evidence there in `../references/document-style.md` style.

Completion criterion: the question has a written answer with evidence, filed under the question's context directory.
