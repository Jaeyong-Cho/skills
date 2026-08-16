---
name: to-spec
description: Write this session's spec-grill-me decisions directly into the target project's spec/**/*.md and todo/**/*.md — requirements and acceptance criteria in spec, one or more TASK todos per STORY sub-topic in todo. Invoke as /to-spec.
disable-model-invocation: true
---

# To-Spec

Turn this session's decisions into the target project's persisted spec, plus temp TASK todo files per STORY. Unlike `@skills/to-plan`, this writes no branch/release plan; use it when the spec itself is the deliverable (e.g. spec-first, or documenting settled behavior) rather than a step toward `@skills/do-plan`.

1. **Follow document style.** Read `../references/document-style.md` first — its size limits govern the draft.
2. **Follow spec convention.** Read `../references/spec-convention.md` first — locate the target project's `spec/{topic-slug}.md` (or `spec/{area}/{topic-slug}.md`); create `spec/` if it doesn't exist yet.
3. **Follow requirements engineering.** Read `../references/requirement-engineering.md` first — its Acceptance Criteria format (Given-When-Then, Category, Verification Method) is what step 4 fills in; every row's Verification Method must name a real test file/path, not "manual" unless the check genuinely can't be automated.
4. **Draft one spec per EPIC** the session settled (a `@skills/spec-grill-me` session may cover one or more topics), each per `../template/spec.md`: Introduction (3 sentences), one sub-topic per requirement area — each sub-topic a STORY — ending in an AC block. Pull content only from this session's settled decisions — no invented requirements.
5. **Write each spec** to its own `spec/{topic-slug}.md` in the target project, and update `spec/index.md` in the same change — an unlisted spec file is treated as not done.
6. **Follow todo convention.** Read `../references/todo-convention.md` first, then write one `todo/{task-slug}.md` per TASK (one or more per STORY sub-topic from step 4) using `../template/todo.md`'s format exactly: a link back to its spec sub-topic, then `- [ ] action` items that complete the task end-to-end (not layered by frontend/backend). Pull items only from this session's settled decisions. It's temp scratch, delete once checked off.
7. **Update `todo/index.md`.** Per `../references/todo-convention.md`'s EPIC/STORY/TASK WBS guide format, add every new task under its EPIC/STORY heading and round based on this session's settled task ordering, marking the critical path — an unlisted task is treated as not scheduled.
8. **Update the project overview.** Update `spec/overview.md` (create it if missing, per `../references/spec-convention.md`) so its paragraph still describes what the project does after this change, linking to `spec/index.md` for detail. Don't restate requirements or AC there — link, don't duplicate.

Completion criterion: every EPIC from this session has its own spec file with every STORY's AC block traceable to a decision from this session, plus its TASK file(s) scheduled in `todo/index.md`, and `spec/index.md`/`spec/overview.md` reflect the same change.

Tell the user the file path when done.
