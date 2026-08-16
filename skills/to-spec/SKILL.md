---
name: to-spec
description: Write this session's spec-grill-me decisions directly into the target project's spec/**/*.md and todo/**/*.md — requirements and acceptance criteria in spec, one vertical-slice todo per sub-topic in todo. Invoke as /to-spec.
disable-model-invocation: true
---

# To-Spec

Turn this session's decisions into the target project's persisted spec and todo. Unlike `@skills/to-plan`, this writes only spec + todo — no branch/release plan; use it when the spec itself is the deliverable (e.g. spec-first, or documenting settled behavior) rather than a step toward `@skills/do-plan`.

1. **Follow document style.** Read `../references/document-style.md` first — its size limits govern the draft.
2. **Follow spec convention.** Read `../references/spec-convention.md` first — locate the target project's `spec/{topic-slug}.md` (or `spec/{area}/{topic-slug}.md`); create `spec/` if it doesn't exist yet.
3. **Follow requirements engineering.** Read `../references/requirement-engineering.md` first — its Acceptance Criteria format (Given-When-Then, Category, Verification Method) is what step 4 fills in; every row's Verification Method must name a real test file/path, not "manual" unless the check genuinely can't be automated.
4. **Draft one spec per topic** the session settled (a `@skills/spec-grill-me` session may cover one or more), each per `../template/spec.md`: Introduction (3 sentences), one sub-topic per requirement area — each sub-topic a vertical slice — ending in an AC block. Pull content only from this session's settled decisions — no invented requirements.
5. **Write each spec** to its own `spec/{topic-slug}.md` in the target project, and update `spec/index.md` in the same change — an unlisted spec file is treated as not done.
6. **Follow todo convention.** Read `../references/todo-convention.md` first, then draft one `todo/{topic-slug}.md` per vertical slice (per sub-topic in step 4) using `../template/todo.md`: a link back to its spec sub-topic, then `- [ ] action` items that build the slice end-to-end (not layered by frontend/backend). Pull items only from this session's settled decisions.
7. **Write each todo** to its own `todo/{topic-slug}.md` in the target project, and update `todo/index.md` in the same change — an unlisted todo file is treated as not done.
8. **Update the project overview.** Update `spec/overview.md` (create it if missing, per `../references/spec-convention.md`) so its paragraph still describes what the project does after this change, linking to `spec/index.md` for detail. Don't restate requirements or AC there — link, don't duplicate.

Completion criterion: every topic from this session has its own spec file with every sub-topic's AC block traceable to a decision from this session, plus its own todo file, `spec/index.md` and `todo/index.md` list all of them, and `spec/overview.md` reflects the same change.

Tell the user the file path when done.
