---
name: to-context
description: Write up this session as a context document — objective, background, key facts, current state — so a fresh session can resume it cold. Filed alongside @skills/experiment output. Invoke as /to-context.
disable-model-invocation: true
---

# To-Context

Capture this session as reusable context instead of leaving it locked in chat history.

1. **Follow document style.** Read `../references/document-style.md` first — its structure and size limits govern the draft.
2. **Scope the session** — reread it in full. Pull out: Objective (what was asked), Background (why it matters / what triggered it), Key facts (decisions, findings, constraints discovered), Current state (what exists now, what changed), Open questions (anything unresolved). Completion criterion: each has content traceable to the session, or is explicitly noted empty.
3. **Draft the context, exact not paraphrased** — per `../references/document-style.md` priority order: key-value block for Objective/Background/Current state, bullets for Key facts and Open questions. Any file, command, or identifier the session touched is written as its exact string (`../references/good-harness.md`, not "a harness reference doc"; `npm run test:unit`, not "the test command") — a fresh reader must be able to open or run it verbatim. No invented facts.
4. **Write it.** If this session already wrote a `contexts/{nn}-{slug}.md` file, update that file in place with the current Objective/Background/Key facts/Current state/Open questions instead of creating another one — a context document tracks the session's latest state, not a history of drafts. Otherwise, read `../references/research-topic-directory.md` first — confirm `{NN}-{slug}` with the user (new directory vs. an existing one from today, e.g. the one `@skills/experiment` used if this session continues that job) before writing, skipping re-asking if already confirmed earlier this session — then write to `{NN}-{slug}/contexts/{nn}-{slug}.md` under `~/wiki/today/research/`, creating the directory if needed, `{nn}` the next zero-padded sequence number inside `contexts/` (count existing files there; starts at `01`).

Completion criterion: the file exists, and a fresh reader with zero session history could resume the work from it alone.

Tell the user the file path when done.

Use bellow question format
```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```
