# Todo Document Convention

WBS terms: **EPIC** = a spec topic (`spec/{topic-slug}.md`) — a business-level requirement, a set of related stories. **STORY** = a spec sub-topic — done means the user gets one specific value or feature. **TASK** = one `todo/{epic-slug}/{story-slug}/{task-slug}.md` file — work to build or support a story; a story may need one or more tasks.

A target project's task todos live under `todo/{epic-slug}/{story-slug}/*.md`, one file per task, never a horizontal layer (e.g. not "backend" + "frontend" for one story).

Each task file is temp scratch, not a persisted document like `spec/`: no per-file ceremony beyond the link and checklist. Format:

```
Spec: spec/{topic-slug}.md#{sub-topic}

- [ ] {action item}
- [ ] {action item}
```

- One file per task: `todo/{epic-slug}/{story-slug}/{task-slug}.md` — the directory nesting already says which EPIC/STORY the task belongs to.
- First line still links back to the story's spec sub-topic, so the file is self-contained even if moved — the task lists *how*, the spec already said *what*; don't restate AC or requirements here.
- Checklist ordered so the task completes end-to-end top to bottom.
- Delete the file once every item is checked; delete the `{story-slug}/` directory once it's empty — it's disposable, the spec is the record that lasts.

## `todo/index.md` — the EPIC / STORY / TASK WBS guide

`todo/index.md` is the work-breakdown-structure: every EPIC's stories, each story's tasks, and task ordering. Format:

```
# EPIC: {epic-slug}

## STORY: {story-slug} — spec/{epic-slug}.md#{sub-topic}
Round 1: {task-slug-a}, {task-slug-b}
Round 2: {task-slug-c}*
```

- One `# EPIC` heading per `todo/{epic-slug}/` directory, one `## STORY` heading per `{story-slug}/` subdirectory underneath it — headings mirror the directory tree.
- Under each story, one line per round of its tasks (bare `{task-slug}`, resolved against `todo/{epic-slug}/{story-slug}/{task-slug}.md`); a round's tasks can run in parallel, later rounds depend on all earlier rounds finishing.
- Mark the critical-path task(s) with `*` and name why in a trailing legend line if it isn't obvious.
- Adding, finishing, or deleting a task file updates `todo/index.md` in the same change — an unlisted task is treated as not scheduled.
- Delete a task's line once its file is deleted; delete the STORY heading once its directory is empty; delete the EPIC heading once no stories remain; delete `todo/index.md` itself once `todo/` is empty.
